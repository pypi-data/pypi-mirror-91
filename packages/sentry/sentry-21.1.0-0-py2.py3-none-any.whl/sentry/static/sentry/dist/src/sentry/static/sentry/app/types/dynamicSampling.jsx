export var DynamicSamplingRuleType;
(function (DynamicSamplingRuleType) {
    /**
     * The rule applies to traces (transaction events considered in the context of a trace)
     */
    DynamicSamplingRuleType["TRACE"] = "trace";
    /**
     *  The rule applies to transaction events considered independently
     */
    DynamicSamplingRuleType["TRANSACTION"] = "transaction";
    /**
     * The rule applies to error events (not transaction events)
     */
    DynamicSamplingRuleType["ERROR"] = "error";
})(DynamicSamplingRuleType || (DynamicSamplingRuleType = {}));
export var DynamicSamplingConditionOperator;
(function (DynamicSamplingConditionOperator) {
    /**
     * It uses glob matches for checking (e.g. releases use glob matching "1.1.*" will match release 1.1.1 and 1.1.2)
     */
    DynamicSamplingConditionOperator["GLOB_MATCH"] = "globMatch";
    /**
     * It uses simple equality for checking
     */
    DynamicSamplingConditionOperator["EQUAL"] = "equal";
    /**
     * It uses a case insensitive string comparison
     */
    DynamicSamplingConditionOperator["STR_EQUAL_NO_CASE"] = "strEqualNoCase";
})(DynamicSamplingConditionOperator || (DynamicSamplingConditionOperator = {}));
//# sourceMappingURL=dynamicSampling.jsx.map