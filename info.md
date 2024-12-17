# Types of Errors and Warnings in Indexer Runs  

During indexer executions in **Azure AI Search**, errors or warnings may occur due to issues with the data source, skillset configuration, or indexing pipeline. Understanding these errors and their causes is essential for troubleshooting and ensuring a smooth data enrichment and indexing process.  

---

## Data Source Errors  
**Description:** Errors that occur when the indexer is unable to access or read from the specified data source.  

**Common Causes:**  
- **Invalid or Incorrect Data Source Configuration:** Incorrect connection strings, paths, or permissions for Azure Data Lake or other data sources.  
- **Missing Data:** Referenced files or blobs are missing in the specified location.  
- **Access Denied:** The indexer lacks permissions to access the data source (e.g., RBAC misconfigurations).  
- **Corrupt Data:** Data files are corrupted or unreadable.  

**Impact:**  
- The indexer may skip documents or fail entirely, resulting in incomplete indexing.  
- Content may not appear in search queries, impacting downstream workflows.  

---

## Skillset Errors  
**Description:** Errors that occur when a skill in the skillset fails to process input data.  

**Common Causes:**  
- **Invalid Input:** Skills such as OCR or text splitting receive input in an unexpected format (e.g., passing non-image data to an OCR skill).  
- **Missing Context:** The context path in the skill is incorrectly specified, causing the skill to fail when processing data.  
- **Skill Configuration Issues:** Incorrect parameters, such as unsupported languages in OCR or missing visual feature settings in image skills.  
- **Service Limits:** Hitting API limits for Cognitive Services (e.g., Azure Computer Vision).  

**Impact:**  
- Skills fail to enrich documents, leading to incomplete or inaccurate indexed data.  
- For example, missing text from images due to OCR failures could reduce search coverage and result relevance.  

---

## Document-Level Warnings  
**Description:** Warnings that occur when the indexer processes a document but encounters a minor issue that does not prevent indexing.  

**Common Causes:**  
- **Partial Data Read:** Certain fields in the document may not conform to the schema (e.g., unexpected data types or missing fields).  
- **Skillset Failures for Part of the Document:** A specific skill fails on part of the document (e.g., a single image within a PDF), but the rest of the document is indexed successfully.  
- **Excessive Content:** The document content exceeds maximum size limits for indexing, causing some sections to be truncated.  

**Impact:**  
- Partial data is indexed, but some content may be missing, which can reduce search quality.  
- Document warnings may lead to incomplete metadata or missing enriched fields like embeddings.  

---

## Index Schema Mismatch Errors  
**Description:** Errors caused when the enriched data does not match the expected schema of the target search index.  

**Common Causes:**  
- **Field Name Mismatch:** The skillset output is mapped to a field name that does not exist in the index schema.  
- **Incorrect Field Types:** The data type of the enriched output (e.g., string vs. numeric) does not align with the field type defined in the index.  
- **Missing Required Fields:** Certain required fields, like `id` (document key), are not populated during the indexing process.  

**Impact:**  
- Documents fail to index entirely, leading to missing content.  
- Query results are incomplete, impacting user experience and downstream applications.  

---

## Incremental Indexer Warnings  
**Description:** Warnings related to incremental updates when using incremental enrichment or scheduled runs.  

**Common Causes:**  
- **Untracked Changes:** New or updated documents are not detected due to missing tracking information (e.g., `lastModified` metadata not updated).  
- **Skipped Documents:** Some documents may be skipped due to unresolved errors in previous runs.  

**Impact:**  
- Newly ingested data may not appear in the search index.  
- Index freshness is reduced, leading to outdated query results.  

---

## Quota and Service Limit Errors  
**Description:** Errors that occur when Azure resource or service limits are exceeded.  

**Common Causes:**  
- **Quota Limits:** Hitting indexer throughput limits, document size restrictions, or API call quotas.  
- **High Index Size:** Index grows beyond the limits of the Azure AI Search tier (e.g., S1, S2).  
- **Excessive Skill Execution:** High volume of calls to skills like OCR or embedding generation exceeds Cognitive Services quotas.  

**Impact:**  
- Indexer runs may stop or fail entirely, resulting in incomplete indexing.  
- Costs may increase significantly due to excessive usage of Cognitive Services APIs.  

---

## Impact Summary Table  

| **Error/Warning Type**          | **Cause**                                  | **Impact**                                           |  
|---------------------------------|-------------------------------------------|-----------------------------------------------------|  
| **Data Source Errors**          | Misconfigurations, missing files          | Indexer skips documents or fails completely.        |  
| **Skillset Errors**             | Invalid input, context, or configuration  | Missing enrichments like OCR or embeddings.         |  
| **Document Warnings**           | Partial failures, excessive content       | Partial data indexed, reducing search quality.      |  
| **Schema Mismatch Errors**      | Name/type mismatch or missing fields      | Documents fail to index.                            |  
| **Incremental Update Warnings** | Missing change tracking or skips          | Index freshness reduced.                            |  
| **Quota/Service Limit Errors**  | Hitting API, throughput, or size limits   | Indexer stops; costs may increase.                  |  

---

## How to Mitigate These Errors  

### Data Source Errors  
- Verify connection strings, permissions, and data paths.  
- Set up monitoring to identify missing or corrupt data files.  

### Skillset Errors  
- Validate skill inputs, contexts, and parameters.  
- Monitor Cognitive Services quotas and optimize skill execution.  

### Document Warnings  
- Break large documents into smaller pieces for processing.  
- Address schema issues to ensure all fields align.  

### Schema Mismatch Errors  
- Review index schema and ensure skillset outputs map correctly.  
- Log errors to identify missing or incorrect field mappings.  

### Quota and Service Limits  
- Scale Azure AI Search resources (replicas and partitions) as needed.  
- Monitor Cognitive Services usage and adjust indexing schedules to avoid spikes.  

---

## Summary  
Understanding these errors and warnings during indexer runs is essential for maintaining a reliable and efficient **Azure AI Search** pipeline. By identifying root causes and applying targeted fixes, issues like incomplete indexing, missing enrichments, and performance bottlenecks can be mitigated to ensure smooth operations and high-quality search results.