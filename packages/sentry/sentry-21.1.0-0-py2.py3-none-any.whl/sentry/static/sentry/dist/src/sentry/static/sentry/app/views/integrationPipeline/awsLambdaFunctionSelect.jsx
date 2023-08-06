import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addLoadingMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
var getLabel = function (func) { return func.FunctionName + " - " + func.Runtime; };
var AwsLambdaFunctionSelect = /** @class */ (function (_super) {
    __extends(AwsLambdaFunctionSelect, _super);
    function AwsLambdaFunctionSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new FormModel({ apiOptions: { baseUrl: window.location.origin } });
        _this.handlePreSubmit = function () { return addLoadingMessage(t('Submitting\u2026')); };
        _this.render = function () {
            var model = _this.model;
            var formFields = {
                title: t('Select the lambda functions to install Sentry on'),
                fields: _this.lambdaFunctions.map(function (func) {
                    return {
                        name: func.FunctionName,
                        type: 'boolean',
                        required: false,
                        label: getLabel(func),
                    };
                }),
            };
            return (<StyledForm initialData={_this.initialData} skipPreventDefault model={model} apiEndpoint="/extensions/aws_lambda/setup/" onPreSubmit={_this.handlePreSubmit}>
        <JsonForm forms={[formFields]}/>
      </StyledForm>);
        };
        return _this;
    }
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "initialData", {
        get: function () {
            var lambdaFunctions = this.props.lambdaFunctions;
            var initialData = lambdaFunctions.reduce(function (accum, func) {
                accum[func.FunctionName] = true;
                return accum;
            }, {});
            return initialData;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "lambdaFunctions", {
        get: function () {
            return this.props.lambdaFunctions.sort(function (a, b) {
                return getLabel(a).toLowerCase() < getLabel(b).toLowerCase() ? -1 : 1;
            });
        },
        enumerable: false,
        configurable: true
    });
    return AwsLambdaFunctionSelect;
}(React.Component));
export default AwsLambdaFunctionSelect;
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 50px;\n  padding-bottom: 50px;\n"], ["\n  margin: 50px;\n  padding-bottom: 50px;\n"])));
var templateObject_1;
//# sourceMappingURL=awsLambdaFunctionSelect.jsx.map