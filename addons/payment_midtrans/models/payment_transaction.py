import logging
import requests
import pprint
from werkzeug import urls

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Midtrans-specific rendering values. """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'midtrans':
            return res

        base_url = self.provider_id.get_base_url()
        
        # Prepare Midtrans payload
        payload = {
            "transaction_details": {
                "order_id": self.reference,
                "gross_amount": int(self.amount),
            },
            "customer_details": {
                "first_name": self.partner_name,
                "email": self.partner_email,
                "phone": self.partner_phone,
            },
            "callbacks": {
                "finish": urls.url_join(base_url, '/payment/midtrans/return')
            }
        }
        
        api_url = self.provider_id._get_midtrans_api_url()
        headers = self.provider_id._midtrans_get_api_headers()

        _logger.info("Midtrans request to %s: %s", api_url, pprint.pformat(payload))
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            snap_token = data.get('token')
            if not snap_token:
                raise ValidationError("Midtrans did not return a token.")
        except requests.exceptions.RequestException as e:
            _logger.error("Midtrans API error: %s", str(e))
            raise ValidationError("Could not communicate with Midtrans Payment Gateway.")
            
        env_url = 'https://app.midtrans.com/snap/snap.js' if self.provider_id.midtrans_environment == 'production' else 'https://app.sandbox.midtrans.com/snap/snap.js'

        # The rendering values will be passed to the checkout form template
        return {
            'api_url': '/payment/midtrans/checkout',
            'snap_token': snap_token,
            'client_key': self.provider_id.midtrans_client_key,
            'reference': self.reference,
            'snap_script_url': env_url,
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'midtrans' or len(tx) == 1:
            return tx

        reference = notification_data.get('order_id')
        if not reference:
            raise ValidationError("Midtrans: No reference found in notification data.")

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'midtrans')])
        if not tx:
            raise ValidationError(f"Midtrans: No transaction found matching reference {reference}.")
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'midtrans':
            return

        status = notification_data.get('transaction_status')
        if status in ['capture', 'settlement']:
            self._set_done()
        elif status == 'pending':
            self._set_pending()
        elif status in ['deny', 'cancel', 'expire', 'failure']:
            self._set_canceled("Midtrans payment canceled or failed.")
        else:
            _logger.warning("Midtrans: Received unknown status %s for reference %s", status, self.reference)
