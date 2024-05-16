import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import { BlockUI} from "@web/core/ui/block_ui";
import { session } from "@web/session";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
    if (action.report_type === 'xlsx') {
        BlockUI;
        var def = $.Deferred();
        await download({
            url: '/xlsx_reports',
            data: action.data,
            success: def.resolve.bind(def),
            error: (error) => this.call('crash manager', 'rpc_error', error),
            complete: () => unblockUI,
        });
    }
});