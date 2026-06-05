{
    'name': 'Toko Sentosa POS Custom',
    'version': '19.0.2.1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Kustomisasi POS: tracking barcode, catatan kasir, & peringatan produk berbahaya',
    'depends': ['point_of_sale', 'stock'],
    'data': [
        'views/pos_order_views.xml',
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # ── CSS ──────────────────────────────────────────────────
            'toko_sentosa_pos_custom/static/src/css/pos_custom.css',

            # ── XML templates (harus sebelum JS yang merujuknya) ─────
            'toko_sentosa_pos_custom/static/src/xml/pos_order_templates.xml',
            'toko_sentosa_pos_custom/static/src/xml/hazardous_item_popup.xml',

            # ── JS ───────────────────────────────────────────────────
            'toko_sentosa_pos_custom/static/src/js/pos_order_patch.js',
            'toko_sentosa_pos_custom/static/src/js/hazardous_item_popup.js',
            'toko_sentosa_pos_custom/static/src/js/pos_hazardous_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
