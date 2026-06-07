/** @odoo-module */

import { Component, useState } from "@odoo/owl";

export class HazardousItemPopup extends Component {
    static template = "toko_sentosa_pos_custom.HazardousItemPopup";
    static props = {
        product:   Object,
        onConfirm: Function,
        onCancel:  Function,
        close:     Function,
    };

    static HAZARD_LABELS = {
        chemical:  "Mengandung Zat Kimia Berbahaya",
        sharp:     "Benda Tajam / Berpotensi Melukai",
        flammable: "Mudah Terbakar / Flammable",
        other:     "Bahaya Lainnya",
    };

    static HAZARD_CONFIG = {
        chemical:  { icon: "fa-flask",                color: "#e67e22", bg: "#fef9e7" },
        sharp:     { icon: "fa-cut",                  color: "#e74c3c", bg: "#fdedec" },
        flammable: { icon: "fa-fire",                 color: "#c0392b", bg: "#fdedec" },
        other:     { icon: "fa-exclamation-triangle", color: "#f39c12", bg: "#fef9e7" },
    };

    setup() {
        this.state = useState({
            confirmed: false,
        });
    }

    get hazardLabel() {
        return HazardousItemPopup.HAZARD_LABELS[this.props.product.x_hazard_type] || "Produk Berbahaya";
    }

    get hazardConfig() {
        const type = this.props.product.x_hazard_type || "other";
        return HazardousItemPopup.HAZARD_CONFIG[type] || HazardousItemPopup.HAZARD_CONFIG["other"];
    }

    get hazardNotes() {
        return this.props.product.x_hazard_notes || null;
    }

    get canProceed() {
        return this.state.confirmed;
    }

    toggleConfirm() {
        this.state.confirmed = !this.state.confirmed;
    }

    confirm() {
        if (!this.canProceed) return;
        this.props.close();
        this.props.onConfirm();
    }

    cancel() {
        this.props.close();
        this.props.onCancel();
    }
}
