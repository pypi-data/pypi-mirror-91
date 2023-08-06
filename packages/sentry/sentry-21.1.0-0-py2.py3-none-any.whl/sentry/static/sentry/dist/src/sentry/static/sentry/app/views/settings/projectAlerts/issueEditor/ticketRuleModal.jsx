import { __assign, __extends, __makeTemplateObject, __read, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import AbstractExternalIssueForm from 'app/components/externalIssues/abstractExternalIssueForm';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
var TicketRuleModal = /** @class */ (function (_super) {
    __extends(TicketRuleModal, _super);
    function TicketRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleReceiveIntegrationDetails = function (integrationDetails) {
            _this.setState({
                issueConfigFieldsCache: integrationDetails[_this.getConfigName()],
            });
        };
        /**
         * Get a list of formFields names with valid config data.
         */
        _this.getValidAndSavableFieldNames = function () {
            var issueConfigFieldsCache = _this.state.issueConfigFieldsCache;
            return (issueConfigFieldsCache || [])
                .filter(function (field) { return field.hasOwnProperty('name'); })
                .map(function (field) { return field.name; });
        };
        _this.getEndPointString = function () {
            var _a = _this.props, instance = _a.instance, organization = _a.organization;
            return "/organizations/" + organization.slug + "/integrations/" + instance.integration + "/";
        };
        /**
         * Clean up the form data before saving it to state.
         */
        _this.cleanData = function (data) {
            var e_1, _a;
            var instance = _this.props.instance;
            var issueConfigFieldsCache = _this.state.issueConfigFieldsCache;
            var names = _this.getValidAndSavableFieldNames();
            var formData = {};
            if (instance === null || instance === void 0 ? void 0 : instance.hasOwnProperty('integration')) {
                formData.integration = instance.integration;
            }
            formData.dynamic_form_fields = issueConfigFieldsCache;
            try {
                for (var _b = __values(Object.entries(data)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), key = _d[0], value = _d[1];
                    if (names.includes(key)) {
                        formData[key] = value;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return formData;
        };
        _this.onFormSubmit = function (data, _success, _error, e, model) {
            var _a = _this.props, onSubmitAction = _a.onSubmitAction, closeModal = _a.closeModal;
            var fetchedFieldOptionsCache = _this.state.fetchedFieldOptionsCache;
            // This is a "fake form", so don't actually POST to an endpoint.
            e.preventDefault();
            e.stopPropagation();
            if (model.validateForm()) {
                onSubmitAction(_this.cleanData(data), fetchedFieldOptionsCache);
                addSuccessMessage(t('Changes applied.'));
                closeModal();
            }
        };
        _this.updateFetchedFieldOptionsCache = function (field, result) {
            var fetchedFieldOptionsCache = result.options.map(function (obj) { return [obj.value, obj.label]; });
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, "fetchedFieldOptionsCache[" + field.name + "]", fetchedFieldOptionsCache);
                return newState;
            });
        };
        _this.getFormProps = function () {
            var closeModal = _this.props.closeModal;
            return __assign(__assign({}, _this.getDefaultFormProps()), { cancelLabel: t('Close'), onCancel: closeModal, onSubmit: _this.onFormSubmit, submitLabel: t('Apply Changes') });
        };
        /**
         * Set the initial data from the Rule, replace `title` and `description` with
         * disabled inputs, and use the cached dynamic choices.
         */
        _this.cleanFields = function () {
            var instance = _this.props.instance;
            var _a = _this.state, fetchedFieldOptionsCache = _a.fetchedFieldOptionsCache, integrationDetails = _a.integrationDetails;
            var fields = [
                {
                    name: 'title',
                    label: 'Title',
                    type: 'string',
                    default: 'This will be the same as the Sentry Issue.',
                    disabled: true,
                },
                {
                    name: 'description',
                    label: 'Description',
                    type: 'string',
                    default: 'This will be generated from the Sentry Issue details.',
                    disabled: true,
                },
            ];
            var configsFromAPI = (integrationDetails || {})[_this.getConfigName()];
            return fields.concat((configsFromAPI || [])
                // Skip fields if they already exist.
                .filter(function (field) { return !fields.map(function (f) { return f.name; }).includes(field.name); })
                .map(function (field) {
                // Overwrite defaults from cache.
                if (instance.hasOwnProperty(field.name)) {
                    field.default = instance[field.name] || field.default;
                }
                // Overwrite choices from cache.
                if (fetchedFieldOptionsCache === null || fetchedFieldOptionsCache === void 0 ? void 0 : fetchedFieldOptionsCache.hasOwnProperty(field.name)) {
                    field.choices = fetchedFieldOptionsCache[field.name];
                }
                return field;
            }));
        };
        _this.renderBodyText = function () {
            // `ticketType` already includes indefinite article.
            var _a = _this.props, ticketType = _a.ticketType, link = _a.link;
            return (<BodyText>
        {tct('When this alert is triggered [ticketType] will be ' +
                'created with the following fields. It will also [linkToDocs] ' +
                'with the new Sentry Issue.', {
                linkToDocs: <ExternalLink href={link}>{t('stay in sync')}</ExternalLink>,
                ticketType: ticketType,
            })}
      </BodyText>);
        };
        return _this;
    }
    TicketRuleModal.prototype.getDefaultState = function () {
        var instance = this.props.instance;
        var issueConfigFieldsCache = Object.values((instance === null || instance === void 0 ? void 0 : instance.dynamic_form_fields) || {});
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { fetchedFieldOptionsCache: Object.fromEntries(issueConfigFieldsCache.map(function (field) { return [
                field.name,
                field.choices,
            ]; })), issueConfigFieldsCache: issueConfigFieldsCache });
    };
    TicketRuleModal.prototype.getEndpoints = function () {
        var _a = this.props, instance = _a.instance, organization = _a.organization;
        var query = (instance.dynamic_form_fields || [])
            .filter(function (field) { return field.updatesForm; })
            .filter(function (field) { return instance.hasOwnProperty(field.name); })
            .reduce(function (accumulator, _a) {
            var name = _a.name;
            accumulator[name] = instance[name];
            return accumulator;
        }, { action: 'create' });
        return [
            [
                'integrationDetails',
                "/organizations/" + organization.slug + "/integrations/" + instance.integration + "/",
                { query: query },
            ],
        ];
    };
    TicketRuleModal.prototype.render = function () {
        return this.renderForm(this.cleanFields());
    };
    return TicketRuleModal;
}(AbstractExternalIssueForm));
var BodyText = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
export default TicketRuleModal;
var templateObject_1;
//# sourceMappingURL=ticketRuleModal.jsx.map