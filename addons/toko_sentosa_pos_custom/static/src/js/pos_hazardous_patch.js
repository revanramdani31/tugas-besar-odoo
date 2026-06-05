/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { HazardousItemPopup } from "@toko_sentosa_pos_custom/js/hazardous_item_popup";
import { useService } from "@web/core/utils/hooks";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.hazardDialog = useService("dialog");
    },

    _isProductHazardous(product) {
        // Odoo 19 POS: data field custom ada di dalam product.raw
        // Cek semua kemungkinan lokasi data
        if (product?.raw?.x_is_hazardous) return true;
        if (product?.x_is_hazardous) return true;

        // Fallback: cek via model records cache
        try {
            const allProducts = this.pos?.models?.["product.product"]?.getAll?.() || [];
            const match = allProducts.find(p => p.id === (product?.id || product?.raw?.id));
            if (match?.raw?.x_is_hazardous || match?.x_is_hazardous) return true;
        } catch (e) {
            // ignore
        }

        return false;
    },

    _getProductData(product) {
        // Return data object yang berisi field hazardous untuk popup
        const raw = product?.raw || {};
        return {
            display_name: product?.display_name || raw.display_name || "Unknown",
            x_is_hazardous: raw.x_is_hazardous || product?.x_is_hazardous || false,
            x_hazard_type: raw.x_hazard_type || product?.x_hazard_type || "other",
            x_hazard_notes: raw.x_hazard_notes || product?.x_hazard_notes || "",
        };
    },

    async addProductToOrder(product) {
        const isHazardous = this._isProductHazardous(product);

        console.log("[Hazardous Check]", product?.display_name, "isHazardous:", isHazardous);
        console.log("[Hazardous DEBUG] raw:", JSON.stringify(product?.raw));

        if (isHazardous) {
            const dlg = this.hazardDialog || this.dialog;
            if (dlg) {
                const productData = this._getProductData(product);
                const confirmed = await new Promise((resolve) => {
                    dlg.add(HazardousItemPopup, {
                        product:   productData,
                        onConfirm: () => resolve(true),
                        onCancel:  () => resolve(false),
                    });
                });
                if (!confirmed) return;
            }
        }

        return super.addProductToOrder(product);
    },
});
