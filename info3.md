# Types of Errors and Warnings in Indexer Runs  

During indexer executions in **Azure AI Search**, errors or warnings may occur due to issues with the data source, skillset configuration, or indexing pipeline. This guide also includes whether the errors or warnings are silent and hard to detect, providing further insight into troubleshooting.  

---

## Data Source Errors  

**Description:** Errors occur when the indexer is unable to access or read from the specified data source.  

**Common Causes:**  
- **Invalid or Incorrect Data Source Configuration:** Issues with connection strings, paths, or permissions for Azure Data Lake.  
- **Missing Data:** Referenced files or blobs are missing from the specified location.  
- **Access Denied:** The indexer lacks permissions due to RBAC misconfigurations.  
- **Corrupt Data:** Data files are corrupted or unreadable.  

**Impact:**  
- Indexer skips documents or fails entirely, resulting in incomplete indexing.  
- Content may not appear in search queries, impacting downstream workflows.  

**Where to Find in Portal:**  
- **Indexer Results:** In the "Indexer Runs" section of the Azure AI Search blade, these errors will appear with messages such as "Data source unavailable" or "Access denied."  
- **Log Analytics:** Detailed logs in Log Analytics provide the exact data path or connection issue causing the failure.  

**Are These Errors Silent?**  
No, these errors are generally highly visible in the Indexer Runs section. Failures due to data source issues typically prevent the indexer from completing and trigger error messages.  

---

## Skillset Errors  

**Description:** Errors occur when a skill in the skillset fails to process input data or when the sequence of skill execution is incorrectly programmed.  

**Common Causes:**  
- **Invalid Input:** Incorrect formats passed to skills like OCR or text splitting.  
- **Missing Context:** The context path in the skill is incorrectly specified.  
- **Skill Configuration Issues:** Incorrect parameters or unsupported features (e.g., unsupported languages in OCR).  
- **Programming Mistake in Skill Order:**  
  - Skills executed in the wrong sequence, such as embedding generation being attempted before OCR or merge skill processing.  
  - Skills relying on outputs from previous steps receive incomplete or incorrect input, leading to downstream failures.  
- **Service Limits:** Exceeding Cognitive Services API limits (e.g., calls to Azure Computer Vision).  

**Impact:**  
- Skills fail to enrich documents, leading to incomplete or inaccurate indexed data.  
- Programming mistakes in skill order can result in:  
  - **Embeddings Generated from Partial or Invalid Text:** If embedding generation occurs before merging or splitting, embeddings might be created from incomplete content, reducing semantic search accuracy.  
  - **Missing Data:** Subsequent skills (e.g., text splitting) may fail due to incorrect inputs, leaving key content unindexed.  
  - **Performance Bottlenecks:** Misaligned skill sequences could lead to redundant processing or additional API calls.  

**Where to Find in Portal:**  
- **Indexer Results:** These errors or warnings may appear as skill-specific failures in the "Indexer Runs" section, with messages such as "Skill execution failed: Invalid input from previous step."  
- **Log Analytics:** Detailed logs can reveal the sequence of skill execution and pinpoint where errors occurred due to misplaced or incorrectly ordered skills.  

**Are These Errors Silent?**  
Partially Silent: Errors due to programming mistakes in skill order may not immediately trigger visible errors. Instead, they often manifest as:  
- Reduced quality in query results.  
- Warnings or partial successes in the "Indexer Runs" section, which may go unnoticed without thorough validation.  

---

## Document-Level Warnings  

**Description:** Warnings occur when the indexer processes a document but encounters a minor issue that does not prevent indexing.  

**Common Causes:**  
- **Partial Data Read:** Fields in the document may not conform to the schema.  
- **Skillset Failures for Part of a Document:** A specific skill fails on part of the document, but the rest is indexed successfully.  
- **Excessive Content:** Content exceeding size limits may be truncated.  

**Impact:**  
- Partial data is indexed, reducing search quality.  
- Document warnings may lead to incomplete metadata or missing enriched fields like embeddings.  

**Where to Find in Portal:**  
- **Indexer Results:** These warnings appear as partial successes in the "Indexer Runs" section, often labeled as "Document partially indexed."  
- **Dashboard Alerts:** If monitoring tools like Azure Monitor are configured, warnings for partial indexing will trigger alerts.  

**Are These Warnings Silent?**  
Yes, these warnings can be silent and hard to detect, as they do not cause the indexer to fail. They may only appear as minor messages in the Indexer Runs section or in logs, requiring proactive monitoring.  

---

## Index Schema Mismatch Errors  

**Description:** Errors caused when the enriched data does not match the expected schema of the target search index.  

**Common Causes:**  
- **Field Name Mismatch:** Skillset output maps to a field name not present in the index schema.  
- **Incorrect Field Types:** Data types in the skill output (e.g., string vs. numeric) do not align with index schema field types.  
- **Missing Required Fields:** Certain required fields, like `id` (document key), are not populated.  

**Impact:**  
- Documents fail to index entirely, leading to missing content.  
- Query results are incomplete, impacting user experience and downstream applications.  

**Where to Find in Portal:**  
- **Indexer Results:** Errors appear in the "Indexer Runs" section with messages such as "Field mapping error: Field type mismatch."  
- **Index Schema Blade:** Check the schema configuration in the Azure AI Search index schema settings for discrepancies.  

**Are These Errors Silent?**  
No, these errors are highly visible because they typically cause document indexing to fail. They appear prominently in the Indexer Runs section.  

---

## Incremental Indexer Warnings  

**Description:** Warnings occur during incremental updates when changes in the data source are not detected or handled properly.  

**Common Causes:**  
- **Untracked Changes:** Missing or improperly configured `lastModified` metadata in the data source.  
- **Skipped Documents:** Documents skipped due to unresolved errors in previous runs.  

**Impact:**  
- Newly ingested data may not appear in the search index.  
- Index freshness is reduced, leading to outdated query results.  

**Where to Find in Portal:**  
- **Indexer Runs:** Incremental update warnings are visible in the "Indexer Runs" section, often labeled as "Skipped document due to unchanged metadata."  
- **Log Analytics:** Detailed logs can help identify which documents or fields are causing issues with change tracking.  

**Are These Warnings Silent?**  
Yes, these warnings can be silent and often go unnoticed unless incremental enrichment logs are reviewed closely.  

---

## Quota and Service Limit Errors  

**Description:** Errors occur when Azure resource or service limits are exceeded.  

**Common Causes:**  
- **Quota Limits:** Hitting API quotas for Cognitive Services or Azure AI Search.  
- **High Index Size:** Exceeding partition size or number of documents in the index.  
- **Excessive Skill Execution:** High volume of calls to skills like OCR or embedding generation exceeds Cognitive Services limits.  

**Impact:**  
- Indexer runs may stop or fail entirely, resulting in incomplete indexing.  
- Increased costs due to excessive service usage.  

**Where to Find in Portal:**  
- **Usage and Quotas Blade:** Quota limits and usage statistics can be viewed in the Azure Cognitive Services Usage and Quotas section.  
- **Indexer Results:** Failures due to exceeded quotas appear in the "Indexer Runs" section with messages like "Quota exceeded."  
- **Azure Monitor:** Alerts and logs track API usage spikes and quota violations.  

**Are These Errors Silent?**  
No, these errors are typically highly visible because they prevent processing and trigger clear messages in both Indexer Runs and Usage and Quotas sections.  