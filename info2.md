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