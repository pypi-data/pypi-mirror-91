import { __makeTemplateObject } from "tslib";
import React from 'react';
import withRouter from 'react-router/lib/withRouter';
import styled from '@emotion/styled';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import LoadingPanel from 'app/components/charts/loadingPanel';
import { getInterval } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import space from 'app/styles/space';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import withApi from 'app/utils/withApi';
import Chart from '../charts/chart';
import { DoubleHeaderContainer, HeaderTitleLegend } from '../styles';
function DurationChart(props) {
    var organization = props.organization, api = props.api, eventView = props.eventView, location = props.location, router = props.router, field = props.field, title = props.title, titleTooltip = props.titleTooltip;
    // construct request parameters for fetching chart data
    var globalSelection = eventView.getGlobalSelection();
    var start = globalSelection.datetime.start
        ? getUtcToLocalDateObject(globalSelection.datetime.start)
        : undefined;
    var end = globalSelection.datetime.end
        ? getUtcToLocalDateObject(globalSelection.datetime.end)
        : undefined;
    var utc = getParams(location.query).utc;
    return (<EventsRequest organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} start={start} end={end} interval={getInterval({
        start: start || null,
        end: end || null,
        period: globalSelection.datetime.period,
    }, true)} showLoading={false} query={eventView.getEventsAPIPayload(location).query} includePrevious={false} yAxis={[field]}>
      {function (_a) {
        var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, timeseriesData = _a.timeseriesData;
        var results = timeseriesData;
        if (errored) {
            return (<ErrorPanel>
              <IconWarning color="gray300" size="lg"/>
            </ErrorPanel>);
        }
        return (<DurationChartContainer>
            <DoubleHeaderContainer>
              <HeaderTitleLegend>
                {title}
                <QuestionTooltip position="top" size="sm" title={titleTooltip}/>
              </HeaderTitleLegend>
            </DoubleHeaderContainer>
            {results ? (<ChartContainer>
                <Chart height={250} data={results} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} utc={utc === 'true'} grid={{
            left: space(3),
            right: space(3),
            top: space(3),
            bottom: space(1.5),
        }} disableMultiAxis/>
              </ChartContainer>) : (<LoadingPanel data-test-id="events-request-loading"/>)}
          </DurationChartContainer>);
    }}
    </EventsRequest>);
}
var DurationChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var ChartContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1));
export default withRouter(withApi(DurationChart));
var templateObject_1, templateObject_2;
//# sourceMappingURL=durationChart.jsx.map