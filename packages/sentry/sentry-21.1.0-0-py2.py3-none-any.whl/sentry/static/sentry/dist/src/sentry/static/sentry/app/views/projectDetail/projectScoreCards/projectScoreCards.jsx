import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ScoreCard from 'app/components/scoreCard';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import ProjectApdexScoreCard from './projectApdexScoreCard';
import ProjectVelocityScoreCard from './projectVelocityScoreCard';
function ProjectScoreCards(_a) {
    var organization = _a.organization, selection = _a.selection;
    return (<CardWrapper>
      <ScoreCard title={t('Stability Score')} help={t('Stability score is used to // TODO(project-detail)')} score="94.1%" trend="+13.5%" trendStyle="good"/>

      <ProjectVelocityScoreCard organization={organization} selection={selection}/>

      <ProjectApdexScoreCard organization={organization} selection={selection}/>
    </CardWrapper>);
}
var CardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"])), space(2), space(3), function (p) { return p.theme.breakpoints[0]; });
export default withGlobalSelection(ProjectScoreCards);
var templateObject_1;
//# sourceMappingURL=projectScoreCards.jsx.map