import React from 'react';
import { t } from 'app/locale';
import TextBlock from 'app/views/settings/components/text/textBlock';
import RulesPanel from './rulesPanel';
function TransactionRules(_a) {
    var rules = _a.rules, onAddRule = _a.onAddRule;
    return (<React.Fragment>
      <TextBlock>
        {t('The transaction order is limited. Traces must occur first and individual transactions must occur last. Any individual transaction rules before a trace rule will be disregarded. ')}
      </TextBlock>
      <RulesPanel rules={rules} docsUrl="" onAddRule={onAddRule}/>
    </React.Fragment>);
}
export default TransactionRules;
//# sourceMappingURL=transactionRules.jsx.map