import React from 'react';
import VitalsCardDiscoverQuery from 'app/views/performance/vitalDetail/vitalsCardsDiscoverQuery';
import { VitalBar } from '../landing/vitalsCards';
export default function vitalInfo(props) {
    var vital = props.vital, eventView = props.eventView, organization = props.organization, location = props.location, hideBar = props.hideBar, hideStates = props.hideStates, hideVitalPercentNames = props.hideVitalPercentNames, hideDurationDetail = props.hideDurationDetail;
    return (<VitalsCardDiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} vitals={Array.isArray(vital) ? vital : [vital]}>
      {function (_a) {
        var _b;
        var isLoading = _a.isLoading, tableData = _a.tableData;
        return (<VitalBar isLoading={isLoading} result={(_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]} vital={vital} showBar={!hideBar} showStates={!hideStates} showVitalPercentNames={!hideVitalPercentNames} showDurationDetail={!hideDurationDetail}/>);
    }}
    </VitalsCardDiscoverQuery>);
}
//# sourceMappingURL=vitalInfo.jsx.map