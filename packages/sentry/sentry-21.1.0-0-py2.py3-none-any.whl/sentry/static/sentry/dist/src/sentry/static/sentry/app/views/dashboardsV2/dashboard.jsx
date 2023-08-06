import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import LazyLoad from 'react-lazyload';
import styled from '@emotion/styled';
import { openAddDashboardWidgetModal } from 'app/actionCreators/modal';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import { IconAdd } from 'app/icons';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { getPointerPosition } from 'app/utils/touch';
import { setBodyUserSelect } from 'app/utils/userselect';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import WidgetCard from './widgetCard';
var GHOST_WIDGET_OFFSET = 20;
var Dashboard = /** @class */ (function (_super) {
    __extends(Dashboard, _super);
    function Dashboard(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            draggingIndex: undefined,
            draggingTargetIndex: undefined,
            isDragging: false,
            top: undefined,
            left: undefined,
            widgets: undefined,
        };
        _this.previousUserSelect = null;
        _this.portal = null;
        _this.dragGhostRef = React.createRef();
        _this.handleStartAdd = function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
            });
        };
        _this.handleAddComplete = function (widget) {
            _this.props.onUpdate(__spread(_this.props.dashboard.widgets, [widget]));
        };
        _this.handleUpdateComplete = function (index) { return function (nextWidget) {
            var nextList = __spread(_this.props.dashboard.widgets);
            nextList[index] = nextWidget;
            _this.props.onUpdate(nextList);
        }; };
        _this.handleDeleteWidget = function (index) { return function () {
            var nextList = __spread(_this.props.dashboard.widgets);
            nextList.splice(index, 1);
            _this.props.onUpdate(nextList);
        }; };
        _this.handleEditWidget = function (widget, index) { return function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                widget: widget,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
                onUpdateWidget: _this.handleUpdateComplete(index),
            });
        }; };
        _this.startWidgetDrag = function (index) { return function (event) {
            if (_this.state.isDragging || !['mousedown', 'touchstart'].includes(event.type)) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            // prevent the user from selecting things when dragging a widget.
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor can drag anywhere
            window.addEventListener('mousemove', _this.onWidgetDragMove);
            window.addEventListener('mouseup', _this.onWidgetDragEnd);
            // If the target element is removed from the document, events will still be targeted at it, and hence won't
            // necessarily bubble up to the window or document anymore.
            // If there is any risk of an element being removed while it is being touched, the best practice is to attach the
            // touch listeners directly to the target.
            //
            // Source: https://developer.mozilla.org/en-US/docs/Web/API/Touch/target
            //
            // React may remove event.target from the document, and thus window.addEventListener('touchmove') would not get
            // called. Hence, for touch events, we attach to event.target directly, and
            // persist the event.
            event.target.addEventListener('touchmove', _this.onWidgetDragMove);
            event.persist();
            var onTouchEnd = function () {
                if (event.target) {
                    event.target.removeEventListener('touchmove', _this.onWidgetDragMove);
                    event.target.removeEventListener('touchend', onTouchEnd);
                }
            };
            event.target.addEventListener('touchend', onTouchEnd);
            var widgetWrappers = document.querySelectorAll('[data-component="widget-wrapper"]');
            var widgetWrapper = widgetWrappers[index];
            var rects = widgetWrapper.getBoundingClientRect();
            if (_this.dragGhostRef.current) {
                var ghostDOM = _this.dragGhostRef.current;
                // create the ghost widget
                var newClone = widgetWrapper.cloneNode(true);
                newClone.removeAttribute('data-component');
                var iconContainer = newClone.querySelector('[data-component="icon-container"]');
                if (iconContainer && iconContainer.parentNode) {
                    iconContainer.parentNode.removeChild(iconContainer);
                }
                newClone.style.width = rects.width + "px";
                newClone.style.height = rects.height + "px";
                ghostDOM.appendChild(newClone);
                ghostDOM.style.left = getPointerPosition(event, 'pageX') - GHOST_WIDGET_OFFSET + "px";
                ghostDOM.style.top = getPointerPosition(event, 'pageY') - GHOST_WIDGET_OFFSET + "px";
            }
            _this.setState({
                isDragging: true,
                draggingIndex: index,
                draggingTargetIndex: index,
                top: getPointerPosition(event, 'pageY'),
                left: getPointerPosition(event, 'pageX'),
                widgets: _this.shallowCloneWidgets(),
            });
        }; };
        _this.onWidgetDragMove = function (event) {
            if (!_this.state.isDragging ||
                !['mousemove', 'touchmove'].includes(event.type) ||
                !_this.state.widgets ||
                _this.state.draggingIndex === undefined) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            if (_this.dragGhostRef.current) {
                // move the ghost box
                var ghostDOM = _this.dragGhostRef.current;
                ghostDOM.style.left = getPointerPosition(event, 'pageX') - GHOST_WIDGET_OFFSET + "px";
                ghostDOM.style.top = getPointerPosition(event, 'pageY') - GHOST_WIDGET_OFFSET + "px";
            }
            var widgetWrappers = document.querySelectorAll('[data-component="widget-wrapper"]');
            // Find the widget that the ghost is currently over.
            var targetIndex = Array.from(widgetWrappers).findIndex(function (widgetWrapper) {
                var rects = widgetWrapper.getBoundingClientRect();
                var top = getPointerPosition(event, 'clientY');
                var left = getPointerPosition(event, 'clientX');
                var topStart = rects.top;
                var topEnd = rects.top + rects.height;
                var leftStart = rects.left;
                var leftEnd = rects.left + rects.width;
                return topStart <= top && top <= topEnd && leftStart <= left && left <= leftEnd;
            });
            if (targetIndex >= 0 && targetIndex !== _this.state.draggingTargetIndex) {
                var nextWidgets = _this.shallowCloneWidgets();
                var removed = nextWidgets.splice(_this.state.draggingIndex, 1);
                nextWidgets.splice(targetIndex, 0, removed[0]);
                _this.setState({ draggingTargetIndex: targetIndex, widgets: nextWidgets });
            }
        };
        _this.onWidgetDragEnd = function (event) {
            if (!_this.state.isDragging || !['mouseup', 'touchend'].includes(event.type)) {
                return;
            }
            var sourceIndex = _this.state.draggingIndex;
            var targetIndex = _this.state.draggingTargetIndex;
            if (typeof sourceIndex !== 'number' || typeof targetIndex !== 'number') {
                return;
            }
            // remove listeners that were attached in startWidgetDrag
            _this.cleanUpListeners();
            // restore body user-select values
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            if (_this.dragGhostRef.current) {
                var ghostDOM = _this.dragGhostRef.current;
                ghostDOM.innerHTML = '';
            }
            // Reorder widgets and trigger change.
            if (sourceIndex !== targetIndex) {
                var newWidgets = __spread(_this.props.dashboard.widgets);
                var removed = newWidgets.splice(sourceIndex, 1);
                newWidgets.splice(targetIndex, 0, removed[0]);
                _this.props.onUpdate(newWidgets);
            }
            _this.setState({
                isDragging: false,
                left: undefined,
                top: undefined,
                draggingIndex: undefined,
                draggingTargetIndex: undefined,
                widgets: undefined,
            });
        };
        _this.renderGhost = function () {
            if (!_this.portal) {
                return null;
            }
            var top = typeof _this.state.top === 'number' ? _this.state.top - GHOST_WIDGET_OFFSET : 0;
            var left = typeof _this.state.left === 'number' ? _this.state.left - GHOST_WIDGET_OFFSET : 0;
            var ghost = (<WidgetGhost id="ghost" ref={_this.dragGhostRef} style={{ top: top + "px", left: left + "px" }}/>);
            return ReactDOM.createPortal(ghost, _this.portal);
        };
        // Create a DOM node that exists outside the DOM hierarchy of this component.
        // Widget ghosts will be rendered within this portal.
        var portal = document.createElement('div');
        portal.style.position = 'absolute';
        portal.style.top = '0';
        portal.style.left = '0';
        portal.style.zIndex = String(theme.zIndex.modal);
        _this.portal = portal;
        return _this;
    }
    Dashboard.prototype.componentDidMount = function () {
        var isEditing = this.props.isEditing;
        // Load organization tags when in edit mode.
        if (isEditing) {
            this.fetchTags();
        }
        if (this.portal) {
            document.body.appendChild(this.portal);
        }
    };
    Dashboard.prototype.componentDidUpdate = function (prevProps) {
        var isEditing = this.props.isEditing;
        // Load organization tags when going into edit mode.
        // We use tags on the add widget modal.
        if (prevProps.isEditing !== isEditing && isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.componentWillUnmount = function () {
        if (this.portal) {
            document.body.removeChild(this.portal);
        }
        this.cleanUpListeners();
    };
    Dashboard.prototype.fetchTags = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
    };
    Dashboard.prototype.cleanUpListeners = function () {
        if (this.state.isDragging) {
            window.removeEventListener('mousemove', this.onWidgetDragMove);
            window.removeEventListener('mouseup', this.onWidgetDragEnd);
        }
    };
    Dashboard.prototype.shallowCloneWidgets = function () {
        return this.props.dashboard.widgets.map(function (widget, index) {
            var _a;
            return __assign(__assign({}, widget), { id: (_a = widget.id) !== null && _a !== void 0 ? _a : String(index) });
        });
    };
    Dashboard.prototype.renderWidget = function (widget, index) {
        var _a;
        var isEditing = this.props.isEditing;
        return (<LazyLoad key={"" + ((_a = widget.id) !== null && _a !== void 0 ? _a : index)} once height={240} offset={100}>
        <WidgetWrapper data-component="widget-wrapper">
          <WidgetCard widget={widget} isEditing={isEditing} onDelete={this.handleDeleteWidget(index)} onEdit={this.handleEditWidget(widget, index)} isDragging={this.state.isDragging && this.state.draggingTargetIndex === index} hideToolbar={this.state.isDragging} startWidgetDrag={this.startWidgetDrag(index)}/>
        </WidgetWrapper>
      </LazyLoad>);
    };
    Dashboard.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEditing = _a.isEditing, dashboard = _a.dashboard;
        var widgets = this.state.isDragging && this.state.widgets
            ? this.state.widgets
            : dashboard.widgets;
        return (<WidgetContainer>
        {widgets.map(function (widget, i) { return _this.renderWidget(widget, i); })}
        {isEditing && (<WidgetWrapper key="add">
            <AddWidgetWrapper key="add" data-test-id="widget-add" onClick={this.handleStartAdd}>
              <IconAdd size="lg" isCircled color="inactive"/>
            </AddWidgetWrapper>
          </WidgetWrapper>)}
        {this.renderGhost()}
      </WidgetContainer>);
    };
    return Dashboard;
}(React.Component));
export default withApi(withGlobalSelection(Dashboard));
var WidgetContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; });
var WidgetWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var AddWidgetWrapper = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n  min-height: 200px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: 100%;\n  height: 100%;\n  min-height: 200px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var WidgetGhost = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: block;\n  position: absolute;\n  cursor: grabbing;\n  opacity: 0.8;\n  box-shadow: ", ";\n  border-radius: ", ";\n"], ["\n  display: block;\n  position: absolute;\n  cursor: grabbing;\n  opacity: 0.8;\n  box-shadow: ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.dropShadowHeavy; }, function (p) { return p.theme.borderRadius; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=dashboard.jsx.map