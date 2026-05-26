odoo.define('toko_sentosa_pos_custom.pos_order_patch', function (require) {
    "use strict";

    const { patch } = require('@web/core/utils/patch');
    const PosOrder = require('point_of_sale.models').PosOrder;

    // Ensure the PosOrder JS model serializes our custom fields when present
    patch(PosOrder.prototype, {
        serializeForStore() {
            const res = this._super(...arguments);
            try {
                // copy any custom fields from this to serialized record
                if (this.x_barcode_verified !== undefined) {
                    res.x_barcode_verified = this.x_barcode_verified;
                }
                if (this.x_cashier_notes !== undefined) {
                    res.x_cashier_notes = this.x_cashier_notes;
                }
            } catch (err) {
                console.error('pos_order_patch serializeForStore error', err);
            }
            return res;
        },
    });

    // Patch OrderTabs order object lookup so templates can access raw values
    const OrderTabs = require('point_of_sale.app.components.order_tabs');
    try {
        patch(OrderTabs.prototype, {
            setup() {
                this.pos = this.env.services.pos;
                this.ui = this.env.services.ui;
                this.dialog = this.env.services.dialog;
            },
        });
    } catch (e) {
        // best-effort; the registry names can differ between versions
        console.debug('toko_sentosa_pos_custom: OrderTabs patch skipped', e);
    }
});
