/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";

patch(ProductCard.prototype, {
    /**
     * Returns stock level category string for CSS class binding.
     */
    get stockLevel() {
        const qty = this.props.product?.qty_available || 0;
        if (qty > 10) return "high";
        if (qty >= 5) return "medium";
        if (qty >= 1) return "low";
        return "zero";
    },

    /**
     * Returns true if the product is out of stock.
     */
    get isOutOfStock() {
        return (this.props.product?.qty_available || 0) <= 0;
    },
});
