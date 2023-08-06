import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import Hovercard, { Body } from 'app/components/hovercard';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
var StacktracePreview = /** @class */ (function (_super) {
    __extends(StacktracePreview, _super);
    function StacktracePreview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            loadingVisible: false,
        };
        _this.loaderTimeout = null;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, issueId, event_1, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (this.state.event) {
                            return [2 /*return*/];
                        }
                        this.loaderTimeout = window.setTimeout(function () {
                            _this.setState({ loadingVisible: true });
                        }, 1000);
                        _a = this.props, api = _a.api, issueId = _a.issueId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 2:
                        event_1 = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ event: event_1, loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleStacktracePreviewClick = function (event) {
            event.stopPropagation();
            event.preventDefault();
        };
        return _this;
    }
    StacktracePreview.prototype.renderHovercardBody = function (stacktrace) {
        var _a;
        var _b = this.state, event = _b.event, loading = _b.loading, loadingVisible = _b.loadingVisible;
        if (loading && loadingVisible) {
            return (<NoStackTraceWrapper>
          <LoadingIndicator hideMessage size={48}/>
        </NoStackTraceWrapper>);
        }
        if (loading) {
            return null;
        }
        if (!stacktrace) {
            return (<NoStackTraceWrapper onClick={this.handleStacktracePreviewClick}>
          {t("There's no stack trace available for this issue.")}
        </NoStackTraceWrapper>);
        }
        if (event) {
            trackAnalyticsEvent({
                eventKey: 'stacktrace.preview.open',
                eventName: 'Stack Trace Preview: Open',
                organization_id: parseInt(this.props.organization.id, 10),
                issue_id: this.props.issueId,
            });
            return (<div onClick={this.handleStacktracePreviewClick}>
          <StacktraceContent data={stacktrace} expandFirstFrame={false} includeSystemFrames={stacktrace.frames.every(function (frame) { return !frame.inApp; })} platform={((_a = event.platform) !== null && _a !== void 0 ? _a : 'other')} newestFirst={isStacktraceNewestFirst()} event={event} isHoverPreviewed/>
        </div>);
        }
        return null;
    };
    StacktracePreview.prototype.render = function () {
        var _a, _b, _c, _d, _e, _f;
        var _g = this.props, children = _g.children, organization = _g.organization, disablePreview = _g.disablePreview;
        var exceptionsWithStacktrace = (_d = (_c = (_b = (_a = this.state.event) === null || _a === void 0 ? void 0 : _a.entries.find(function (e) { return e.type === 'exception'; })) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values.filter(function (_a) {
            var stacktrace = _a.stacktrace;
            return defined(stacktrace);
        })) !== null && _d !== void 0 ? _d : [];
        var stacktrace = isStacktraceNewestFirst()
            ? (_e = exceptionsWithStacktrace[exceptionsWithStacktrace.length - 1]) === null || _e === void 0 ? void 0 : _e.stacktrace : (_f = exceptionsWithStacktrace[0]) === null || _f === void 0 ? void 0 : _f.stacktrace;
        if (!organization.features.includes('stacktrace-hover-preview') || disablePreview) {
            return children;
        }
        return (<span onMouseEnter={this.fetchData}>
        <StyledHovercard body={this.renderHovercardBody(stacktrace)} position="right" modifiers={{
            flip: {
                enabled: false,
            },
            preventOverflow: {
                padding: 20,
                enabled: true,
                boundariesElement: 'viewport',
            },
        }}>
          {children}
        </StyledHovercard>
      </span>);
    };
    return StacktracePreview;
}(React.Component));
var StyledHovercard = styled(Hovercard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 700px;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  width: 700px;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), Body, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[2]; });
var NoStackTraceWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 80px;\n"], ["\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 80px;\n"])), function (p) { return p.theme.gray400; }, space(1.5));
export default withApi(StacktracePreview);
var templateObject_1, templateObject_2;
//# sourceMappingURL=stacktracePreview.jsx.map