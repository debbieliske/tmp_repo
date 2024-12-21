
# 🚀 Solution 2: Comprehensive Monitoring Design for Search Service and OpenAI (Azure AI Services)

This solution extends **Solution 1** to comprehensively monitor both **Search Service (`SEARCHSERVICES`)** and **OpenAI (`ACCOUNTS`)**, ensuring visibility into indexing, querying, and AI-powered enrichment processes.

---

## 📊 1. Workbook Structure (Deep Dive & Analysis)

The **Workbook** serves as your **central hub** for analytics, troubleshooting, and detailed insights. 

### 📚 Workbook Sections Overview

| **Section Name**          | **Primary ResourceType** | **Focus**                                  |
|----------------------------|--------------------------|--------------------------------------------|
| 🚦 **Pipeline Health Overview** | Both (`SEARCHSERVICES`, `ACCOUNTS`) | High-level KPIs and health metrics.        |
| 📈 **Indexing Performance Trends** | `SEARCHSERVICES` | Indexer latency, throughput, and error rates. |
| 🛠️ **Indexer Status**       | `SEARCHSERVICES`       | Individual indexer health and errors.      |
| 📑 **Index Details**        | `SEARCHSERVICES`       | Document count, index growth, freshness.   |
| 🧠 **Skillset Performance**  | `ACCOUNTS`            | AI enrichment performance and errors.      |
| ⚠️ **Error Analysis**       | Both                  | Common errors across both services.        |
| 🔍 **Query Performance**    | `SEARCHSERVICES`       | Query latency, success rates, and anomalies. |
| 📊 **Resource Utilization**  | Both                  | CPU, memory, and network usage trends.     |
| 📅 **Timeline and Changes** | Both                  | Configuration changes and significant events. |

---

## 🛠️ 2. Workbook Section Details and KQL Queries

Below are the sections, their purposes, and sample KQL queries for each.

### 🚦 1. Pipeline Health Overview

**🔍 Focus:** Provide a high-level health summary for both Search Service and AI Services.

#### ✅ Tile 1: Error Count Across Both Services
**Visualization:** KPI Card  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType in ("SEARCHSERVICES", "ACCOUNTS")
| summarize ErrorCount = countif(Level == "Error") by ResourceType
```

#### ✅ Tile 2: Average Latency Across Both Services
**Visualization:** KPI Card  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType in ("SEARCHSERVICES", "ACCOUNTS")
| summarize AvgLatency = avg(DurationMs) by ResourceType
```

#### ✅ Tile 3: Health Distribution by Resource Type
**Visualization:** Pie Chart  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType in ("SEARCHSERVICES", "ACCOUNTS")
| summarize HealthStatus = count() by ResourceType, Level
```

---

### 📈 2. Indexing Performance Trends

**🔍 Focus:** Monitor document indexing throughput, latency, and trends over time.

#### ✅ Tile 4: Documents Indexed Over Time
**Visualization:** Timechart  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "SEARCHSERVICES"
| where OperationName contains "Index"
| summarize DocumentCount = count() by bin(TimeGenerated, 1h)
```

#### ✅ Tile 5: Indexing Latency Trends
**Visualization:** Timechart  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "SEARCHSERVICES"
| where OperationName contains "Index"
| summarize AvgLatency = avg(DurationMs) by bin(TimeGenerated, 1h)
```

---

### 🛠️ 3. Indexer Health

**🔍 Focus:** Highlight errors and health of individual indexers.

#### ✅ Tile 6: Top Indexer Errors
**Visualization:** Bar Chart  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "SEARCHSERVICES"
| where OperationName contains "Index"
| summarize ErrorCount = countif(Level == "Error") by IndexerName_s
| order by ErrorCount desc
```

#### ✅ Tile 7: Indexer Performance Overview
**Visualization:** Table  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "SEARCHSERVICES"
| summarize AvgDuration = avg(DurationMs), ErrorCount = countif(Level == "Error") by IndexerName_s
| order by ErrorCount desc
```

---

### 🧠 4. Skillset Performance

**🔍 Focus:** Monitor the health and performance of AI skillsets.

#### ✅ Tile 8: Top Skillset Errors
**Visualization:** Table  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "ACCOUNTS"
| where OperationName contains "Skillset"
| summarize ErrorCount = countif(Level == "Error") by SkillsetName_s
| order by ErrorCount desc
```

#### ✅ Tile 9: Skillset Execution Time
**Visualization:** Timechart  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType == "ACCOUNTS"
| where OperationName contains "Skillset"
| summarize AvgExecutionTime = avg(DurationMs) by bin(TimeGenerated, 1h)
```

---

### ⚠️ 5. Error Overview

**🔍 Focus:** Display the most frequent errors across both services.

#### ✅ Tile 10: Top Errors Across Both Services
**Visualization:** Table  
**Query:**
```kql
AzureDiagnostics
| where TimeGenerated > ago(14d)
| where ResourceType in ("SEARCHSERVICES", "ACCOUNTS")
| where Level == "Error"
| summarize ErrorCount = count() by ErrorMessage_s, ResourceType
| order by ErrorCount desc
```

---

# Final Steps

- Validate Logs and Queries.
- Build Workbook and Dashboard Sections.
- Pin Critical Insights to the Dashboard.
