import { __assign, __rest } from "tslib";
import 'echarts/lib/component/legend';
import 'echarts/lib/component/legendScroll';
import { truncationFormatter } from '../utils';
export default function Legend(props) {
    if (props === void 0) { props = {}; }
    var _a = props !== null && props !== void 0 ? props : {}, truncate = _a.truncate, theme = _a.theme, rest = __rest(_a, ["truncate", "theme"]);
    var formatter = function (value) { return truncationFormatter(value, truncate !== null && truncate !== void 0 ? truncate : 0); };
    return __assign({ show: true, type: 'scroll', padding: 0, formatter: formatter, textStyle: {
            color: theme === null || theme === void 0 ? void 0 : theme.textColor,
        } }, rest);
}
//# sourceMappingURL=legend.jsx.map