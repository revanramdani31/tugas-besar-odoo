import logging
import requests
import base64
from odoo import api, fields, models
import uuid
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [('midtrans', 'Midtrans')]

    # Midtrans credentials directly on the payment method for POS
    midtrans_merchant_id = fields.Char(string="Midtrans Merchant ID", groups='base.group_system')
    midtrans_client_key = fields.Char(string="Midtrans Client Key", groups='base.group_system')
    midtrans_server_key = fields.Char(string="Midtrans Server Key", groups='base.group_system')
    midtrans_environment = fields.Selection([
        ('sandbox', 'Sandbox'),
        ('production', 'Production')
    ], string="Midtrans Environment", default='sandbox')

    @api.model
    def midtrans_get_snap_token(self, order_uid, amount, customer_name, method_id):
        """Called from POS JS to get the Snap token for a specific order."""
        payment_method = self.sudo().browse(method_id)
        if not payment_method or payment_method.use_payment_terminal != 'midtrans':
            raise ValidationError("Invalid Payment Method for Midtrans.")

        api_url = 'https://app.midtrans.com/snap/v1/transactions' if payment_method.midtrans_environment == 'production' else 'https://app.sandbox.midtrans.com/snap/v1/transactions'
        
        server_key = (payment_method.midtrans_server_key or '').strip()
        auth_string = f"{server_key}:".encode('utf-8')
        encoded_auth = base64.b64encode(auth_string).decode('utf-8')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_auth}',
        }

        unique_order_id = f"{order_uid}-{str(uuid.uuid4())[:8]}"
        payload = {
            "transaction_details": {
                "order_id": unique_order_id,
                "gross_amount": int(amount),
            },
            "customer_details": {
                "first_name": customer_name or "POS Customer",
            }
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                'token': data.get('token'),
                'client_key': payment_method.midtrans_client_key,
                'environment': payment_method.midtrans_environment
            }
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - Details: {e.response.text}"
            _logger.error("Midtrans API error (POS): %s", error_msg)
            raise ValidationError(f"Could not connect to Midtrans: {error_msg}")
