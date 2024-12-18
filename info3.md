# Skillsets and Indexer Workflow

## Overview of the Skillset Process
The skillset in Azure AI Search consists of sequential steps (skills) that process and enrich data for indexing. The order of execution is crucial because each skill builds on the output of the previous step, ensuring that all extracted and enriched content flows logically and cohesively into the index.

### OCR Text Extraction Skill
- **Purpose**: Extracts text content from images, scanned PDFs, or visual content using Optical Character Recognition (OCR).
- **Input**: Raw images, scanned PDFs, or other documents stored in Azure Data Lake Gen2.
- **Output**: Extracted text from images, which is made available for subsequent processing.
- **Why This is First**: OCR ensures that all visible text content is captured and enriched before any merging or splitting occurs. This is critical for documents where content exists primarily in image form.

### Text Merge Skill
- **Purpose**: Combines the text extracted via OCR with any pre-existing raw text content in the document to create a single, unified version of the content.
- **Input**:
  - OCR-extracted text output from the first step.
  - Raw document text from the data source.
- **Output**: A merged version of the document content that integrates both OCR results and raw data.
- **Why This is Second**: Merging immediately after OCR ensures that both structured (text) and unstructured (OCR-extracted) data are seamlessly consolidated before further processing, reducing redundancy and ensuring completeness.

### Text Splitting Skill
- **Purpose**: Splits the merged text into smaller, manageable chunks, such as logical sections or pages. This improves the granularity of indexing and enables better retrieval results.
- **Input**: Unified content output from the merge skill.
- **Output**: Smaller sections or pages of text that are optimized for indexing and embedding generation.
- **Why This is Third**: Splitting content after merging ensures that the OCR-enriched data and raw text are evenly distributed and logically broken down, making it easier to process, store, and search.

### Embedding Generation Skill
- **Purpose**: Generates semantic embeddings from the split content using the Azure OpenAI model (text-embedding-ada-002). These embeddings enable vector-based search for highly relevant results.
- **Input**: Split content from the previous step.
- **Output**: Numerical embeddings (vectors) stored in a designated vector field in the search index.
- **Why This is Last**: Embeddings must be generated from the final, cleaned, and structured content to ensure high quality and semantic relevance for search.

## Skill Execution Order and Information Flow
The order of skill execution ensures proper enrichment and logical processing of document content:
- **OCR Extraction**: Captures visible text content from images and scanned files.
- **Text Merge**: Combines OCR-extracted text with raw document text to create a unified version of the content.
- **Text Splitting**: Breaks the unified text into smaller, structured chunks for better indexing and embedding generation.
- **Embedding Generation**: Creates vector embeddings from the final, split content to enable semantic search.

### Data Flow Summary
Input → OCR Skill → Extracted text → Merge Skill → Unified content → Text Splitting → Logical chunks → Embedding Skill → Vector embeddings.

## Understanding the Offset Parameter in the Merge Skill
- **Definition**: The offset parameter determines the starting position for merging text content, ensuring that the newly appended content is aligned logically with the existing content.
- **Purpose**:
  - Ensures there are no overlaps or logical inconsistencies when merging text extracted by OCR with raw text data.
  - Allows sequential appending of content, especially useful when handling paginated data or partial merges.

## Impact of the Offset
- Without a proper offset, content may overwrite or misalign during the merge process.
- Correct offsets ensure that the final text output flows logically and retains the correct structure.

## Purpose of the Indexer
The indexer acts as the orchestrator, connecting the data source, skillset, and index to automate data ingestion, enrichment, and indexing.

### Components of the Indexer
- **Data Source**: The input source where raw files and documents reside (e.g., Azure Data Lake).
- **Skillset**: A pipeline of sequential skills (OCR, merge, splitting, embeddings) that process and enrich the data.
- **Index**: The target location where enriched data, including content, metadata, and embeddings, is stored for querying.

### Workflow
- The indexer pulls raw data from the data source.
- The skillset processes the data in the defined order (OCR → Merge → Split → Embed).
- The enriched and processed data is stored in the search index.
- **Incremental Updates**: If enabled, the indexer processes only new or modified documents, ensuring efficient updates.