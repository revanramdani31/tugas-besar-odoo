from odoo import models, fields


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

    def _load_pos_data_fields(self, config_id):
        pos_fields = super()._load_pos_data_fields(config_id)
        pos_fields += ['x_is_hazardous', 'x_hazard_type', 'x_hazard_notes', 'qty_available']
        return pos_fields

    def _load_pos_data_read(self, records, config):
        """Tambahkan qty_available dengan konteks gudang agar nilainya tidak 0 untuk POS."""
        res = super()._load_pos_data_read(records, config)
        for data, record in zip(res, records):
            data['qty_available'] = record.with_context(
                warehouse_id=config.picking_type_id.warehouse_id.id
            ).qty_available
        return res


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

    def _load_pos_data_fields(self, config_id):
        """Tambahkan field hazardous ke data yang dikirim ke frontend POS."""
        pos_fields = super()._load_pos_data_fields(config_id)
        pos_fields += ['x_is_hazardous', 'x_hazard_type', 'x_hazard_notes', 'qty_available']
        return pos_fields

    def _load_pos_data_read(self, records, config):
        """Tambahkan qty_available dengan konteks gudang agar nilainya tidak 0."""
        res = super()._load_pos_data_read(records, config)
        for data, record in zip(res, records):
            data['qty_available'] = record.with_context(
                warehouse_id=config.picking_type_id.warehouse_id.id
            ).qty_available
        return res
