/** @odoo-module */

import {Component, onWillStart, useRef, onMounted, onWillUnmount} from "@odoo/owl";
import {loadJS} from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: {}
    };

    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        this.board = useRef("board");
        onMounted(() => {
            console.log("mounted")
            console.log(this.props.data);
            const keys = Object.keys(this.props.data);
            const values = Object.values(this.props.data);
            this.pie = new Chart(this.board.el, {
                type: "pie",
                data: {
                    labels: keys,
                    datasets: [
                        {
                            label: this.props.label,
                            data: values,
                        },
                    ],
                },
            });
        });

        onWillUnmount(() => {
            console.log("unmounted")
            console.log(this.pie);
            this.pie.destroy();
        });
    }

}