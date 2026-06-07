/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { HazardousItemPopup } from "@toko_sentosa_pos_custom/js/hazardous_item_popup";
import { useService } from "@web/core/utils/hooks";

// ProductScreen.addProductToOrder() adalah method yang dipanggil
// setiap kali produk diklik di layar POS (line 418 product_screen.js)
// Barcode scan memanggil _barcodeProductAction — kita patch itu juga

patch(ProductScreen.prototype, {

    setup() {
        super.setup(...arguments);
        // Odoo 19: gunakan dialog service, bukan popup
        this.hazardDialog = useService("dialog");
    },

    async addProductToOrder(product) {
        const isHazardous = product?.x_is_hazardous
            ?? product?.raw?.x_is_hazardous
            ?? false;

        if (isHazardous) {
            const dlg = this.hazardDialog || this.dialog;
            if (!dlg) {
                console.warn("[Hazardous] Dialog service not available, skipping popup.");
                return super.addProductToOrder(product);
            }
            const confirmed = await new Promise((resolve) => {
                dlg.add(HazardousItemPopup, {
                    product:   product,
                    onConfirm: () => resolve(true),
                    onCancel:  () => resolve(false),
                });
            });
            if (!confirmed) return;
        }

        return super.addProductToOrder(product);
    },

    // Barcode scan masuk via _barcodeProductAction → addLineToCurrentOrder
    // Patch ini menangkap scan barcode produk berbahaya
    async _barcodeProductAction(code) {
        // Jalankan dulu logic parent untuk resolve product dari barcode
        const originalResult = await super._barcodeProductAction(code);

        // Cek apakah produk terakhir yang di-scan adalah berbahaya
        // dengan melihat orderline terakhir yang baru ditambahkan
        const order = this.pos.getOrder();
        const lastLine = order?.getLastOrderline();
        const product = lastLine?.product_id;

        if (product?.x_is_hazardous || product?.raw?.x_is_hazardous) {
            const dlg = this.hazardDialog || this.dialog;
            if (dlg) {
                // Tampilkan warning setelah produk masuk (informational saja untuk barcode)
                dlg.add(HazardousItemPopup, {
                    product:   product,
                    onConfirm: () => {},
                    onCancel:  () => {
                        // Hapus orderline yang baru saja ditambahkan
                        if (lastLine) {
                            order.removeOrderline(lastLine);
                        }
                    },
                });
            }
        }

        return originalResult;
    },
});
