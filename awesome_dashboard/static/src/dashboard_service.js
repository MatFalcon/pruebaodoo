// /** @odoo-module **/
// 
// import { memoize } from "@web/core/utils/functions";
// import { registry } from "@web/core/registry";
// 
// const statisticsService = {
// 	dependencies: ["rpc"],
// 	start(env, { rpc }) {
// 		return {mem_rpc: memoize(rpc)};
// 	},
// };
// 
// registry.category("services").add("awesome_dashboard.statistics", statisticsService);

/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
	dependencies: ["rpc"],
	async start(env, { rpc }) {
		let state = reactive({data: await rpc("awesome_dashboard/statistics")});
		setInterval(async () => {
			state.data = await rpc("awesome_dashboard/statistics");
		}, 3 * 1000);
		return state;
	},
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
