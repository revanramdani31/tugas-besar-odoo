from odoo import api, SUPERUSER_ID

from odoo.addons.toko_sentosa_pos_custom.hooks import apply_pos_category_setup


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    apply_pos_category_setup(env)