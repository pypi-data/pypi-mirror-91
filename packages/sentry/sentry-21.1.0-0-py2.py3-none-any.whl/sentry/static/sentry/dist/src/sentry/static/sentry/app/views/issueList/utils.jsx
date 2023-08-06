import { __read } from "tslib";
import { t } from 'app/locale';
export var Query;
(function (Query) {
    Query["NEEDS_REVIEW"] = "is:unresolved is:needs_review";
    Query["NEEDS_REVIEW_OWNER"] = "is:unresolved is:needs_review owner:me_or_none";
    Query["UNRESOLVED"] = "is:unresolved";
    Query["IGNORED"] = "is:ignored";
    Query["REPROCESSING"] = "is:reprocessing";
})(Query || (Query = {}));
/**
 * Get a list of currently active tabs
 */
export function getTabs(organization) {
    var tabs = [
        [
            Query.NEEDS_REVIEW_OWNER,
            {
                name: t('Needs Review'),
                analyticsName: 'needs_review',
                count: true,
                enabled: organization.features.includes('inbox-owners-query'),
            },
        ],
        [
            Query.NEEDS_REVIEW,
            {
                name: t('Needs Review'),
                analyticsName: 'needs_review',
                count: true,
                enabled: !organization.features.includes('inbox-owners-query'),
            },
        ],
        [
            Query.UNRESOLVED,
            {
                name: t('All Unresolved'),
                analyticsName: 'unresolved',
                count: true,
                enabled: true,
            },
        ],
        [
            Query.IGNORED,
            {
                name: t('Ignored'),
                analyticsName: 'ignored',
                count: true,
                enabled: true,
            },
        ],
        [
            Query.REPROCESSING,
            {
                name: t('Reprocessing'),
                analyticsName: 'reprocessing',
                count: true,
                enabled: organization.features.includes('reprocessing-v2'),
            },
        ],
    ];
    return tabs.filter(function (_a) {
        var _b = __read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.enabled;
    });
}
/**
 * @returns queries that should have counts fetched
 */
export function getTabsWithCounts(organization) {
    var tabs = getTabs(organization);
    return tabs.filter(function (_a) {
        var _b = __read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.count;
    }).map(function (_a) {
        var _b = __read(_a, 1), query = _b[0];
        return query;
    });
}
// the tab counts will look like 99+
export var TAB_MAX_COUNT = 99;
//# sourceMappingURL=utils.jsx.map