from odoo import api, SUPERUSER_ID


def apply_pos_category_setup(env):
    categ_rt = env.ref('toko_sentosa_pos_custom.pos_categ_rumah_tangga', raise_if_not_found=False)
    categ_dk = env.ref('toko_sentosa_pos_custom.pos_categ_dekorasi', raise_if_not_found=False)

    if categ_rt and categ_dk:
        products = env['product.template'].search([('available_in_pos', '=', True)])
        for product in products:
            if product.categ_id.name and 'Rumah Tangga' in product.categ_id.name:
                product.write({'pos_categ_ids': [(4, categ_rt.id)]})
            elif product.categ_id.name and 'Dekorasi' in product.categ_id.name:
                product.write({'pos_categ_ids': [(4, categ_dk.id)]})

        pos_configs = env['pos.config'].search([])
        for config in pos_configs:
            available_categories = config.iface_available_categ_ids | categ_rt | categ_dk
            config.write({
                'limit_categories': True,
                'iface_available_categ_ids': [(6, 0, available_categories.ids)],
            })


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    apply_pos_category_setup(env)