import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Card from 'app/components/card';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { decodeList } from 'app/utils/queryString';
import VitalsCardsDiscoverQuery from 'app/views/performance/vitalDetail/vitalsCardsDiscoverQuery';
import { HeaderTitle } from '../styles';
import ColorBar from '../vitalDetail/colorBar';
import { vitalAbbreviations, vitalDescription, vitalDetailRouteWithQuery, vitalMap, vitalsBaseFields, vitalsMehFields, vitalsP75Fields, vitalsPoorFields, VitalState, vitalStateColors, } from '../vitalDetail/utils';
import VitalPercents from '../vitalDetail/vitalPercents';
// Temporary list of platforms to only show web vitals for.
var VITALS_PLATFORMS = [
    'javascript',
    'javascript-react',
    'javascript-angular',
    'javascript-angularjs',
    'javascript-backbone',
    'javascript-ember',
    'javascript-gatsby',
    'javascript-vue',
];
export function FrontendCards(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, _a = props.frontendOnly, frontendOnly = _a === void 0 ? false : _a;
    if (frontendOnly) {
        var isFrontend = eventView.project.some(function (projectId) {
            var _a;
            return VITALS_PLATFORMS.includes(((_a = projects.find(function (project) { return project.id === "" + projectId; })) === null || _a === void 0 ? void 0 : _a.platform) || '');
        });
        if (!isFrontend) {
            return null;
        }
    }
    var vitals = [WebVital.FCP, WebVital.LCP, WebVital.FID, WebVital.CLS];
    return (<VitalsCardsDiscoverQuery eventView={eventView} location={location} orgSlug={organization.slug} vitals={vitals}>
      {function (_a) {
        var _b;
        var isLoading = _a.isLoading, tableData = _a.tableData;
        var result = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0];
        return (<VitalsContainer>
            {vitals.map(function (vital) {
            var _a, _b;
            var target = vitalDetailRouteWithQuery({
                orgSlug: organization.slug,
                query: eventView.generateQueryStringObject(),
                vitalName: vital,
                projectID: decodeList(location.query.project),
            });
            var value = isLoading ? '\u2014' : getP75(result, vital);
            var chart = (<VitalBar isLoading={isLoading} vital={vital} result={result}/>);
            return (<Link key={vital} to={target} data-test-id={"vitals-linked-card-" + vitalAbbreviations[vital]}>
                  <VitalCard title={(_a = vitalMap[vital]) !== null && _a !== void 0 ? _a : ''} tooltip={(_b = vitalDescription[vital]) !== null && _b !== void 0 ? _b : ''} value={isLoading ? '\u2014' : value} chart={chart}/>
                </Link>);
        })}
          </VitalsContainer>);
    }}
    </VitalsCardsDiscoverQuery>);
}
var VitalsContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
export function VitalBar(props) {
    var isLoading = props.isLoading, result = props.result, vital = props.vital, value = props.value, _a = props.showBar, showBar = _a === void 0 ? true : _a, _b = props.showStates, showStates = _b === void 0 ? false : _b, _c = props.showDurationDetail, showDurationDetail = _c === void 0 ? false : _c, _d = props.showVitalPercentNames, showVitalPercentNames = _d === void 0 ? false : _d;
    if (isLoading) {
        return showStates ? <Placeholder height="48px"/> : null;
    }
    var emptyState = showStates ? (<EmptyStateWarning small>{t('No data available')}</EmptyStateWarning>) : null;
    if (!result) {
        return emptyState;
    }
    var counts = {
        poorCount: 0,
        mehCount: 0,
        goodCount: 0,
        baseCount: 0,
    };
    var vitals = Array.isArray(vital) ? vital : [vital];
    vitals.forEach(function (vitalName) {
        var c = getCounts(result, vitalName);
        Object.keys(counts).forEach(function (countKey) { return (counts[countKey] += c[countKey]); });
    });
    if (!counts.baseCount) {
        return emptyState;
    }
    var p75 = Array.isArray(vital)
        ? null
        : value !== null && value !== void 0 ? value : getP75(result, vital);
    var percents = getPercentsFromCounts(counts);
    var colorStops = getColorStopsFromPercents(percents);
    return (<React.Fragment>
      {showBar && <ColorBar colorStops={colorStops}/>}
      <BarDetail>
        {showDurationDetail && p75 && (<div>
            {t('The p75 for all transactions is ')}
            <strong>{p75}</strong>
          </div>)}
        <VitalPercents percents={percents} showVitalPercentNames={showVitalPercentNames}/>
      </BarDetail>
    </React.Fragment>);
}
function VitalCard(props) {
    var chart = props.chart, title = props.title, tooltip = props.tooltip, value = props.value;
    return (<StyledCard interactive>
      <HeaderTitle>
        <OverflowEllipsis>{t(title)}</OverflowEllipsis>
        <QuestionTooltip size="sm" position="top" title={tooltip}/>
      </HeaderTitle>
      <CardValue>{value}</CardValue>
      {chart}
    </StyledCard>);
}
var StyledCard = styled(Card)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  min-height: 150px;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  min-height: 150px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.textColor; }, space(2), space(3), space(2));
function getP75(result, vitalName) {
    var _a;
    var p75 = (_a = result === null || result === void 0 ? void 0 : result[getAggregateAlias(vitalsP75Fields[vitalName])]) !== null && _a !== void 0 ? _a : null;
    if (p75 === null) {
        return '\u2014';
    }
    else {
        return vitalName === WebVital.CLS ? p75.toFixed(2) : p75.toFixed(0) + "ms";
    }
}
function getCounts(result, vitalName) {
    var base = result[getAggregateAlias(vitalsBaseFields[vitalName])];
    var poorCount = parseFloat(result[getAggregateAlias(vitalsPoorFields[vitalName])]) || 0;
    var mehTotal = parseFloat(result[getAggregateAlias(vitalsMehFields[vitalName])]) || 0;
    var mehCount = mehTotal - poorCount;
    var baseCount = parseFloat(base) || 0;
    var goodCount = baseCount - mehCount - poorCount;
    return {
        poorCount: poorCount,
        mehCount: mehCount,
        goodCount: goodCount,
        baseCount: baseCount,
    };
}
function getPercentsFromCounts(_a) {
    var poorCount = _a.poorCount, mehCount = _a.mehCount, goodCount = _a.goodCount, baseCount = _a.baseCount;
    var poorPercent = poorCount / baseCount;
    var mehPercent = mehCount / baseCount;
    var goodPercent = goodCount / baseCount;
    var percents = [
        {
            vitalState: VitalState.GOOD,
            percent: goodPercent,
        },
        {
            vitalState: VitalState.MEH,
            percent: mehPercent,
        },
        {
            vitalState: VitalState.POOR,
            percent: poorPercent,
        },
    ];
    return percents;
}
function getColorStopsFromPercents(percents) {
    return percents.map(function (_a) {
        var percent = _a.percent, vitalState = _a.vitalState;
        return ({
            percent: percent,
            color: vitalStateColors[vitalState],
        });
    });
}
var BarDetail = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"], ["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; });
var CardValue = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 32px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: 32px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(1), space(1.5));
var OverflowEllipsis = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=vitalsCards.jsx.map