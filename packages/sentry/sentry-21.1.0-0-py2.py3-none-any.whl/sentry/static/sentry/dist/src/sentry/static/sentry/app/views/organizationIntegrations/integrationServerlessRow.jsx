import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import Switch from 'app/components/switch';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import withApi from 'app/utils/withApi';
var IntegrationServerlessRow = /** @class */ (function (_super) {
    __extends(IntegrationServerlessRow, _super);
    function IntegrationServerlessRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.recordAction = function (action) {
            trackIntegrationEvent({
                eventKey: 'integrations.serverless_function_action',
                eventName: 'Integrations: Serverless Function Action',
                integration: _this.props.integration.provider.key,
                integration_type: 'first_party',
                action: action,
            }, _this.props.organization);
        };
        _this.toggleEnable = function () { return __awaiter(_this, void 0, void 0, function () {
            var action, data, resp, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        action = this.enabled ? 'disable' : 'enable';
                        data = {
                            action: action,
                            target: this.props.serverlessFunction.name,
                        };
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        addLoadingMessage();
                        this.recordAction(action);
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _a.sent();
                        this.props.onUpdateFunction(resp);
                        addSuccessMessage(t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        // TODO: specific error handling
                        addErrorMessage(t('An error ocurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.updateVersion = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, resp, err_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        data = {
                            action: 'updateVersion',
                            target: this.props.serverlessFunction.name,
                        };
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        addLoadingMessage();
                        this.recordAction('updateVersion');
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _a.sent();
                        this.props.onUpdateFunction(resp);
                        addSuccessMessage(t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _a.sent();
                        // TODO: specific error handling
                        addErrorMessage(t('An error ocurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Object.defineProperty(IntegrationServerlessRow.prototype, "enabled", {
        get: function () {
            return this.props.serverlessFunction.enabled;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationServerlessRow.prototype, "endpoint", {
        get: function () {
            var orgSlug = this.props.organization.slug;
            return "/organizations/" + orgSlug + "/integrations/" + this.props.integration.id + "/serverless-functions/";
        },
        enumerable: false,
        configurable: true
    });
    IntegrationServerlessRow.prototype.render = function () {
        var serverlessFunction = this.props.serverlessFunction;
        var versionDisplay = this.enabled ? serverlessFunction.version : 'None';
        return (<Item>
        <NameWrapper>{serverlessFunction.name}</NameWrapper>
        <RuntimeWrapper>{serverlessFunction.runtime}</RuntimeWrapper>
        <VersionWrapper>{versionDisplay}</VersionWrapper>
        <StyledSwitch isActive={this.enabled} size="sm" toggle={this.toggleEnable}/>
        {serverlessFunction.outOfDate && (<UpdateButton size="small" priority="primary" onClick={this.updateVersion}>
            Update
          </UpdateButton>)}
      </Item>);
    };
    return IntegrationServerlessRow;
}(React.Component));
export default withApi(IntegrationServerlessRow);
var Item = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr 0.25fr 0.5fr;\n  grid-template-areas: 'function-name runtime version enable-switch update-button';\n"], ["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr 0.25fr 0.5fr;\n  grid-template-areas: 'function-name runtime version enable-switch update-button';\n"])), space(1), function (p) { return p.theme.innerBorder; }, space(1));
var ItemWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var NameWrapper = styled(ItemWrapper)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-area: function-name;\n"], ["\n  grid-area: function-name;\n"])));
var RuntimeWrapper = styled(ItemWrapper)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-area: runtime;\n"], ["\n  grid-area: runtime;\n"])));
var VersionWrapper = styled(ItemWrapper)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-area: version;\n"], ["\n  grid-area: version;\n"])));
var StyledSwitch = styled(Switch)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  grid-area: enable-switch;\n"], ["\n  grid-area: enable-switch;\n"])));
var UpdateButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: update-button;\n"], ["\n  grid-area: update-button;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=integrationServerlessRow.jsx.map