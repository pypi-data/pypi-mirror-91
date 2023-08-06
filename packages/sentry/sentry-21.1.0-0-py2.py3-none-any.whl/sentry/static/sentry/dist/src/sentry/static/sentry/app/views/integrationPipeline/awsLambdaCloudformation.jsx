import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as qs from 'query-string';
import { addErrorMessage, addLoadingMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import { uniqueId } from 'app/utils/guid';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
// let the browser generate and store the external ID
// this way the same user always has the same external ID if they restart the pipeline
var ID_NAME = 'AWS_EXTERNAL_ID';
var getAwsExternalId = function () {
    var awsExternalId = window.localStorage.getItem(ID_NAME);
    if (!awsExternalId) {
        awsExternalId = uniqueId();
        window.localStorage.setItem(ID_NAME, awsExternalId);
    }
    return awsExternalId;
};
var AwsLambdaCloudformation = /** @class */ (function (_super) {
    __extends(AwsLambdaCloudformation, _super);
    function AwsLambdaCloudformation() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new FormModel();
        _this.handleSubmit = function (data) {
            addLoadingMessage(t('Submitting\u2026'));
            _this.model.setFormSaving();
            var origin = window.location.origin;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            var newUrl = origin + "/extensions/aws_lambda/setup/?" + qs.stringify(data);
            window.location.assign(newUrl);
        };
        _this.renderFormHeader = function () {
            var cloudformationUrl = _this.cloudformationUrl;
            var acklowedgeResource = (<strong>
        {t('I Acknowledge that AWS CloudFormation might create IAM resources')}
      </strong>);
            var create = <strong>{t('Create')}</strong>;
            var arnStrong = <strong>ARN</strong>;
            var sentryMonitoringStack = <strong>SentryMonitoringStack</strong>;
            return (<InstructionWrapper>
        <ol>
          <li>
            <ExternalLink href={cloudformationUrl}>
              {t("Add Sentry's Cloudfromation stack to your AWS")}
            </ExternalLink>
          </li>
          <li>
            {tct('Mark "[acklowedgeResource]"', {
                acklowedgeResource: acklowedgeResource,
            })}
          </li>
          <li>
            {tct('Press "[create]"', {
                create: create,
            })}
          </li>
          <li>
            {tct('It might take a minute or two for the CloudFormation stack to set up. Find the stack in list of stacks and copy the "[arnStrong]" value of "[sentryMonitoringStack]" into the input below:', {
                arnStrong: arnStrong,
                sentryMonitoringStack: sentryMonitoringStack,
            })}
          </li>
        </ol>
      </InstructionWrapper>);
        };
        _this.render = function () {
            var model = _this.model;
            var formFields = {
                title: t('Install Sentry to your AWS account'),
                fields: [
                    {
                        name: 'awsExternalId',
                        type: 'hidden',
                        required: true,
                    },
                    {
                        name: 'arn',
                        type: 'text',
                        required: true,
                        label: t('ARN'),
                        inline: false,
                        placeholder: 'arn:aws:iam::XXXXXXXXXXXX:stack/SentryMonitoringStack-XXXXXXXXXXXXX',
                        validate: function (_a) {
                            var id = _a.id, form = _a.form;
                            var value = form[id];
                            // validate the ARN matches a cloudformation stack
                            return /arn:aws:cloudformation:\S+:\d+:stack+\/\S+/.test(value)
                                ? []
                                : [[id, 'Invalid ARN']];
                        },
                    },
                ],
            };
            return (<StyledForm initialData={_this.initialData} model={model} onSubmit={_this.handleSubmit}>
        <JsonForm renderHeader={_this.renderFormHeader} forms={[formFields]}/>
      </StyledForm>);
        };
        return _this;
    }
    AwsLambdaCloudformation.prototype.componentDidMount = function () {
        // show the error if we have it
        var error = this.props.error;
        if (error) {
            addErrorMessage(error, { duration: 10000 });
        }
    };
    Object.defineProperty(AwsLambdaCloudformation.prototype, "initialData", {
        get: function () {
            var arn = this.props.arn;
            var awsExternalId = getAwsExternalId();
            return {
                awsExternalId: awsExternalId,
                arn: arn,
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaCloudformation.prototype, "cloudformationUrl", {
        get: function () {
            // generarate the cloudformation URL using the params we get from the server
            // and the external id we generate
            var _a = this.props, baseCloudformationUrl = _a.baseCloudformationUrl, templateUrl = _a.templateUrl, stackName = _a.stackName;
            var awsExternalId = getAwsExternalId();
            var query = qs.stringify({
                templateURL: templateUrl,
                stackName: stackName,
                param_ExternalId: awsExternalId,
            });
            return baseCloudformationUrl + "?" + query;
        },
        enumerable: false,
        configurable: true
    });
    return AwsLambdaCloudformation;
}(React.Component));
export default AwsLambdaCloudformation;
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 50px;\n  padding-bottom: 50px;\n"], ["\n  margin: 50px;\n  padding-bottom: 50px;\n"])));
var InstructionWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 20px;\n"], ["\n  margin: 20px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=awsLambdaCloudformation.jsx.map