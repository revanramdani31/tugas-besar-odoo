{
    'name': 'Toko Sentosa POS Custom',
    'version': '19.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Modifikasi ringan POS untuk tracking barcode & catatan kasir',
    'depends': ['point_of_sale', 'stock'],
    'data': ['views/pos_order_views.xml'],
    'assets': {
        'point_of_sale.assets': [
            'toko_sentosa_pos_custom/static/src/xml/pos_order_templates.xml',
            'toko_sentosa_pos_custom/static/src/js/pos_order_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}