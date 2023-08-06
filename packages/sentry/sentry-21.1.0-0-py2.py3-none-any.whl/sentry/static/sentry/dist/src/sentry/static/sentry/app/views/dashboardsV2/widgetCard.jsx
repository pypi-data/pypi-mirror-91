import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import BarChart from 'app/components/charts/barChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getSeriesSelection } from 'app/components/charts/utils';
import ErrorBoundary from 'app/components/errorBoundary';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconDelete, IconEdit, IconGrabbable, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { getAggregateArg, getMeasurementSlug } from 'app/utils/discover/fields';
import getDynamicText from 'app/utils/getDynamicText';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import { ChartContainer, HeaderTitleLegend } from '../performance/styles';
import WidgetQueries from './widgetQueries';
var WidgetCard = /** @class */ (function (_super) {
    __extends(WidgetCard, _super);
    function WidgetCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCard.prototype.shouldComponentUpdate = function (nextProps) {
        if (!isEqual(nextProps.widget, this.props.widget) ||
            !isEqual(nextProps.selection, this.props.selection) ||
            this.props.isEditing !== nextProps.isEditing ||
            this.props.isDragging !== nextProps.isDragging ||
            this.props.hideToolbar !== nextProps.hideToolbar) {
            return true;
        }
        return false;
    };
    WidgetCard.prototype.chartComponent = function (chartProps) {
        var widget = this.props.widget;
        switch (widget.displayType) {
            case 'bar':
                return <BarChart {...chartProps}/>;
            case 'line':
            default:
                return <LineChart {...chartProps}/>;
        }
    };
    WidgetCard.prototype.renderVisual = function (_a) {
        var _this = this;
        var _b, _c, _d;
        var results = _a.results, errorMessage = _a.errorMessage, loading = _a.loading;
        var _e = this.props, location = _e.location, router = _e.router, selection = _e.selection, widget = _e.widget;
        var _f = selection.datetime, start = _f.start, end = _f.end, period = _f.period;
        var legend = {
            right: 10,
            top: 5,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            type: 'plain',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
            selected: getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
        };
        var axisField = (_d = (_c = (_b = widget.queries[0]) === null || _b === void 0 ? void 0 : _b.fields) === null || _c === void 0 ? void 0 : _c[0]) !== null && _d !== void 0 ? _d : 'count()';
        var chartOptions = {
            grid: {
                left: '0px',
                right: '0px',
                top: '40px',
                bottom: '10px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return axisLabelFormatter(value, axisField); },
                },
            },
        };
        return (<ChartZoom router={router} period={period} start={start} end={end}>
        {function (zoomRenderProps) {
            if (errorMessage) {
                return (<ErrorPanel>
                <IconWarning color="gray500" size="lg"/>
              </ErrorPanel>);
            }
            var colors = results ? theme.charts.getColorPalette(results.length - 2) : [];
            // Create a list of series based on the order of the fields,
            var series = results
                ? results.map(function (values, i) { return (__assign(__assign({}, values), { color: colors[i] })); })
                : [];
            return (<TransitionChart loading={loading} reloading={loading}>
              <TransparentLoadingMask visible={loading}/>
              {getDynamicText({
                value: _this.chartComponent(__assign(__assign(__assign({}, zoomRenderProps), chartOptions), { legend: legend,
                    series: series })),
                fixed: 'Widget Chart',
            })}
            </TransitionChart>);
        }}
      </ChartZoom>);
    };
    WidgetCard.prototype.renderToolbar = function () {
        if (!this.props.isEditing) {
            return null;
        }
        if (this.props.hideToolbar) {
            return <ToolbarPanel />;
        }
        var _a = this.props, onEdit = _a.onEdit, onDelete = _a.onDelete, startWidgetDrag = _a.startWidgetDrag;
        return (<ToolbarPanel>
        <IconContainer data-component="icon-container">
          <StyledIconGrabbable color="gray500" size="md" onMouseDown={function (event) { return startWidgetDrag(event); }} onTouchStart={function (event) { return startWidgetDrag(event); }}/>
          <IconClick data-test-id="widget-edit" onClick={function () {
            onEdit();
        }}>
            <IconEdit color="gray500" size="md"/>
          </IconClick>
          <IconClick data-test-id="widget-delete" onClick={function () {
            onDelete();
        }}>
            <IconDelete color="gray500" size="md"/>
          </IconClick>
        </IconContainer>
      </ToolbarPanel>);
    };
    WidgetCard.prototype.render = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, isDragging = _a.isDragging, api = _a.api, organization = _a.organization, selection = _a.selection, renderErrorMessage = _a.renderErrorMessage;
        return (<ErrorBoundary customComponent={<ErrorCard>{t('Error loading widget data')}</ErrorCard>}>
        <StyledPanel isDragging={isDragging}>
          <WidgetQueries api={api} organization={organization} widget={widget} selection={selection}>
            {function (_a) {
            var results = _a.results, errorMessage = _a.errorMessage, loading = _a.loading;
            return (<React.Fragment>
                  {typeof renderErrorMessage === 'function'
                ? renderErrorMessage(errorMessage)
                : null}
                  <ChartContainer>
                    <HeaderTitleLegend>{widget.title}</HeaderTitleLegend>
                    {_this.renderVisual({ results: results, errorMessage: errorMessage, loading: loading })}
                    {_this.renderToolbar()}
                  </ChartContainer>
                </React.Fragment>);
        }}
          </WidgetQueries>
        </StyledPanel>
      </ErrorBoundary>);
    };
    return WidgetCard;
}(React.Component));
export default withApi(withOrganization(withGlobalSelection(ReactRouter.withRouter(WidgetCard))));
var ErrorCard = styled(Placeholder)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space(2));
var StyledPanel = styled(Panel, {
    shouldForwardProp: function (prop) { return prop !== 'isDragging'; },
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n  visibility: ", ";\n"], ["\n  margin: 0;\n  visibility: ", ";\n"])), function (p) { return (p.isDragging ? 'hidden' : 'visible'); });
var ToolbarPanel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  background-color: rgba(255, 255, 255, 0.5);\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  background-color: rgba(255, 255, 255, 0.5);\n"])));
var IconContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n\n  > * + * {\n    margin-left: 50px;\n  }\n"], ["\n  display: flex;\n\n  > * + * {\n    margin-left: 50px;\n  }\n"])));
var IconClick = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  &:hover {\n    cursor: pointer;\n  }\n"])));
var StyledIconGrabbable = styled(IconGrabbable)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  &:hover {\n    cursor: grab;\n  }\n"], ["\n  &:hover {\n    cursor: grab;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=widgetCard.jsx.map