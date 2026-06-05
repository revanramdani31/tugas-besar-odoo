from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    x_barcode_verified = fields.Boolean(
        string='Terverifikasi Barcode', 
        default=False, 
        help='Ditandai True jika transaksi menggunakan input barcode scanner'
    )
    x_cashier_notes = fields.Char(
        string='Catatan Kasir', 
        help='Catatan manual dari kasir terkait transaksi ini'
    )
