import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('midtrans', "Midtrans")], ondelete={'midtrans': 'set default'})
    
    midtrans_merchant_id = fields.Char(string="Merchant ID", required_if_provider='midtrans', groups='base.group_system')
    midtrans_client_key = fields.Char(string="Client Key", required_if_provider='midtrans', groups='base.group_system')
    midtrans_server_key = fields.Char(string="Server Key", required_if_provider='midtrans', groups='base.group_system')
    midtrans_environment = fields.Selection([
        ('sandbox', 'Sandbox'),
        ('production', 'Production')
    ], string="Environment", default='sandbox', required_if_provider='midtrans')

    @api.model
    def _get_midtrans_api_url(self):
        """ Return the API URL based on the environment. """
        self.ensure_one()
        if self.midtrans_environment == 'production':
            return 'https://app.midtrans.com/snap/v1/transactions'
        else:
            return 'https://app.sandbox.midtrans.com/snap/v1/transactions'

    def _midtrans_get_api_headers(self):
        self.ensure_one()
        import base64
        auth_string = f"{self.midtrans_server_key}:".encode('utf-8')
        encoded_auth = base64.b64encode(auth_string).decode('utf-8')
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_auth}',
        }
