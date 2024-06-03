/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = 'awesome_dashboard.pie_chart_card';
    static props = {
        title: { type: String },
        ...PieChart.props,
    };
    static components = { PieChart };
}
