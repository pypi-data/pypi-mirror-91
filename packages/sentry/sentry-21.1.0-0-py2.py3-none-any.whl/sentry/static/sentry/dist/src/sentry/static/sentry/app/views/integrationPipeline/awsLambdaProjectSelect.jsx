import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addLoadingMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
var AwsLambdaProjectSelect = /** @class */ (function (_super) {
    __extends(AwsLambdaProjectSelect, _super);
    function AwsLambdaProjectSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new FormModel();
        return _this;
    }
    AwsLambdaProjectSelect.prototype.render = function () {
        var _this = this;
        var projects = this.props.projects;
        var formFields = {
            title: t('Select a project to use for your AWS Lambda functions'),
            fields: [
                {
                    name: 'projectId',
                    type: 'sentry_project_selector',
                    required: true,
                    label: t('Project'),
                    inline: false,
                    projects: projects,
                },
            ],
        };
        var handleSubmit = function (_a) {
            var projectId = _a.projectId;
            addLoadingMessage(t('Submitting\u2026'));
            _this.model.setFormSaving();
            var origin = window.location.origin;
            // redirect to the extensions endpoint with the projectId as a query param
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            var newUrl = origin + "/extensions/aws_lambda/setup/?projectId=" + projectId;
            window.location.assign(newUrl);
        };
        // TODO: Add logic if no projects
        return (<StyledForm model={this.model} onSubmit={handleSubmit}>
        <JsonForm forms={[formFields]}/>
      </StyledForm>);
    };
    return AwsLambdaProjectSelect;
}(React.Component));
export default AwsLambdaProjectSelect;
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-width: 500px;\n  margin: 50px;\n"], ["\n  max-width: 500px;\n  margin: 50px;\n"])));
var templateObject_1;
//# sourceMappingURL=awsLambdaProjectSelect.jsx.map