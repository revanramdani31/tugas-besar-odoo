/** @odoo-module */

import { PaymentInterface } from "@point_of_sale/app/utils/payment/payment_interface";
import { register_payment_method } from "@point_of_sale/app/services/pos_store";
import { loadJS } from "@web/core/assets";

export class PaymentMidtrans extends PaymentInterface {
    
    /**
     * @override
     */
    async sendPaymentRequest(cid) {
        super.sendPaymentRequest(cid);
        const order = this.pos.getOrder();
        const line = order.getPaymentlineByUuid(cid) || order.getSelectedPaymentline();
        const method_id = this.payment_method_id.id || this.payment_method_id;
        
        try {
            // 1. Get Snap Token from Odoo Backend
            const data = await this.env.services.orm.call(
                'pos.payment.method',
                'midtrans_get_snap_token',
                [
                    order.uid,
                    line.amount,
                    order.getPartner() ? order.getPartner().name : 'POS Customer',
                    method_id
                ]
            );

            if (!data || !data.token) {
                this._show_error("Could not generate Midtrans Snap Token.");
                return false;
            }

            // 2. Load Snap JS dynamically based on environment
            const snapJsUrl = data.environment === 'production' 
                ? 'https://app.midtrans.com/snap/snap.js' 
                : 'https://app.sandbox.midtrans.com/snap/snap.js';
                
            await loadJS(snapJsUrl);
            
            // 3. Trigger Snap Popup
            return new Promise((resolve) => {
                window.snap.pay(data.token, {
                    onSuccess: (result) => {
                        console.log("Midtrans payment success:", result);
                        line.setPaymentStatus('done');
                        resolve(true);
                    },
                    onPending: (result) => {
                        console.log("Midtrans payment pending:", result);
                        this._show_error("Payment is pending. Please check Midtrans dashboard.");
                        line.setPaymentStatus('retry');
                        resolve(false);
                    },
                    onError: (result) => {
                        console.error("Midtrans payment error:", result);
                        this._show_error("Payment failed: " + (result.status_message || "Unknown error"));
                        line.setPaymentStatus('retry');
                        resolve(false);
                    },
                    onClose: () => {
                        console.log("Midtrans popup closed by user.");
                        line.setPaymentStatus('retry');
                        resolve(false); // Customer closed without paying
                    }
                });
            });
            
        } catch (error) {
            console.error("Error in Midtrans sendPaymentRequest:", error);
            this._show_error("Failed to connect to Midtrans: " + (error.message ? error.message.message || error.message : error));
            line.setPaymentStatus('retry');
            return false;
        }
    }

    /**
     * @override
     */
    sendPaymentCancel(order, cid) {
        super.sendPaymentCancel(order, cid);
        const line = order.getPaymentlineByUuid(cid) || order.getSelectedPaymentline();
        line.setPaymentStatus('retry');
        return Promise.resolve(true);
    }

    _show_error(msg) {
        if (this.env.services.popup) {
            import("@point_of_sale/app/errors/popups/error_popup").then((m) => {
                if (m.ErrorPopup) {
                    this.env.services.popup.add(m.ErrorPopup, {
                        title: "Midtrans Error",
                        body: msg,
                    });
                } else {
                    alert("Midtrans Error: " + msg);
                }
            }).catch(() => alert("Midtrans Error: " + msg));
        } else {
            alert("Midtrans Error: " + msg);
        }
    }
}

// Register the payment method
register_payment_method('midtrans', PaymentMidtrans);
