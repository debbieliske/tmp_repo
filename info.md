# Azure RAG App Cutover Checklist

## 1. Environment Configuration
- **Production Azure Resource Group** is created and aligned with proper naming conventions.
- Azure services used (e.g., Azure Cognitive Search, Azure OpenAI, Blob Storage, Azure Functions) are deployed to the production subscription.
- **Endpoints** for production Azure OpenAI and Cognitive Search are configured.
- Appropriate Azure **regions** are selected for performance and compliance needs.
- Azure **Access Keys** and **Connection Strings** are securely stored using **Azure Key Vault**.

---

## 2. Data Preparation and Indexing
- All documents or knowledge sources are **cleaned**, **pre-processed**, and finalized.
- Data ingestion pipeline (using Azure Blob Storage, Azure Cognitive Search Indexers, etc.) is configured for production data.
- Production **Cognitive Search Index** is set up with optimized schema (including fields for embeddings, filters, and metadata).
- Indexing has been **completed successfully**, and data availability is verified.

---

## 3. Azure OpenAI Service
- Production **OpenAI models** (e.g., GPT-4, GPT-3.5) are deployed with appropriate quotas.
- Model deployment is tested for latency and throughput at production levels.
- **Prompt Engineering** is finalized for accuracy and consistency.
- Rate limits and token quotas are reviewed for anticipated load.

---

## 4. Application Performance and Scalability
- Conduct **load testing** to ensure the app can handle production traffic.
- Autoscaling rules are implemented for compute resources (e.g., Azure Kubernetes Service, Azure App Service).
- Monitor latency of RAG pipeline components (retrieval, generation, API response).
- Implement **caching strategies** where applicable to reduce load on the search index and OpenAI model.

---

## 5. Security and Compliance
- **Role-Based Access Control (RBAC)** is configured for Azure resources.
- All sensitive credentials (e.g., API keys, secrets) are managed securely in **Azure Key Vault**.
- **Network Security**: Enable Azure Virtual Networks (VNet), Private Endpoints, or IP whitelisting to secure access.
- Enable **encryption at rest and in transit** for all services.
- Conduct a **security review** and ensure compliance with relevant standards (e.g., GDPR, HIPAA).

---

## 6. Monitoring and Logging
- Enable **Azure Monitor** and configure log analytics for all services.
- Set up **Application Insights** to monitor app performance, failures, and user behavior.
- Implement alerts for critical metrics such as latency, failures, or resource consumption.
- Logging is configured for:
    - Retrieval process (Cognitive Search)
    - API calls to Azure OpenAI
    - Backend components

---

## 7. Backup and Disaster Recovery
- Configure backups for Azure Blob Storage and Cognitive Search indexes.
- Set up disaster recovery processes with geo-replication for critical Azure services.
- Test failover and recovery processes.

---

## 8. Cost Optimization
- Review production costs using **Azure Cost Management**.
- Right-size Azure resources to avoid over-provisioning.
- Implement quotas and budget alerts for cost management.

---

## 9. Production Deployment
- CI/CD pipelines are configured (e.g., using **Azure DevOps** or GitHub Actions) to deploy changes safely.
- Production **environment variables** are configured properly (API keys, endpoints).
- Conduct a final round of **User Acceptance Testing (UAT)** in production-like conditions.
- **Go/No-Go Review** is completed with all stakeholders.

---

## 10. Post-Cutover Monitoring
- Monitor Azure OpenAI token usage and Cognitive Search query performance.
- Verify **end-to-end RAG pipeline** for accuracy and latency.
- Continuously review logs, metrics, and alerts during the stabilization period.
- Gather feedback and optimize prompt tuning or indexing performance as needed.

---

## Tools and Documentation
- Use **Azure Resource Manager (ARM)** templates or **Bicep** for repeatable infrastructure deployment.
- Maintain clear **runbooks** for operational procedures (e.g., scaling, troubleshooting).
- Update documentation for production processes, including API endpoints, usage limits, and maintenance plans.

---

## Optional Additions
- Conduct a **penetration test** or security audit before full production launch.
- Enable **Azure Policy** to enforce compliance standards on Azure resources.
