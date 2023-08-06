import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import NotAvailable from '../notAvailable';
function List(_a) {
    var items = _a.items;
    if (!items.length) {
        return <NotAvailable />;
    }
    return <Wrapper>{items}</Wrapper>;
}
export default List;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  font-size: ", ";\n"])), space(2), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=list.jsx.map