import { t } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { getVitalDetailTableMehStatusFunction, getVitalDetailTablePoorStatusFunction, vitalNameFromLocation, } from './vitalDetail/utils';
export var DEFAULT_STATS_PERIOD = '24h';
export var COLUMN_TITLES = [
    'transaction',
    'project',
    'tpm',
    'p50',
    'p95',
    'failure rate',
    'apdex',
    'users',
    'user misery',
];
export function getAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, 'apdex'),
            value: "apdex(" + organization.apdexThreshold + ")",
            label: t('Apdex'),
        },
        {
            tooltip: getTermHelp(organization, 'tpm'),
            value: 'tpm()',
            label: t('Transactions Per Minute'),
        },
        {
            tooltip: getTermHelp(organization, 'failureRate'),
            value: 'failure_rate()',
            label: t('Failure Rate'),
        },
        {
            tooltip: getTermHelp(organization, 'p50'),
            value: 'p50()',
            label: t('p50 Duration'),
        },
        {
            tooltip: getTermHelp(organization, 'p95'),
            value: 'p95()',
            label: t('p95 Duration'),
        },
        {
            tooltip: getTermHelp(organization, 'p99'),
            value: 'p99()',
            label: t('p99 Duration'),
        },
    ];
}
export function getFrontendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, 'lcp'),
            value: "p75(lcp)",
            label: t('LCP p75'),
        },
        {
            tooltip: getTermHelp(organization, 'lcp'),
            value: 'lcp_distribution',
            label: t('LCP Distribution'),
        },
    ];
}
var PERFORMANCE_TERMS = {
    apdex: function () {
        return t('Apdex is the ratio of both satisfactory and tolerable response times to all response times.');
    },
    tpm: function () { return t('TPM is the number of recorded transaction events per minute.'); },
    failureRate: function () {
        return t('Failure rate is the percentage of recorded transactions that had a known and unsuccessful status.');
    },
    p50: function () { return t('p50 indicates the duration that 50% of transactions are faster than.'); },
    p95: function () { return t('p95 indicates the duration that 95% of transactions are faster than.'); },
    p99: function () { return t('p99 indicates the duration that 99% of transactions are faster than.'); },
    lcp: function () {
        return t('Largest contentful paint (LCP) is a web vital meant to represent user load times');
    },
    userMisery: function (organization) {
        return t("User misery is the percentage of users who are experiencing load times 4x your organization's apdex threshold of %sms.", organization.apdexThreshold);
    },
    statusBreakdown: function () {
        return t('The breakdown of transaction statuses. This may indicate what type of failure it is.');
    },
};
export function getTermHelp(organization, term) {
    if (!PERFORMANCE_TERMS.hasOwnProperty(term)) {
        return '';
    }
    return PERFORMANCE_TERMS[term](organization);
}
export function generatePerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'tpm()',
            'p50()',
            'p95()',
            'failure_rate()',
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort) || '-tpm';
    var searchQuery = decodeScalar(query.query) || '';
    var conditions = tokenizeSearch(searchQuery);
    conditions.setTagValues('event.type', ['transaction']);
    conditions.setTagValues('transaction.duration', ['<15m']);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    return EventView.fromNewQueryWithLocation(savedQuery, location);
}
export function generateFrontendPerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'tpm()',
            'p75(measurements.fcp)',
            'p75(measurements.lcp)',
            'p75(measurements.fid)',
            'p75(measurements.cls)',
            'count_unique(user)',
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort) || '-tpm';
    var searchQuery = decodeScalar(query.query) || '';
    var conditions = tokenizeSearch(searchQuery);
    conditions.setTagValues('event.type', ['transaction']);
    conditions.setTagValues('transaction.duration', ['<15m']);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    return EventView.fromNewQueryWithLocation(savedQuery, location);
}
export function generatePerformanceVitalDetailView(_organization, location) {
    var query = location.query;
    var vitalName = vitalNameFromLocation(location);
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Vitals Performance Details'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'count_unique(user)',
            'count()',
            "p50(" + vitalName + ")",
            "p75(" + vitalName + ")",
            "p95(" + vitalName + ")",
            getVitalDetailTablePoorStatusFunction(vitalName),
            getVitalDetailTableMehStatusFunction(vitalName),
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort) || "-count";
    var searchQuery = decodeScalar(query.query) || '';
    var conditions = tokenizeSearch(searchQuery);
    conditions.setTagValues('has', [vitalName]);
    conditions.setTagValues('event.type', ['transaction']);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    return EventView.fromNewQueryWithLocation(savedQuery, location);
}
//# sourceMappingURL=data.jsx.map