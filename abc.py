AzureDiagnostics
| where TimeGenerated > ago(DefaultTimeRange)
| where OperationName == "Query.Search"
| summarize TotalCount = count() by IndexName_s
| join kind=inner (
    AzureDiagnostics
    | where TimeGenerated > ago(DefaultTimeRange)
    | where OperationName == "Query.Search"
    | summarize Count = count() by IndexName_s, ResultType
) on IndexName_s
| extend Percent = round(Count * 100.0 / TotalCount, 2)
| project IndexName_s, ResultType, Count, Percent
| order by IndexName_s, Count desc