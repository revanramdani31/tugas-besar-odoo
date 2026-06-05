from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_is_hazardous = fields.Boolean(
        string='Produk Berbahaya',
        default=False,
        help='Centang jika produk ini mengandung bahan berbahaya atau merupakan benda tajam. '
             'Sistem POS akan menampilkan peringatan khusus saat kasir menambahkan produk ini.'
    )
    x_hazard_type = fields.Selection([
        ('chemical',  'Mengandung Zat Kimia Berbahaya'),
        ('sharp',     'Benda Tajam / Berpotensi Melukai'),
        ('flammable', 'Mudah Terbakar / Flammable'),
        ('other',     'Bahaya Lainnya'),
    ], string='Jenis Bahaya')

    x_hazard_notes = fields.Char(
        string='Catatan Bahaya / SOP',
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Related fields agar nilai dari product.template
    # bisa diakses langsung dari product.product (yang dipakai POS)
    x_is_hazardous = fields.Boolean(
        related='product_tmpl_id.x_is_hazardous',
        string='Produk Berbahaya',
        store=True,
    )
    x_hazard_type = fields.Selection(
        related='product_tmpl_id.x_hazard_type',
        string='Jenis Bahaya',
        store=True,
    )
    x_hazard_notes = fields.Char(
        related='product_tmpl_id.x_hazard_notes',
        string='Catatan Bahaya / SOP',
        store=True,
    )

    @api.model
    def _load_pos_data_fields(self, config):
        """Odoo 19: Tambahkan field hazardous ke data yang dikirim ke frontend POS."""
        fields = super()._load_pos_data_fields(config)
        fields += ['x_is_hazardous', 'x_hazard_type', 'x_hazard_notes']
        return fields
