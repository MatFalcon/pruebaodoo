/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * @returns {ClickerStore}
 */
export function useClickerService() {
    return useState(useService("awesome_clicker.clicker_service"));
}
