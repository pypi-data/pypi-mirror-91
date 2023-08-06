import React from 'react';
import ProcessingItem from '../processing/item';
import ProcessingList from '../processing/list';
import ProcessingIcon from './processingIcon';
function Processings(_a) {
    var unwind_status = _a.unwind_status, debug_status = _a.debug_status;
    var items = [];
    if (debug_status) {
        items.push(<ProcessingItem key="symbolication" type="symbolication" icon={<ProcessingIcon status={debug_status}/>}/>);
    }
    if (unwind_status) {
        items.push(<ProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<ProcessingIcon status={unwind_status}/>}/>);
    }
    return <ProcessingList items={items}/>;
}
export default Processings;
//# sourceMappingURL=processings.jsx.map