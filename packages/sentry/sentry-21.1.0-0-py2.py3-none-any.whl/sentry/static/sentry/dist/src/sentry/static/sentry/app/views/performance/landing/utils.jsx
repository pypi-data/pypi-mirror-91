import { decodeScalar } from 'app/utils/queryString';
export var LandingDisplayField;
(function (LandingDisplayField) {
    LandingDisplayField["FRONTEND"] = "frontend";
})(LandingDisplayField || (LandingDisplayField = {}));
export var LANDING_DISPLAYS = [
    {
        label: 'Frontend',
        field: LandingDisplayField.FRONTEND,
    },
];
export function getCurrentLandingDisplay(location) {
    var _a;
    var landingField = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.landingDisplay);
    var display = LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === landingField;
    });
    return display || LANDING_DISPLAYS[0];
}
export function getChartWidth(chartData, refPixelRect) {
    var distance = refPixelRect ? refPixelRect.point2.x - refPixelRect.point1.x : 0;
    var chartWidth = chartData.length * distance;
    return {
        chartWidth: chartWidth,
    };
}
export function getAdditionalTableQuery(location) {
    var _a;
    return decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a.tableFilterQuery) || '';
}
//# sourceMappingURL=utils.jsx.map