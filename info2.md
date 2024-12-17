# Knowledge Transfer Document: Azure AI Search Pipeline

## 1. Overview of the Solution
The solution implements a Retrieval-Augmented Generation (RAG) pipeline to enhance document-based query responses for end users.

### Data Flow:
- **Source:** Documents, images, and HTML files are ingested from SharePoint Online.  
- **Storage:** Data is stored in **Azure Data Lake Gen2** as the centralized repository.  
- **Search:** Enriched and indexed data is stored in **Azure AI Search**, including:
  - Full-text content.  
  - Metadata fields.  
  - Vector embeddings for semantic search.  
- **Generation:** Queries are augmented with relevant search results and sent to **Azure OpenAI** for generating responses.

### Azure AI Search Role:
- Serves as the core retrieval store for both full-text and vector-based queries.  
- Enables advanced querying, filtering, and ranking of indexed documents.

---

## 2. Development Environment

- **Operating System:**  
  Windows machine with **Windows Subsystem for Linux (WSL)** for a Linux-compatible environment.  

- **Development Tool:**  
  **Visual Studio Code (VS Code)** was used as the integrated development environment (IDE).  

- **Programming Language:**  
  **Python** was used for scripting, automating workflows, and managing resources.  

- **Azure SDK for Python:**  
  Used for interacting with Azure services, including:
  - **Azure AI Search:** Index creation, indexer configuration, and querying.  
  - **Azure Data Lake Gen2:** Data source management and access.  
  - **Azure OpenAI:** Embedding generation using the `text-embedding-ada-002` model.  

- **Configuration:**
  - Python virtual environments (e.g., `venv`) were used for dependency isolation.  
  - **Azure CLI** was integrated to manage Azure resources programmatically.  
  - **Azure Key Vault** was used for securely managing API keys and credentials.  

---

## 3. Data Sources and Ingestion

- **Data Source:**  
  The data originates from **SharePoint Online**, serving as the primary repository for documents, images, and other content types.

- **Ingestion Process:**
  - Documents are pulled from SharePoint into **Azure Data Lake Gen2**.  
  - The **Azure AI Search indexer** connects to Azure Data Lake as its data source.  
  - Indexer runs process the raw data and apply skillsets to enrich content, ensuring completeness and structure.  

- **Supported File Types:**  
  PDFs, images, text files, and HTML content are handled by the skillset pipeline.

---

## 4. AI Search Index Configuration

### Index Schema:  
The following fields are defined in the search index to store enriched data, metadata, and embeddings:

| **Field**                | **Description**                                         |
|--------------------------|---------------------------------------------------------|
| `id`                     | Unique document identifier (key field).                 |
| `content`                | Unified, full-text searchable content of the document. |
| `embedding`              | Vector field containing embeddings generated via Azure OpenAI. |
| `metadata_author`        | Author metadata extracted from the document.           |
| `metadata_creationdate`  | Original creation date of the document.                |
| `metadata_moddate`       | Last modified date of the document.                    |
| `adls_file_link`         | Link to the document stored in Azure Data Lake Gen2.   |
| `raw_source_link`        | Link to the original source document (e.g., SharePoint location). |

### Vector Field Configuration:
- The `embedding` field is configured to store vector representations of the text, ensuring semantic search capability.  
- Dimensions match those of the `text-embedding-ada-002` model output.

### Field Types:
Each field is explicitly defined as searchable, filterable, sortable, or retrievable based on its purpose.

---

## 5. Skillset and Indexer Workflow

### Skillset Pipeline:
1. **OCR Text Extraction Skill:** Extracts visible text from images and scanned PDFs using Azure Cognitive Services.  
2. **Merge Skill:** Combines OCR-extracted text with raw document text into a unified content field.  
3. **Text Splitting Skill:** Breaks the unified content into smaller sections or pages for more granular indexing.  
4. **Embedding Generation Skill:** Generates vector embeddings for the split content using the Azure OpenAI `text-embedding-ada-002` model.

### Skill Execution Order:
**OCR → Merge → Split → Embed**

### Field Mapping and Index Projections:
Outputs from each skill (e.g., extracted text, embeddings) are mapped to specific fields in the index schema using index projections.

### Purpose of the Indexer:
- Connects the data source (Azure Data Lake), applies the skillset, and populates the index.  
- Handles incremental updates for new or modified content to ensure index freshness.

---

## 6. Query Execution and Integration

### Types of Queries:
- **Text-Based Queries:** Perform full-text searches on the `content` field.  
- **Vector-Based Queries:** Leverage embeddings stored in the `embedding` field to return semantically relevant results.  
- **Hybrid Queries:** Combine text and vector-based searches to improve relevance and accuracy.  

### Integration:
- **Azure AI Search** exposes REST APIs to allow external applications (e.g., Mendix) to query the index and retrieve results.  
- Retrieved results, including text and metadata, are formatted and appended to prompts sent to **Azure OpenAI** for response generation.

---

## 7. Monitoring and Logging

- **Azure Monitor:**  
  Configured to monitor key metrics such as query latency, indexer performance, and throughput.

- **Log Analytics:**  
  Captures detailed logs for indexing runs, query requests, and skillset execution errors.

- **Alerts:**  
  Alerts are configured for the following:
  - Indexer failures or skipped documents.  
  - High query latency.  
  - API usage spikes or anomalies.  

- **Dashboards:**  
  Dashboards in Azure Monitor provide real-time visibility into:
  - Query performance metrics.  
  - Indexer health and error rates.  
  - Resource consumption and usage trends.

---

## 8. Error and Warning Handling

### Common Errors:
- **Data Source Errors:** Issues accessing or reading from Azure Data Lake.  
- **Skillset Errors:** Failures during OCR, text merging, or embedding generation.  
- **Schema Mismatch Errors:** Outputs that do not align with index schema fields.  
- **Quota and Service Limit Errors:** API rate limits or exceeding index size quotas.  

### Impact and Mitigation:
- Partial data loss, failed indexing runs, or incomplete query results.  
- Logs and error alerts should be reviewed to identify root causes and apply fixes.

---

## 9. Security and Access Controls

- **Private Endpoints:** Ensure that Azure AI Search traffic flows securely within a VNet.  
- **RBAC (Role-Based Access Control):** Access permissions are assigned to manage and secure resources.  
- **API Key Management:** Keys are stored securely in Azure Key Vault and rotated periodically.  
- **Managed Identities:** Used to connect to Azure Data Lake and other services securely without exposing credentials.

---

## 10. Future Recommendations

- **Scaling:** Monitor query loads and scale replicas/partitions as needed.  
- **Advanced Ranking:** Introduce semantic rankers for more precise query results.  
- **Image Enhancements:** Add multimodal models for enhanced image embedding capabilities.  
- **Cost Optimization:** Continuously monitor service usage and refine indexer schedules to optimize costs.
