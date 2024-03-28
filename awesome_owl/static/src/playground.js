/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
    
    setup() {
        this.html = markup(`<div class="text-primary">some content</div>`);
        this.sum = useState({value: 0});
    }

    incrementSum() {
        this.sum.value++;
    }
}
