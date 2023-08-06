import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import space from 'app/styles/space';
import { defined } from 'app/utils';
/**
 * Displays a number count. If `max` is specified, then give representation
 * of count, i.e. "1000+"
 *
 * Render nothing by default if `count` is falsy.
 */
var QueryCount = function (_a) {
    var count = _a.count, max = _a.max, _b = _a.hideIfEmpty, hideIfEmpty = _b === void 0 ? true : _b, _c = _a.hideParens, hideParens = _c === void 0 ? false : _c, backgroundColor = _a.backgroundColor;
    var countOrMax = defined(count) && defined(max) && count >= max ? max + "+" : count;
    if (hideIfEmpty && !count) {
        return null;
    }
    if (backgroundColor) {
        return (<StyledBackground backgroundColor={backgroundColor}>{countOrMax}</StyledBackground>);
    }
    return (<span>
      {!hideParens && <span>(</span>}
      <span>{countOrMax}</span>
      {!hideParens && <span>)</span>}
    </span>);
};
QueryCount.propTypes = {
    count: PropTypes.number,
    max: PropTypes.number,
    hideIfEmpty: PropTypes.bool,
    hideParens: PropTypes.bool,
};
var StyledBackground = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n  height: 20px;\n  border-radius: 20px;\n  color: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n  line-height: 20px;\n  font-size: ", ";\n"], ["\n  display: inline-flex;\n  align-items: center;\n  height: 20px;\n  border-radius: 20px;\n  color: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n  line-height: 20px;\n  font-size: ", ";\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.backgroundColor; }, space(1), function (p) { return p.theme.fontSizeSmall; });
export default QueryCount;
var templateObject_1;
//# sourceMappingURL=queryCount.jsx.map