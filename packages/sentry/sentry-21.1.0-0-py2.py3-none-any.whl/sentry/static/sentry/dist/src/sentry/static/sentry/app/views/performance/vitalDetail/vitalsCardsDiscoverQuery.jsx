import { __read, __spread } from "tslib";
import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
import { vitalsBaseFields, vitalsMehFields, vitalsP75Fields, vitalsPoorFields, } from './utils';
function getRequestPayload(props) {
    var eventView = props.eventView, vitals = props.vitals;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    var vitalFields = vitals
        .map(function (vital) {
        return [
            vitalsPoorFields[vital],
            vitalsBaseFields[vital],
            vitalsMehFields[vital],
            vitalsP75Fields[vital],
        ].filter(Boolean);
    })
        .reduce(function (fields, fs) { return fields.concat(fs); }, []);
    apiPayload.field = __spread(vitalFields);
    delete apiPayload.sort;
    return apiPayload;
}
function VitalsCardDiscoverQuery(props) {
    return (<GenericDiscoverQuery getRequestPayload={getRequestPayload} route="eventsv2" noPagination {...props}/>);
}
export default withApi(VitalsCardDiscoverQuery);
//# sourceMappingURL=vitalsCardsDiscoverQuery.jsx.map