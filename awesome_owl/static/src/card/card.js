/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {}
    }
    setup() {
        this.state = useState({ isOpen: false });
    }

    toggleState() {
        this.state.isOpen = !this.state.isOpen;
    }

}
