import { __assign } from "tslib";
import { statsPeriodToDays } from 'app/utils/dates';
import getCurrentSentryReactTransaction from 'app/utils/getCurrentSentryReactTransaction';
import { decodeScalar } from 'app/utils/queryString';
export function getPerformanceLandingUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/";
}
export function getTransactionSearchQuery(location, query) {
    if (query === void 0) { query = ''; }
    return String(decodeScalar(location.query.query) || query).trim();
}
export function getTransactionDetailsUrl(organization, eventSlug, transaction, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/" + eventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function getTransactionComparisonUrl(_a) {
    var organization = _a.organization, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug, transaction = _a.transaction, query = _a.query;
    return {
        pathname: "/organizations/" + organization.slug + "/performance/compare/" + baselineEventSlug + "/" + regressionEventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function addRoutePerformanceContext(selection) {
    var transaction = getCurrentSentryReactTransaction();
    var days = statsPeriodToDays(selection.datetime.period, selection.datetime.start, selection.datetime.end);
    var seconds = Math.floor(days * 86400);
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('statsPeriod', seconds.toString());
}
export function getTransactionName(location) {
    var transaction = location.query.transaction;
    return decodeScalar(transaction);
}
//# sourceMappingURL=utils.jsx.map