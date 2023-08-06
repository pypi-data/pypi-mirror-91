import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import _Footer from '../charts/footer';
import { getFrontendAxisOptions } from '../data';
import DurationChart from './durationChart';
import HistogramChart from './histogramChart';
function FrontendDisplay(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization;
    var onFilterChange = function (minValue, maxValue, tagName) {
        var conditions = tokenizeSearch('');
        conditions.setTagValues(tagName, [
            ">=" + Math.round(minValue),
            "<" + Math.round(maxValue),
        ]);
        var query = stringifyQueryObject(conditions);
        props.onFrontendDisplayFilter(query);
    };
    var axisOptions = getFrontendAxisOptions(organization);
    var leftAxis = axisOptions[0].value; // TODO: Temporary until backend changes
    var rightAxis = axisOptions[1].value; // TODO: Temporary until backend changes
    return (<Panel>
      <DoubleChartContainer>
        <DurationChart field="p75(measurements.lcp)" eventView={eventView} organization={organization} title={t('LCP p75')} titleTooltip={t('This is the 75th percentile over time of the largest contentful paint, a web vital meant to represent user load times')}/>
        <HistogramChart field="measurements.lcp" {...props} onFilterChange={onFilterChange} title={t('LCP Distribution')} titleTooltip={t('This is a histogram of the largest contentful paint, a web vital meant to represent user load times')}/>
      </DoubleChartContainer>

      <Footer options={getFrontendAxisOptions(organization)} leftAxis={leftAxis} rightAxis={rightAxis} organization={organization} eventView={eventView} location={location}/>
    </Panel>);
}
var DoubleChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"])), space(3));
var Footer = withApi(_Footer);
export default FrontendDisplay;
var templateObject_1;
//# sourceMappingURL=frontendDisplay.jsx.map