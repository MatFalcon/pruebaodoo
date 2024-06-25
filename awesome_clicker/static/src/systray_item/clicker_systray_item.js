/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";
import { ClickValue } from "../click_value/click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static components = { ClickValue, Dropdown, DropdownItem };

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
        useExternalListener(
            document.body,
            "click",
            () => {
                this.clicker.increment(1);
            },
            { capture: true }
        );
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker",
        });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", { Component: ClickerSystrayItem });
