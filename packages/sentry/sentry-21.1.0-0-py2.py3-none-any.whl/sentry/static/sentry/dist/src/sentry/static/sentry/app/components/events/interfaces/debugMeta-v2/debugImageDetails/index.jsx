import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { CandidateDownloadStatus } from 'app/types/debugImage';
import theme from 'app/utils/theme';
import NotAvailable from '../notAvailable';
import Candidates from './candidates';
import { INTERNAL_SOURCE } from './utils';
var DebugFileDetails = /** @class */ (function (_super) {
    __extends(DebugFileDetails, _super);
    function DebugFileDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (debugId) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, projectId, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, projectId = _a.projectId;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugId, { method: 'DELETE' })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred while deleting the debug file.'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    DebugFileDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { debugFiles: [], builtinSymbolSources: [] });
    };
    DebugFileDetails.prototype.getUplodedDebugFiles = function (candidates) {
        return candidates.find(function (candidate) { return candidate.source === INTERNAL_SOURCE; });
    };
    DebugFileDetails.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, projectId = _b.projectId, image = _b.image;
        var debug_id = image.debug_id, _c = image.candidates, candidates = _c === void 0 ? [] : _c;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var uploadedDebugFiles = this.getUplodedDebugFiles(candidates);
        var endpoints = [];
        if (uploadedDebugFiles) {
            endpoints.push([
                'debugFiles',
                "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?debug_id=" + debug_id,
                {
                    query: {
                        file_formats: !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('android-mappings'))
                            ? ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle']
                            : undefined,
                    },
                },
            ]);
        }
        if (!builtinSymbolSources && organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    DebugFileDetails.prototype.getCandidates = function () {
        var _a = this.state, debugFiles = _a.debugFiles, loading = _a.loading;
        var image = this.props.image;
        var _b = image.candidates, candidates = _b === void 0 ? [] : _b;
        if (!debugFiles || loading) {
            return candidates;
        }
        // Check for unapplied debug files
        var candidateLocations = new Set(candidates.map(function (candidate) { return candidate.location; }).filter(function (candidate) { return !!candidate; }));
        var unAppliedDebugFiles = debugFiles
            .filter(function (debugFile) { return !candidateLocations.has(debugFile.id); })
            .map(function (debugFile) { return ({
            download: {
                status: CandidateDownloadStatus.UNAPPLIED,
            },
            location: debugFile.id,
            source: INTERNAL_SOURCE,
            source_name: debugFile.objectName,
        }); });
        // Check for deleted debug files
        var debugFileIds = new Set(debugFiles.map(function (debugFile) { return debugFile.id; }));
        var convertedCandidates = candidates.map(function (candidate) {
            if (candidate.source === INTERNAL_SOURCE &&
                candidate.location &&
                !debugFileIds.has(candidate.location)) {
                return __assign(__assign({}, candidate), { download: {
                        status: CandidateDownloadStatus.DELETED,
                    } });
            }
            return candidate;
        });
        return __spread(convertedCandidates, unAppliedDebugFiles);
    };
    DebugFileDetails.prototype.renderLoading = function () {
        return this.renderBody();
    };
    DebugFileDetails.prototype.renderBody = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, image = _a.image, title = _a.title, imageAddress = _a.imageAddress, organization = _a.organization, projectId = _a.projectId;
        var _b = this.state, loading = _b.loading, builtinSymbolSources = _b.builtinSymbolSources;
        var debug_id = image.debug_id, debug_file = image.debug_file, code_file = image.code_file, code_id = image.code_id, architecture = image.arch;
        var candidates = this.getCandidates();
        var baseUrl = this.api.baseUrl;
        return (<React.Fragment>
        <Header closeButton>{title !== null && title !== void 0 ? title : t('Unknown')}</Header>
        <Body>
          <Content>
            <GeneralInfo>
              <Label>{t('Address Range')}</Label>
              <Value>{imageAddress !== null && imageAddress !== void 0 ? imageAddress : <NotAvailable />}</Value>

              <Label coloredBg>{t('Debug ID')}</Label>
              <Value coloredBg>{debug_id !== null && debug_id !== void 0 ? debug_id : <NotAvailable />}</Value>

              <Label>{t('Debug File')}</Label>
              <Value>{debug_file}</Value>

              <Label coloredBg>{t('Code ID')}</Label>
              <Value coloredBg>{code_id}</Value>

              <Label>{t('Code File')}</Label>
              <Value>{code_file}</Value>

              <Label coloredBg>{t('Architecture')}</Label>
              <Value coloredBg>{architecture !== null && architecture !== void 0 ? architecture : <NotAvailable />}</Value>
            </GeneralInfo>
            <Candidates candidates={candidates} organization={organization} projectId={projectId} baseUrl={baseUrl} onDelete={this.handleDelete} isLoading={loading} builtinSymbolSources={builtinSymbolSources}/>
          </Content>
        </Body>
        <Footer>
          <Button href="https://docs.sentry.io/platforms/native/data-management/debug-files/" external>
            {t('Read the docs')}
          </Button>
        </Footer>
      </React.Fragment>);
    };
    return DebugFileDetails;
}(AsyncComponent));
export default DebugFileDetails;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(4), function (p) { return p.theme.fontSizeMedium; });
var GeneralInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"])));
var Label = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  padding: ", " ", " ", " ", ";\n"], ["\n  color: ", ";\n  ", "\n  padding: ", " ", " ", " ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; }, space(1), space(1.5), space(1), space(1));
var Value = styled(Label)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  padding: ", ";\n  font-family: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  color: ", ";\n  ", "\n  padding: ", ";\n  font-family: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; }, space(1), function (p) { return p.theme.text.familyMono; });
export var modalCss = css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 40%;\n      margin-left: -20%;\n    }\n  }\n"], ["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 40%;\n      margin-left: -20%;\n    }\n  }\n"])), theme.breakpoints[0]);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map