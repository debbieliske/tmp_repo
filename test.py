AzureDiagnostics
| where ResourceType == "SEARCHSERVICES"
| where OperationName == "Query.Search"
| where TimeGenerated >= ago(7d)
| summarize 
    TotalQueries = count(),
    SuccessfulQueries = countif(resultSignature_d == 200),
    FailedQueries = countif(resultSignature_d != 200)
    by IndexName_s, bin(TimeGenerated, 1h)
| extend 
    SuccessRate = (todouble(SuccessfulQueries) / todouble(TotalQueries)) * 100,
    FailureRate = (todouble(FailedQueries) / todouble(TotalQueries)) * 100
| project TimeGenerated, IndexName_s, SuccessRate, FailureRate, TotalQueries


AzureDiagnostics
| where ResourceType == "SEARCHSERVICES"
| where OperationName == "Query.Search"
| where TimeGenerated >= ago(7d)
| summarize CountByStatus = count() by IndexName_s, resultSignature_d
| project IndexName_s, resultSignature_d, CountByStatus


AzureDiagnostics
| where ResourceType == "SEARCHSERVICES"
| where OperationName == "Query.Search"
| where resultSignature_d == 429
| where TimeGenerated >= ago(7d)
| summarize ThrottledQueries = count() by IndexName_s, bin(TimeGenerated, 1h)
| project TimeGenerated, IndexName_s, ThrottledQueries


