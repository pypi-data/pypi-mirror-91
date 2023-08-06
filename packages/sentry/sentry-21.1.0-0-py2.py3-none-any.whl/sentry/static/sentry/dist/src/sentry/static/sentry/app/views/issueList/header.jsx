import { __assign, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { openModal } from 'app/actionCreators/modal';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import ContextPickerModalContainer from 'app/components/contextPickerModal';
import * as Layout from 'app/components/layouts/thirds';
import QueryCount from 'app/components/queryCount';
import { IconPause, IconPlay, IconUser } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import withProjects from 'app/utils/withProjects';
import SavedSearchTab from './savedSearchTab';
import { getTabs, Query, TAB_MAX_COUNT } from './utils';
function IssueListHeader(_a) {
    var organization = _a.organization, query = _a.query, queryCounts = _a.queryCounts, orgSlug = _a.orgSlug, projectIds = _a.projectIds, realtimeActive = _a.realtimeActive, onRealtimeChange = _a.onRealtimeChange, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, savedSearchList = _a.savedSearchList, projects = _a.projects, router = _a.router, displayReprocessingTab = _a.displayReprocessingTab;
    var selectedProjectSlugs = projectIds
        .map(function (projectId) { var _a; return (_a = projects.find(function (project) { return project.id === projectId; })) === null || _a === void 0 ? void 0 : _a.slug; })
        .filter(function (selectedProjectSlug) { return !!selectedProjectSlug; });
    var selectedProjectSlug = selectedProjectSlugs.length === 1 ? selectedProjectSlugs[0] : undefined;
    var tabs = getTabs(organization);
    var visibleTabs = displayReprocessingTab
        ? tabs
        : tabs.filter(function (_a) {
            var _b = __read(_a, 1), tab = _b[0];
            return tab !== Query.REPROCESSING;
        });
    var savedSearchTabActive = !visibleTabs.some(function (_a) {
        var _b = __read(_a, 1), tabQuery = _b[0];
        return tabQuery === query;
    });
    function handleSelectProject(settingsPage) {
        return function (event) {
            event.preventDefault();
            openModal(function (modalProps) { return (<ContextPickerModalContainer {...modalProps} nextPath={"/settings/" + orgSlug + "/projects/:projectId/" + settingsPage + "/"} needProject needOrg={false} onFinish={function (path) {
                modalProps.closeModal();
                router.push(path);
            }} projectSlugs={!!selectedProjectSlugs.length
                ? selectedProjectSlugs
                : projects.map(function (p) { return p.slug; })}/>); });
        };
    }
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{t('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <ButtonBar gap={1}>
            <Button size="small" icon={<IconUser size="xs"/>} to={selectedProjectSlug
        ? "/settings/" + orgSlug + "/projects/" + selectedProjectSlug + "/ownership/"
        : undefined} onClick={selectedProjectSlug ? undefined : handleSelectProject('ownership')}>
              {t('Issue Owners')}
            </Button>
            <Button size="small" title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))} onClick={function () { return onRealtimeChange(!realtimeActive); }}>
              {realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}
            </Button>
          </ButtonBar>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {visibleTabs.map(function (_a) {
        var _b;
        var _c = __read(_a, 2), tabQuery = _c[0], queryName = _c[1].name;
        return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
              <Link to={{
            query: __assign(__assign({}, (_b = router === null || router === void 0 ? void 0 : router.location) === null || _b === void 0 ? void 0 : _b.query), { query: tabQuery }),
            pathname: "/organizations/" + organization.slug + "/issues/",
        }}>
                {queryName}{' '}
                {queryCounts[tabQuery] && (<StyledQueryCount count={queryCounts[tabQuery].count} max={queryCounts[tabQuery].hasMore ? TAB_MAX_COUNT : 1000} backgroundColor={((tabQuery === Query.NEEDS_REVIEW_OWNER ||
            tabQuery === Query.NEEDS_REVIEW) &&
            theme.yellow300) ||
            theme.gray100}/>)}
              </Link>
            </li>);
    })}
          <SavedSearchTab organization={organization} query={query} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} isActive={savedSearchTabActive}/>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
export default withProjects(IssueListHeader);
IssueListHeader.propTypes = {
    projectIds: PropTypes.array.isRequired,
    projects: PropTypes.array.isRequired,
};
var StyledLayoutTitle = styled(Layout.Title)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var BorderlessHeader = styled(Layout.Header)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var TabLayoutHeader = styled(Layout.Header)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"], ["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n  margin-right: ", ";\n"], ["\n  margin-bottom: 0;\n  margin-right: ", ";\n"])), space(2));
var StyledQueryCount = styled(QueryCount)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map