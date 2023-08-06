import React from 'react';
import Button from 'app/components/button';
import { Panel } from 'app/components/panels';
import { IconCommit } from 'app/icons';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var NoRepoConnected = function (_a) {
    var orgId = _a.orgId;
    return (<Panel dashedBorder>
    <EmptyMessage icon={<IconCommit size="xl"/>} title={t('Releases are better with commit data!')} description={t('Connect a repository to see commit info, files changed, and authors involved in future releases.')} action={<Button priority="primary" to={"/settings/" + orgId + "/repos/"}>
          {t('Connect a repository')}
        </Button>}/>
  </Panel>);
};
export default NoRepoConnected;
//# sourceMappingURL=noRepoConnected.jsx.map