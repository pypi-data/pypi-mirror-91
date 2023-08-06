import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory, withRouter } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { generateAggregateFields } from 'app/utils/discover/fields';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import SearchBar from 'app/views/events/searchBar';
import Charts from '../charts/index';
import { generateFrontendPerformanceEventView } from '../data';
import Table from '../table';
import { getTransactionSearchQuery } from '../utils';
import { FRONTEND_COLUMN_TITLES } from './data';
import FrontendDisplay from './frontendDisplay';
import { getAdditionalTableQuery, getCurrentLandingDisplay, LANDING_DISPLAYS, LandingDisplayField, } from './utils';
import { FrontendCards } from './vitalsCards';
var LandingContent = /** @class */ (function (_super) {
    __extends(LandingContent, _super);
    function LandingContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLandingDisplayChange = function (field) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { landingDisplay: field }),
            });
        };
        _this.handleTableQueryUpdate = function (additionalTableQuery) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { tableFilterQuery: additionalTableQuery }),
            });
        };
        return _this;
    }
    LandingContent.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch(query);
        parsed.query = [];
        return stringifyQueryObject(parsed);
    };
    LandingContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects, eventView = _a.eventView, setError = _a.setError, handleSearch = _a.handleSearch;
        var currentLandingDisplay = getCurrentLandingDisplay(location);
        var filterString = getTransactionSearchQuery(location, eventView.query);
        var summaryConditions = this.getSummaryConditions(filterString);
        return (<div>
        <Feature organization={organization} features={['performance-landing-v2']}>
          {function (_a) {
            var hasFeature = _a.hasFeature;
            if (hasFeature) {
                var additionalSummaryConditions = _this.getSummaryConditions(getAdditionalTableQuery(location));
                var frontendEventView = generateFrontendPerformanceEventView(_this.props.organization, _this.props.location);
                var frontendTableEventView = frontendEventView.clone();
                frontendTableEventView.query = summaryConditions + " " + additionalSummaryConditions;
                return (<React.Fragment>
                  <SearchContainer>
                    <StyledSearchBar organization={organization} projectIds={frontendEventView.project} query={filterString} fields={generateAggregateFields(organization, __spread(frontendEventView.fields, [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch}/>
                    <ProjectTypeDropdown>
                      <DropdownControl buttonProps={{ prefix: t('Display') }} label={currentLandingDisplay.label}>
                        {LANDING_DISPLAYS.map(function (_a) {
                    var label = _a.label, field = _a.field;
                    return (<DropdownItem key={field} onSelect={_this.handleLandingDisplayChange} eventKey={field} data-test-id={field} isActive={field === currentLandingDisplay.field}>
                            {label}
                          </DropdownItem>);
                })}
                      </DropdownControl>
                    </ProjectTypeDropdown>
                  </SearchContainer>
                  <FrontendCards eventView={frontendEventView} organization={organization} location={location} projects={projects}/>
                  {currentLandingDisplay.field === LandingDisplayField.FRONTEND && (<FrontendDisplay eventView={frontendEventView} organization={organization} location={location} onFrontendDisplayFilter={_this.handleTableQueryUpdate}/>)}
                  <Table eventView={frontendTableEventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={frontendEventView.query} columnTitles={FRONTEND_COLUMN_TITLES}/>
                </React.Fragment>);
            }
            return (<React.Fragment>
                <StyledSearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={generateAggregateFields(organization, __spread(eventView.fields, [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch}/>
                <Feature features={['performance-vitals-overview']}>
                  <FrontendCards eventView={eventView} organization={organization} location={location} projects={projects} frontendOnly/>
                </Feature>
                <Charts eventView={eventView} organization={organization} location={location} router={router}/>
                <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={summaryConditions}/>
              </React.Fragment>);
        }}
        </Feature>
      </div>);
    };
    return LandingContent;
}(React.Component));
var SearchContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n"])));
var ProjectTypeDropdown = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"])), space(2));
export default withRouter(LandingContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map