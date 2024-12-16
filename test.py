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


AzureDiagnostics
| where ResourceType == "SEARCHSERVICES"
| where OperationName == "Query.Search"
| extend HourOfDay = tostring(format_datetime(todatetime(TimeGenerated), "HH"))
| extend DayOfWeek = dayofweek(todatetime(TimeGenerated))
| summarize QueryCount = count() by HourOfDay, DayOfWeek
| project HourOfDay, DayOfWeek, QueryCount


USAGE METRICS
Total Queries Over Time

AzureDiagnostics
| where ResourceType == "SEARCHSERVICE"
| where OperationName == "Query.Search"
| summarize TotalQueries = count() by bin(TimeGenerated, 1h)
| project TimeGenerated, TotalQueries

Top Search Terms
AzureDiagnostics
| where ResourceType == "SEARCHSERVICE"
| where OperationName == "Query.Search"
| extend SearchTerm = tostring(Properties["searchText"])  // Replace with the correct property for search terms
| summarize Count = count() by SearchTerm
| top 10 by Count
| project SearchTerm, Count

Indexing Pipeline Performance
Indexer Success/Failure Rate 

AzureDiagnostics
| where ResourceType == "SEARCHSERVICE"
| where OperationName == "Indexer.Run"
| summarize SuccessCount = countif(HttpStatusCode == 200), FailureCount = countif(HttpStatusCode != 200) by bin(TimeGenerated, 1h)
| project TimeGenerated, SuccessCount, FailureCount

Documents per Indexer Run
AzureDiagnostics
| where ResourceType == "SEARCHSERVICE"
| where OperationName == "Indexer.Run"
| extend DocumentsProcessed = toint(Properties["documentCount"])  // Replace with the correct property for documents processed
| summarize AvgDocuments = avg(DocumentsProcessed) by bin(TimeGenerated, 1h)
| project TimeGenerated, AvgDocuments