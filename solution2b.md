# Create a Markdown file with Solution 2 including time range flexibility for Dashboard

markdown_content = """
# 🚀 Solution 2: Comprehensive Monitoring Design for Search Service and OpenAI (Azure AI Services)

This solution extends **Solution 1** to comprehensively monitor both **Search Service (`SEARCHSERVICES`)** and **OpenAI (`ACCOUNTS`)**, ensuring visibility into indexing, querying, and AI-powered enrichment processes.

**Time Range Configuration:**  
- The default time range is **14 days** (`14d`).  
- If a **global time picker** is selected on the dashboard, it will override the default time range.

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
let DefaultTimeRange = 14d;
AzureDiagnostics
| where TimeGenerated > ago(DefaultTimeRange) or TimeGenerated between (datetime({start_time}) .. datetime({end_time}))
| where ResourceType in ("SEARCHSERVICES", "ACCOUNTS")
| summarize ErrorCount = countif(Level == "Error") by ResourceType
