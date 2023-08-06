import React from 'react';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import OrganizationFiltersAndSampling from './organizationFiltersAndSampling';
var Index = function (_a) {
    var organization = _a.organization;
    return (<Feature features={['filters-and-sampling']} organization={organization} renderDisabled={function () { return (<FeatureDisabled alert={PanelAlert} features={organization.features} featureName={t('Filters & Sampling')}/>); }}>
    <OrganizationFiltersAndSampling />
  </Feature>);
};
export default withOrganization(Index);
//# sourceMappingURL=index.jsx.map