/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        onWillStart(async () => {
            this.result = await this.rpc("/awesome_dashboard/statistics");
        });
    }
    openCustomerList() {
        console.log('clicked');
        this.action.doAction("base.action_partner_form");
    }
    openLeadList() {
        console.log('clicked');
        this.action.doAction("crm.crm_lead_all_leads");
    }

    static components = { Layout, DashboardItem };
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
