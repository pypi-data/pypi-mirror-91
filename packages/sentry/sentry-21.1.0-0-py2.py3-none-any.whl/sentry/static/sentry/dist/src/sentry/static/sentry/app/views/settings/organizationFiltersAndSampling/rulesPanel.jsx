import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { Panel, PanelFooter, PanelTable } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
function RulesPanel(_a) {
    var rules = _a.rules, docsUrl = _a.docsUrl, onAddRule = _a.onAddRule;
    return (<Panel>
      <StyledPanelTable headers={[t('Type'), t('Projects'), t('Condition'), t('Sampling Rate')]} isEmpty={!rules.length}>
        {null}
      </StyledPanelTable>
      <StyledPanelFooter>
        <ButtonBar gap={1}>
          <Button href={docsUrl} external>
            {t('Read the docs')}
          </Button>
          <Button priority="primary" onClick={onAddRule}>
            {t('Add rule')}
          </Button>
        </ButtonBar>
      </StyledPanelFooter>
    </Panel>);
}
export default RulesPanel;
// TODO(Priscila): Add PanelTable footer prop
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  border: none;\n  border-bottom-right-radius: 0;\n  border-bottom-left-radius: 0;\n"], ["\n  margin-bottom: 0;\n  border: none;\n  border-bottom-right-radius: 0;\n  border-bottom-left-radius: 0;\n"])));
var StyledPanelFooter = styled(PanelFooter)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])), space(1), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=rulesPanel.jsx.map