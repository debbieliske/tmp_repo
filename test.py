AzureDiagnostics
| where ResourceType == "SEARCHSERVICES"
| where OperationName == "SearchQuery"
| summarize 
    TotalQueries = count(),
    SuccessfulQueries = countif(HttpStatusCode == 200)
    by bin(TimeGenerated, 1h)
| extend ServiceAvailability = (todouble(SuccessfulQueries) / todouble(TotalQueries)) * 100
| project TimeGenerated, ServiceAvailability