from . import models
from .hooks import apply_pos_category_setup

def post_init_hook(env):
    apply_pos_category_setup(env)
