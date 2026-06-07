from . import models

def post_init_hook(env):
    categ_rt = env.ref('toko_sentosa_pos_custom.pos_categ_rumah_tangga', raise_if_not_found=False)
    categ_dk = env.ref('toko_sentosa_pos_custom.pos_categ_dekorasi', raise_if_not_found=False)
    
    if categ_rt and categ_dk:
        products = env['product.template'].search([('available_in_pos', '=', True)])
        for p in products:
            if p.categ_id.name and 'Rumah Tangga' in p.categ_id.name:
                p.write({'pos_categ_ids': [(4, categ_rt.id)]})
            elif p.categ_id.name and 'Dekorasi' in p.categ_id.name:
                p.write({'pos_categ_ids': [(4, categ_dk.id)]})
