import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownLink from 'app/components/dropdownLink';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import SavedSearchMenu from './savedSearchMenu';
function SavedSearchTab(_a) {
    var isActive = _a.isActive, organization = _a.organization, savedSearchList = _a.savedSearchList, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, query = _a.query;
    var result = savedSearchList.find(function (search) { return query === search.query; });
    var activeTitle = result ? result.name : t('Custom Search');
    var title = isActive ? activeTitle : t('More');
    return (<TabWrapper isActive={isActive} className="saved-search-tab">
      <StyledDropdownLink alwaysRenderMenu={false} anchorMiddle caret title={<TitleWrapper>{title}</TitleWrapper>} isActive={isActive}>
        <SavedSearchMenu organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query}/>
      </StyledDropdownLink>
    </TabWrapper>);
}
export default SavedSearchTab;
var TabWrapper = styled('li')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Color matches nav-tabs - overwritten using dark mode class saved-search-tab */\n  border-bottom: ", ";\n  /* Reposition menu under caret */\n  & > span {\n    display: block;\n  }\n  & > span > .dropdown-menu {\n    margin-top: ", ";\n    min-width: 30vw;\n    max-width: 35vw;\n    z-index: ", ";\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 50vw;\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 55vw;\n    }\n  }\n\n  /* Fix nav tabs style leaking into menu */\n  * > li {\n    margin: 0;\n  }\n"], ["\n  /* Color matches nav-tabs - overwritten using dark mode class saved-search-tab */\n  border-bottom: ", ";\n  /* Reposition menu under caret */\n  & > span {\n    display: block;\n  }\n  & > span > .dropdown-menu {\n    margin-top: ", ";\n    min-width: 30vw;\n    max-width: 35vw;\n    z-index: ", ";\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 50vw;\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 55vw;\n    }\n  }\n\n  /* Fix nav tabs style leaking into menu */\n  * > li {\n    margin: 0;\n  }\n"])), function (p) { return (p.isActive ? "4px solid #6c5fc7" : 0); }, space(1), function (p) { return p.theme.zIndex.globalSelectionHeader; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[2]; });
var TitleWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  max-width: 150px;\n  user-select: none;\n  ", ";\n"], ["\n  margin-right: ", ";\n  max-width: 150px;\n  user-select: none;\n  ", ";\n"])), space(0.5), overflowEllipsis);
var StyledDropdownLink = styled(DropdownLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  display: block;\n  padding: ", " 0;\n  /* Important to override a media query from .nav-tabs */\n  font-size: ", " !important;\n  text-align: center;\n  text-transform: capitalize;\n  /* TODO(scttcper): Replace hex color when nav-tabs is replaced */\n  color: ", ";\n\n  :hover {\n    color: #2f2936;\n  }\n"], ["\n  position: relative;\n  display: block;\n  padding: ", " 0;\n  /* Important to override a media query from .nav-tabs */\n  font-size: ", " !important;\n  text-align: center;\n  text-transform: capitalize;\n  /* TODO(scttcper): Replace hex color when nav-tabs is replaced */\n  color: ", ";\n\n  :hover {\n    color: #2f2936;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeLarge; }, function (p) { return (p.isActive ? p.theme.textColor : '#7c6a8e'); });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=savedSearchTab.jsx.map