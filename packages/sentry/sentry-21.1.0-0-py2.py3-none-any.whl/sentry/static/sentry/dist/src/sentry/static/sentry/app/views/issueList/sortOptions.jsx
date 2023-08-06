import React from 'react';
import PropTypes from 'prop-types';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import { t } from 'app/locale';
var IssueListSortOptions = function (_a) {
    var onSelect = _a.onSelect, sort = _a.sort;
    var sortKey = sort || 'date';
    var getSortLabel = function (key) {
        switch (key) {
            case 'new':
                return t('First Seen');
            case 'priority':
                return t('Priority');
            case 'freq':
                return t('Events');
            case 'user':
                return t('Users');
            case 'trend':
                return t('Relative Change');
            case 'date':
            default:
                return t('Last Seen');
        }
    };
    var getMenuItem = function (key) { return (<DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      {getSortLabel(key)}
    </DropdownItem>); };
    return (<DropdownControl buttonProps={{ prefix: t('Sort by') }} label={getSortLabel(sortKey)}>
      {getMenuItem('priority')}
      {getMenuItem('date')}
      {getMenuItem('new')}
      {getMenuItem('freq')}
      {getMenuItem('user')}
      <Feature features={['issue-list-trend-sort']}>{getMenuItem('trend')}</Feature>
    </DropdownControl>);
};
IssueListSortOptions.propTypes = {
    sort: PropTypes.string.isRequired,
    onSelect: PropTypes.func.isRequired,
};
export default IssueListSortOptions;
//# sourceMappingURL=sortOptions.jsx.map