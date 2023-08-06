import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { AutoSizer, CellMeasurer, CellMeasurerCache, List, } from 'react-virtualized';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import EventDataSection from 'app/components/events/eventDataSection';
import { getImageRange, parseAddress } from 'app/components/events/interfaces/utils';
import { Panel, PanelHeader } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import SearchBar from 'app/components/searchBar';
import { IconSearch } from 'app/icons/iconSearch';
import { t } from 'app/locale';
import DebugMetaStore, { DebugMetaActions } from 'app/stores/debugMetaStore';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { ImageStatus } from 'app/types/debugImage';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Status from './debugImage/status';
import DebugImage from './debugImage';
import DebugImageDetails, { modalCss } from './debugImageDetails';
import Filter from './filter';
import layout from './layout';
import { combineStatus, getFileName, normalizeId } from './utils';
var PANEL_MAX_HEIGHT = 400;
var cache = new CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
var DebugMeta = /** @class */ (function (_super) {
    __extends(DebugMeta, _super);
    function DebugMeta() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            isLoading: false,
            filterOptions: [],
            filteredImages: [],
            filteredImagesByFilter: [],
            filteredImagesBySearch: [],
        };
        _this.panelTableRef = React.createRef();
        _this.listRef = null;
        _this.onStoreChange = function (store) {
            var searchTerm = _this.state.searchTerm;
            if (store.filter !== searchTerm) {
                _this.setState({ searchTerm: store.filter }, _this.filterImagesBySearchTerm);
            }
        };
        _this.onListResize = function () {
            _this.setState({ isLoading: true }, _this.updateGrid);
        };
        _this.updateGrid = function () {
            if (_this.listRef) {
                cache.clearAll();
                _this.listRef.forceUpdateGrid();
            }
        };
        _this.handleChangeFilter = function (filterOptions) {
            var filteredImagesBySearch = _this.state.filteredImagesBySearch;
            var filteredImagesByFilter = _this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
            _this.setState({ filterOptions: filterOptions, filteredImagesByFilter: filteredImagesByFilter }, _this.updateGrid);
        };
        _this.handleChangeSearchTerm = function (searchTerm) {
            if (searchTerm === void 0) { searchTerm = ''; }
            DebugMetaActions.updateFilter(searchTerm);
        };
        _this.handleResetFilter = function () {
            var filterOptions = _this.state.filterOptions;
            _this.setState({
                filterOptions: filterOptions.map(function (filterOption) { return (__assign(__assign({}, filterOption), { isChecked: false })); }),
            }, _this.filterImagesBySearchTerm);
        };
        _this.handleResetSearchBar = function () {
            _this.setState(function (prevState) { return ({
                searchTerm: '',
                filteredImagesByFilter: prevState.filteredImages,
                filteredImagesBySearch: prevState.filteredImages,
            }); });
        };
        _this.handleOpenImageDetailsModal = function (image, imageAddress, fileName) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            return openModal(function (modalProps) { return (<DebugImageDetails {...modalProps} image={image} title={fileName} organization={organization} projectId={projectId} imageAddress={imageAddress}/>); }, {
                modalCss: modalCss,
            });
        };
        _this.renderRow = function (_a) {
            var index = _a.index, key = _a.key, parent = _a.parent, style = _a.style;
            var images = _this.state.filteredImagesByFilter;
            return (<CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <DebugImage style={style} image={images[index]} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>
      </CellMeasurer>);
        };
        return _this;
    }
    DebugMeta.prototype.componentDidMount = function () {
        this.unsubscribeFromStore = DebugMetaStore.listen(this.onStoreChange, undefined);
        cache.clearAll();
        this.getRelevantImages();
    };
    DebugMeta.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
        if (this.state.isLoading) {
            this.getInnerListWidth();
        }
    };
    DebugMeta.prototype.componentWillUnmount = function () {
        if (this.unsubscribeFromStore) {
            this.unsubscribeFromStore();
        }
    };
    DebugMeta.prototype.getInnerListWidth = function () {
        var _a, _b, _c;
        var innerListWidth = (_c = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.querySelector('.ReactVirtualized__Grid__innerScrollContainer')) === null || _c === void 0 ? void 0 : _c.clientWidth;
        if (innerListWidth !== this.state.innerListWidth) {
            this.setState({ innerListWidth: innerListWidth, isLoading: false });
            return;
        }
        this.setState({ isLoading: false });
    };
    DebugMeta.prototype.isValidImage = function (image) {
        // in particular proguard images do not have a code file, skip them
        if (image === null || image.code_file === null || image.type === 'proguard') {
            return false;
        }
        if (getFileName(image.code_file) === 'dyld_sim') {
            // this is only for simulator builds
            return false;
        }
        return true;
    };
    DebugMeta.prototype.filterImage = function (image, searchTerm) {
        var _a, _b;
        // When searching for an address, check for the address range of the image
        // instead of an exact match.  Note that images cannot be found by index
        // if they are at 0x0.  For those relative addressing has to be used.
        if (searchTerm.indexOf('0x') === 0) {
            var needle = parseAddress(searchTerm);
            if (needle > 0 && image.image_addr !== '0x0') {
                var _c = __read(getImageRange(image), 2), startAddress = _c[0], endAddress = _c[1]; // TODO(PRISCILA): remove any
                return needle >= startAddress && needle < endAddress;
            }
        }
        // the searchTerm ending at "!" is the end of the ID search.
        var relMatch = searchTerm.match(/^\s*(.*?)!/); // debug_id!address
        var idSearchTerm = normalizeId((relMatch === null || relMatch === void 0 ? void 0 : relMatch[1]) || searchTerm);
        return (
        // Prefix match for identifiers
        normalizeId(image.code_id).indexOf(idSearchTerm) === 0 ||
            normalizeId(image.debug_id).indexOf(idSearchTerm) === 0 ||
            // Any match for file paths
            (((_a = image.code_file) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_b = image.debug_file) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    };
    DebugMeta.prototype.filterImagesBySearchTerm = function () {
        var _this = this;
        var _a = this.state, filteredImages = _a.filteredImages, filterOptions = _a.filterOptions, searchTerm = _a.searchTerm;
        var filteredImagesBySearch = filteredImages.filter(function (image) {
            return _this.filterImage(image, searchTerm.toLowerCase());
        });
        var filteredImagesByFilter = this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
        this.setState({
            filteredImagesBySearch: filteredImagesBySearch,
            filteredImagesByFilter: filteredImagesByFilter,
        }, this.updateGrid);
    };
    DebugMeta.prototype.getPanelBodyHeight = function () {
        var _a, _b;
        var panelTableHeight = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelTableHeight) {
            return;
        }
        this.setState({ panelTableHeight: panelTableHeight });
    };
    DebugMeta.prototype.getRelevantImages = function () {
        var data = this.props.data;
        var images = data.images;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        var relevantImages = images.filter(this.isValidImage).map(function (releventImage) {
            var debug_status = releventImage.debug_status, unwind_status = releventImage.unwind_status;
            return __assign(__assign({}, releventImage), { status: combineStatus(debug_status, unwind_status) });
        });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        relevantImages.sort(function (a, b) { return parseAddress(a.image_addr) - parseAddress(b.image_addr); });
        var unusedImages = [];
        var usedImages = relevantImages.filter(function (image) {
            if (image.debug_status === ImageStatus.UNUSED) {
                unusedImages.push(image);
                return false;
            }
            return true;
        });
        var filteredImages = __spread(usedImages, unusedImages);
        var filterOptions = this.getFilterOptions(filteredImages);
        this.setState({
            filteredImages: filteredImages,
            filterOptions: filterOptions,
            filteredImagesByFilter: filteredImages,
            filteredImagesBySearch: filteredImages,
        });
    };
    DebugMeta.prototype.getFilterOptions = function (images) {
        return __spread(new Set(images.map(function (image) { return image.status; }))).map(function (status) { return ({
            id: status,
            symbol: <Status status={status}/>,
            isChecked: false,
        }); });
    };
    DebugMeta.prototype.getDebugImages = function () {
        var _this = this;
        var data = this.props.data;
        var images = data.images;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        var filtered = images.filter(function (image) { return _this.isValidImage(image); });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        filtered.sort(function (a, b) { return parseAddress(a.image_addr) - parseAddress(b.image_addr); });
        return filtered;
    };
    DebugMeta.prototype.getListHeight = function () {
        var panelTableHeight = this.state.panelTableHeight;
        if (!panelTableHeight || panelTableHeight > PANEL_MAX_HEIGHT) {
            return PANEL_MAX_HEIGHT;
        }
        return panelTableHeight;
    };
    DebugMeta.prototype.getFilteredImagesByFilter = function (filteredImages, filterOptions) {
        var checkedOptions = new Set(filterOptions
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        if (!__spread(checkedOptions).length) {
            return filteredImages;
        }
        return filteredImages.filter(function (image) { return checkedOptions.has(image.status); });
    };
    DebugMeta.prototype.renderList = function () {
        var _this = this;
        var _a = this.state, images = _a.filteredImagesByFilter, panelTableHeight = _a.panelTableHeight;
        if (!panelTableHeight) {
            return images.map(function (image) { return (<DebugImage key={image.debug_file} image={image} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>); });
        }
        return (<AutoSizer disableHeight onResize={this.onListResize}>
        {function (_a) {
            var width = _a.width;
            return (<StyledList ref={function (el) {
                _this.listRef = el;
            }} deferredMeasurementCache={cache} height={_this.getListHeight()} overscanRowCount={5} rowCount={images.length} rowHeight={cache.rowHeight} rowRenderer={_this.renderRow} width={width} isScrolling={false}/>);
        }}
      </AutoSizer>);
    };
    DebugMeta.prototype.renderContent = function () {
        var _a = this.state, searchTerm = _a.searchTerm, images = _a.filteredImagesByFilter, filterOptions = _a.filterOptions;
        if (searchTerm && !images.length) {
            var hasActiveFilter = filterOptions.find(function (filterOption) { return filterOption.isChecked; });
            return (<EmptyMessage icon={<IconSearch size="xl"/>} action={hasActiveFilter ? (<Button onClick={this.handleResetFilter} priority="primary">
                {t('Reset Filter')}
              </Button>) : (<Button onClick={this.handleResetSearchBar} priority="primary">
                {t('Clear Search Bar')}
              </Button>)}>
          {t('Sorry, no images match your search query.')}
        </EmptyMessage>);
        }
        if (!images.length) {
            return (<EmptyStateWarning>
          <p>{t('There are no images to be displayed')}</p>
        </EmptyStateWarning>);
        }
        return <div ref={this.panelTableRef}>{this.renderList()}</div>;
    };
    DebugMeta.prototype.render = function () {
        var _this = this;
        var _a = this.state, searchTerm = _a.searchTerm, filterOptions = _a.filterOptions, innerListWidth = _a.innerListWidth;
        return (<StyledEventDataSection type="images-loaded" title={<TitleWrapper>
            <GuideAnchor target="images-loaded" position="bottom">
              <Title>{t('Images Loaded')}</Title>
            </GuideAnchor>
            <QuestionTooltip size="xs" position="top" title={t('A list of dynamic librarys or shared objects loaded into process memory at the time of the crash. Images contribute application code that is referenced in stack traces.')}/>
          </TitleWrapper>} actions={<Search>
            <Filter options={filterOptions} onFilter={this.handleChangeFilter}/>
            <StyledSearchBar query={searchTerm} onChange={function (value) { return _this.handleChangeSearchTerm(value); }} placeholder={t('Search images\u2026')}/>
          </Search>} wrapTitle={false} isCentered>
        <StyledPanel innerListWidth={innerListWidth}>
          <StyledPanelHeader>
            <div>{t('Status')}</div>
            <div>{t('Image')}</div>
            <div>{t('Processing')}</div>
            <div>{t('Details')}</div>
          </StyledPanelHeader>
          {this.renderContent()}
        </StyledPanel>
      </StyledEventDataSection>);
    };
    DebugMeta.defaultProps = {
        data: { images: [] },
    };
    return DebugMeta;
}(React.PureComponent));
export default DebugMeta;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"], ["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[0]; }, space(2));
var StyledPanelHeader = styled(PanelHeader)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0;\n  > * {\n    padding: ", ";\n    ", ";\n  }\n  ", ";\n"], ["\n  padding: 0;\n  > * {\n    padding: ", ";\n    ", ";\n  }\n  ", ";\n"])), space(2), overflowEllipsis, function (p) { return layout(p.theme); });
var StyledPanel = styled(Panel, {
    shouldForwardProp: function (prop) { return prop !== 'innerListWidth'; },
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ",
    ";\n"])), function (p) {
    return p.innerListWidth &&
        "\n        " + StyledPanelHeader + " {\n          padding-right: calc(100% - " + p.innerListWidth + "px);\n        }\n    ";
});
// Section Title
var TitleWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"])), space(0.5), space(0.75));
var Title = styled('h3')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"], ["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"])));
// Virtual List
var StyledList = styled(List)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"], ["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"])), function (p) { return p.height; });
// Search
var Search = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space(1), function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled(SearchBar)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  width: 100%;\n  position: relative;\n  z-index: ", ";\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  width: 100%;\n  position: relative;\n  z-index: ", ";\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"])), function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map