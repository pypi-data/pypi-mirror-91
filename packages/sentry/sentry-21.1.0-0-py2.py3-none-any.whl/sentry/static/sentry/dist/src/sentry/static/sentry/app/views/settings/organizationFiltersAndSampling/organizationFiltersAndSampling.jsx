import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import TransactionRules from './transactionRules';
var OrganizationFiltersAndSampling = /** @class */ (function (_super) {
    __extends(OrganizationFiltersAndSampling, _super);
    function OrganizationFiltersAndSampling() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddRule = function () {
            // TODO(Priscila): Implement the request here
        };
        return _this;
    }
    OrganizationFiltersAndSampling.prototype.getTitle = function () {
        return t('Filters & Sampling');
    };
    OrganizationFiltersAndSampling.prototype.render = function () {
        return (<React.Fragment>
        <SettingsPageHeader title={this.getTitle()}/>
        <PermissionAlert />
        <TextBlock>
          {t('Manage the inbound data you want to store. To change the sampling rate or rate limits, update your SDK configuration. The rules added below will apply on top of your SDK configuration.')}
        </TextBlock>
        <TransactionRules rules={[]} onAddRule={this.handleAddRule}/>
      </React.Fragment>);
    };
    return OrganizationFiltersAndSampling;
}(AsyncView));
export default OrganizationFiltersAndSampling;
//# sourceMappingURL=organizationFiltersAndSampling.jsx.map