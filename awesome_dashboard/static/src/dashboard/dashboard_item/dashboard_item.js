/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
        slots: {
            type: Object,
            shape: {
                default: true,
            },
        },
    };
}
