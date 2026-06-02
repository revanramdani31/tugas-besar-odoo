import logging
import json
import werkzeug
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class MidtransController(http.Controller):

    @http.route('/payment/midtrans/checkout', type='http', auth='public', website=True, csrf=False)
    def midtrans_checkout(self, **kwargs):
        """ 
        Intermediate page to automatically launch the Midtrans Snap popup.
        """
        snap_token = kwargs.get('snap_token')
        client_key = kwargs.get('client_key')
        snap_script_url = kwargs.get('snap_script_url')
        reference = kwargs.get('reference')
        
        if not snap_token:
            return request.redirect('/payment/status')

        return request.render('payment_midtrans.midtrans_snap_checkout_page', {
            'snap_token': snap_token,
            'client_key': client_key,
            'snap_script_url': snap_script_url,
            'reference': reference,
            'return_url': '/payment/status'
        })

    @http.route('/payment/midtrans/return', type='http', auth='public', csrf=False)
    def midtrans_return(self, **kwargs):
        """ Route called after Snap popup is closed or finished. """
        return request.redirect('/payment/status')

    @http.route('/payment/midtrans/notification', type='json', auth='public', csrf=False)
    def midtrans_notification(self, **kwargs):
        """ Webhook from Midtrans """
        data = request.get_json_data()
        _logger.info("Midtrans Notification Received: %s", data)
        try:
            request.env['payment.transaction'].sudo()._handle_notification_data('midtrans', data)
        except ValidationError:
            pass # We return 200 OK anyway to acknowledge receipt to Midtrans
        return {'status': 'ok'}
