/** @odoo-module */

import { Component } from "@odoo/owl";

export class Card extends Component { }

Card.template = "awesome_tshirt.Card";
Card.props = {
    slots: {
        type: Object,
        shape: {
            default: Object,
            title: { type: Object, optional: true },
        },
    },
};
