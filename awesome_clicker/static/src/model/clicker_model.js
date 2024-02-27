/* @odoo-module */

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class Clicker extends Reactive {
  constructor() {
    super();
    this.setup();
  }

  setup() {
    this.count = 0;
    this.level = 0;
    this.bots = 0;
    this.eventBus = new EventBus();

    document.addEventListener("click", () => this.increment(1), true);
    setInterval(() => (this.count += 10 * this.bots), 10 * 1000);
  }

  increment(inc) {
    this.count += inc;
    if (this.count >= 1000 && this.level === 0) {
      this.eventBus.trigger("MILESTONE_1k");
      this.level++;
    }
  }

  buyBot() {
    if (this.count < 1000) return;

    this.bots += 1;
    this.count -= 1000;
  }
}
