import { __assign, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import BarChart from 'app/components/charts/barChart';
import BarChartZoom from 'app/components/charts/barChartZoom';
import LoadingPanel from 'app/components/charts/loadingPanel';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getDuration } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { DoubleHeaderContainer, HeaderTitleLegend } from '../styles';
import HistogramQuery from '../transactionVitals/histogramQuery';
var NUM_BUCKETS = 50;
var PRECISION = 0;
function getBucketWidth(chartData) {
    // We can assume that all buckets are of equal width, use the first two
    // buckets to get the width. The value of each histogram function indicates
    // the beginning of the bucket.
    return chartData.length >= 2 ? chartData[1].bin - chartData[0].bin : 0;
}
function computeBuckets(chartData) {
    var bucketWidth = getBucketWidth(chartData);
    return chartData.map(function (item) {
        var bucket = item.bin;
        return {
            start: bucket,
            end: bucket + bucketWidth,
        };
    });
}
function formatDuration(duration) {
    if (duration <= 1000) {
        return getDuration(duration / 1000, 2, true);
    }
    return getDuration(duration / 1000, 3, true);
}
function getSeries(chartData) {
    var bucketWidth = getBucketWidth(chartData);
    var seriesData = chartData.map(function (item) {
        var bucket = item.bin;
        var midPoint = bucketWidth > 1 ? Math.ceil(bucket + bucketWidth / 2) : bucket;
        var name = formatDuration(midPoint);
        var value = item.count;
        return {
            value: value,
            name: name,
        };
    });
    return {
        seriesName: t('Count'),
        data: seriesData,
    };
}
export function HistogramChart(props) {
    var location = props.location, organization = props.organization, eventView = props.eventView, field = props.field, title = props.title, titleTooltip = props.titleTooltip;
    var xAxis = {
        type: 'category',
        truncate: true,
        boundaryGap: false,
        axisTick: {
            alignWithLabel: true,
        },
    };
    var handleZoomChange = function (start, end) {
        var queryString = decodeScalar(location.query.query);
        var conditions = tokenizeSearch(queryString || '');
        conditions.setTagValues(field, [">=" + start, "<=" + end]);
        var query = stringifyQueryObject(conditions);
        browserHistory.push({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { query: String(query).trim() }),
        });
    };
    return (<HistogramContainer>
      <HistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={[field]} dataFilter="exclude_outliers">
        {function (results) {
        var _a;
        var loading = results.isLoading;
        var errored = results.error !== null;
        var chartData = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[field];
        if (loading) {
            return (<LoadingPanel height="250px" data-test-id="histogram-request-loading"/>);
        }
        if (!chartData) {
            return null;
        }
        var series = getSeries(chartData);
        var allSeries = [];
        if (!loading && !errored) {
            allSeries.push(series);
        }
        var values = series.data.map(function (point) { return point.value; });
        var max = values.length ? Math.max.apply(Math, __spread(values)) : undefined;
        var yAxis = {
            type: 'value',
            max: max,
            axisLabel: {
                color: theme.chartLabel,
            },
        };
        return (<React.Fragment>
              <DoubleHeaderContainer>
                <HeaderTitleLegend>
                  {title}
                  <QuestionTooltip position="top" size="sm" title={titleTooltip}/>
                </HeaderTitleLegend>
              </DoubleHeaderContainer>
              <BarChartZoom minZoomWidth={Math.pow(10, -PRECISION) * NUM_BUCKETS} location={location} paramStart={field + ":>="} paramEnd={field + ":<="} xAxisIndex={[0]} buckets={computeBuckets(chartData)} onHistoryPush={handleZoomChange}>
                {function (zoomRenderProps) { return (<BarChartContainer>
                    <BarChart height={250} series={allSeries} xAxis={xAxis} yAxis={yAxis} grid={{
            left: space(3),
            right: space(3),
            top: space(3),
            bottom: space(1.5),
        }} stacked {...zoomRenderProps}/>
                  </BarChartContainer>); }}
              </BarChartZoom>
            </React.Fragment>);
    }}
      </HistogramQuery>
    </HistogramContainer>);
}
var HistogramContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var BarChartContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1));
export default HistogramChart;
var templateObject_1, templateObject_2;
//# sourceMappingURL=histogramChart.jsx.map