/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { HazardousItemPopup } from "@toko_sentosa_pos_custom/js/hazardous_item_popup";

// ProductScreen.addProductToOrder() adalah method yang dipanggil
// setiap kali produk diklik di layar POS (line 418 product_screen.js)
// Barcode scan memanggil addLineToCurrentOrder langsung — kita patch itu juga

patch(ProductScreen.prototype, {

    async addProductToOrder(product) {
        const isHazardous = product?.x_is_hazardous
            ?? product?.raw?.x_is_hazardous
            ?? false;

        if (isHazardous) {
            const confirmed = await new Promise((resolve) => {
                this.env.services.popup.add(HazardousItemPopup, {
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
            // Tampilkan warning setelah produk masuk (informational saja untuk barcode)
            this.env.services.popup.add(HazardousItemPopup, {
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

        return originalResult;
    },
});
