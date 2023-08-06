import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import Collapsible from 'app/components/collapsible';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import { t, tn } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
function ProjectTeamAccess(_a) {
    var organization = _a.organization, project = _a.project;
    function renderInnerBody() {
        if (!project) {
            return <Placeholder height="23px"/>;
        }
        if (project.teams.length === 0) {
            var hasPermission = organization.access.includes('project:write');
            return (<Button to={"/settings/" + organization.slug + "/projects/" + project.slug + "/teams/"} disabled={!hasPermission} title={hasPermission ? undefined : t('You do not have permission to do this')} priority="primary" size="small">
          {t('Assign Team')}
        </Button>);
        }
        return (<Collapsible expandButton={function (_a) {
            var onExpand = _a.onExpand, numberOfCollapsedItems = _a.numberOfCollapsedItems;
            return (<Button priority="link" onClick={onExpand}>
            {tn('Show %s collapsed team', 'Show %s collapsed teams', numberOfCollapsedItems)}
          </Button>);
        }}>
        {project.teams.map(function (team) { return (<StyledLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"} key={team.slug}>
            <IdBadge team={team} hideAvatar/>
          </StyledLink>); })}
      </Collapsible>);
    }
    return (<Section>
      <SectionHeading>{t('Team Access')}</SectionHeading>

      <div>{renderInnerBody()}</div>
    </Section>);
}
ProjectTeamAccess.propTypes = {
    organization: SentryTypes.Organization.isRequired,
    project: SentryTypes.Project,
};
var Section = styled('section')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin-bottom: ", ";\n"], ["\n  display: block;\n  margin-bottom: ", ";\n"])), space(0.5));
export default ProjectTeamAccess;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectTeamAccess.jsx.map