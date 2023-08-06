import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tag from 'app/components/tag';
import { getRelativeDate } from 'app/components/timeSince';
import { t } from 'app/locale';
import { getDuration } from 'app/utils/formatters';
var GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
    REPROCESSED: 4,
};
var EVENT_ROUND_LIMIT = 1000;
function InboxReason(_a) {
    var inbox = _a.inbox, _b = _a.fontSize, fontSize = _b === void 0 ? 'sm' : _b;
    var reason = inbox.reason, reason_details = inbox.reason_details, dateAdded = inbox.date_added;
    var getCountText = function (count) {
        return count > EVENT_ROUND_LIMIT
            ? "More than " + Math.round(count / EVENT_ROUND_LIMIT) + "k"
            : "" + count;
    };
    function getReasonDetails() {
        switch (reason) {
            case GroupInboxReason.UNIGNORED:
                return {
                    tagType: 'default',
                    reasonBadgeText: t('Unignored'),
                    tooltipText: dateAdded &&
                        t('Unignored %(relative)s', {
                            relative: getRelativeDate(dateAdded, 'ago', true),
                        }),
                    tooltipDescription: t('%(count)s events in %(window)s', {
                        count: getCountText((reason_details === null || reason_details === void 0 ? void 0 : reason_details.count) || 0),
                        window: getDuration(((reason_details === null || reason_details === void 0 ? void 0 : reason_details.window) || 0) * 60, 0, true),
                    }),
                };
            case GroupInboxReason.REGRESSION:
                return {
                    tagType: 'error',
                    reasonBadgeText: t('Regression'),
                    tooltipText: dateAdded &&
                        t('Regressed %(relative)s', {
                            relative: getRelativeDate(dateAdded, 'ago', true),
                        }),
                };
            // TODO: Manual moves will go away, remove this then
            case GroupInboxReason.MANUAL:
                return {
                    tagType: 'highlight',
                    reasonBadgeText: t('Manual'),
                    tooltipText: dateAdded &&
                        t('Moved %(relative)s', { relative: getRelativeDate(dateAdded, 'ago', true) }),
                };
            case GroupInboxReason.REPROCESSED:
                return {
                    tagType: 'info',
                    reasonBadgeText: t('Reprocessed'),
                    tooltipText: dateAdded &&
                        t('Reprocessed %(relative)s', {
                            relative: getRelativeDate(dateAdded, 'ago', true),
                        }),
                };
            default:
                return {
                    tagType: 'warning',
                    reasonBadgeText: t('New Issue'),
                    tooltipText: dateAdded &&
                        t('Created %(relative)s', {
                            relative: getRelativeDate(dateAdded, 'ago', true),
                        }),
                };
        }
    }
    var _c = getReasonDetails(), tooltipText = _c.tooltipText, tooltipDescription = _c.tooltipDescription, reasonBadgeText = _c.reasonBadgeText, tagType = _c.tagType;
    var tooltip = (tooltipText || tooltipDescription) && (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {tooltipDescription && (<TooltipDescription>{tooltipDescription}</TooltipDescription>)}
    </TooltipWrapper>);
    return (<StyledTag type={tagType} tooltipText={tooltip} fontSize={fontSize}>
      {reasonBadgeText}
    </StyledTag>);
}
export default InboxReason;
var TooltipWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var TooltipDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
var StyledTag = styled(Tag)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ",
    ";\n"])), function (p) {
    return p.fontSize === 'sm' ? p.theme.fontSizeSmall : p.theme.fontSizeMedium;
});
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=inboxReason.jsx.map