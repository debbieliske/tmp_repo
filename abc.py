let DefaultTimeRange = 14d;
let QueryHealth = AzureDiagnostics
| where TimeGenerated > ago(DefaultTimeRange)
| where OperationName == "Query.Search"
| summarize 
    TotalCount = count(),
    SuccessCount = countif(ResultType == "Success"),
    SignatureBreakdown = count() by IndexName_s, ResultSignature_d
| extend SuccessRate = round(SuccessCount * 100.0 / TotalCount, 2)
| project IndexName_s, ResultSignature_d, SignatureBreakdown, SuccessRate, TotalCount
| order by TotalCount desc;
QueryHealth