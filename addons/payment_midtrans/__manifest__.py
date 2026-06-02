{
    'name': 'Midtrans Payment Provider',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'A payment provider for Midtrans (Snap Embedded Popup)',
    'description': """Midtrans Payment Provider""",
    'depends': ['payment', 'point_of_sale'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_midtrans_templates.xml',
        'views/pos_payment_method_views.xml',
        'data/payment_provider_data.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'payment_midtrans/static/src/js/payment_midtrans_pos.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
