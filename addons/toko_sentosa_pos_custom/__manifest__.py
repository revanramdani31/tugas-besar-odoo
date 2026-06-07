{
    'name': 'Toko Sentosa POS Custom',
    'version': '19.0.3.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Kustomisasi POS: UI transaksi, stok badge, member panel, quick cash, peringatan produk berbahaya, dashboard stok',
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
            'toko_sentosa_pos_custom/static/src/xml/product_card_inherit.xml',
            'toko_sentosa_pos_custom/static/src/xml/navbar_inherit.xml',

            # ── JS ───────────────────────────────────────────────────
            'toko_sentosa_pos_custom/static/src/js/pos_order_patch.js',
            'toko_sentosa_pos_custom/static/src/js/hazardous_item_popup.js',
            'toko_sentosa_pos_custom/static/src/js/pos_hazardous_patch.js',
            'toko_sentosa_pos_custom/static/src/js/product_card_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
