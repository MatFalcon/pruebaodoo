/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class ClickerSystray extends Component {
  static template = "awesome_clicker.ClickerSystray";
  static components = { ClickerValue, Dropdown, DropdownItem };

  setup() {
    this.clicker = useClicker();
    this.actionService = useService("action");
  }

  openClickerView = () =>
    this.actionService.doAction({
      type: "ir.actions.client",
      tag: "awesome_clicker.client_action",
      target: "new",
      name: "Clicker",
    });

  increment = () => this.clicker.increment(9);

  get numberTrees() {
    return Object.keys(this.clicker.trees).reduce(
      (acc, tree) => acc + this.clicker.trees[tree].purchased,
      0
    );
  }

  get numberFruits() {
    return Object.keys(this.clicker.fruits).reduce(
      (acc, fruit) => acc + this.clicker.fruits[fruit],
      0
    );
  }
}

export const systrayItem = {
  Component: ClickerSystray,
};
registry
  .category("systray")
  .add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
