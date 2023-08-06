import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { t } from 'app/locale';
export default function AwsLambdaFailureDetails(_a) {
    var lambdaFunctionFailures = _a.lambdaFunctionFailures;
    return (<Wrapper>
      <h3>{t('Failed to update the following Lambda Functions')}</h3>
      {lambdaFunctionFailures.map(function (func) {
        return <div key={func.FunctionName}>{func.FunctionName}</div>;
    })}
      <StyledButton priority="primary" href="?finish_pipeline=1">
        Finish
      </StyledButton>
    </Wrapper>);
}
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 20px;\n"], ["\n  margin: 20px;\n"])));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 50px;\n"], ["\n  margin: 50px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=awsLambdaFailureDetails.jsx.map