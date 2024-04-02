/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem }

    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.rpcResult = {}

        onWillStart(
            async () => {
                const result = await this.rpc("/awesome_dashboard/statistics/");
                this.rpcResult = result;
            });
    }

    actionCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    actionLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "All leads",
            res_model: 'crm.lead',
            views: [
                [false, 'tree'],
                [false, 'form']
            ],
        });
    }
    
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
