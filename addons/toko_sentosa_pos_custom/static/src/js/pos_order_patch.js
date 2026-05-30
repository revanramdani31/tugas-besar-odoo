/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        this.x_barcode_verified = this.x_barcode_verified || false;
        this.x_cashier_notes = this.x_cashier_notes || "";
    },
    
    serializeForORM(opts = {}) {
        const res = super.serializeForORM(...arguments);
        if (this.x_barcode_verified !== undefined) {
            res.x_barcode_verified = this.x_barcode_verified;
        }
        if (this.x_cashier_notes !== undefined) {
            res.x_cashier_notes = this.x_cashier_notes;
        }
        return res;
    }
});
