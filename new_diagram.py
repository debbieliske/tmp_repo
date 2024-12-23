# Creating an updated architecture diagram based on new specifications

from graphviz import Digraph
from IPython.display import Image, display

# Define the advanced multi-agent architecture diagram
updated_diagram = Digraph(name='Advanced Multi-Agent Chat System')

# Frontend
updated_diagram.node('UI', 'Chat UI', shape='rectangle', style='filled', color='lightblue')

# Core Agents
updated_diagram.node('Orchestrator', 'Orchestrator\n- Route Prompts\n- Aggregate Responses\n- Stateless Routing',
                     shape='ellipse', style='filled', color='lightgreen')
updated_diagram.node('DataInsights', 'Data Insights (DI)\n- Query Structured Data\n- SQL Query on CSV',
                     shape='ellipse', style='filled', color='lightgreen')
updated_diagram.node('EnterpriseSearch', 'Enterprise Search (ES)\n- Query Unstructured Data\n- Image Text Extraction',
                     shape='ellipse', style='filled', color='lightgreen')
updated_diagram.node('ReportGeneration', 'Report Generation\n- Summarize Responses\n- Create Reports',
                     shape='ellipse', style='filled', color='lightgreen')
updated_diagram.node('PromptServices', 'Prompt Services\n- Standardize Prompts',
                     shape='ellipse', style='filled', color='lightcoral')
updated_diagram.node('UserServices', 'User Services\n- Manage Session\n- Handle Preferences',
                     shape='ellipse', style='filled', color='lightcoral')

# Chat History and State Management
updated_diagram.node('ChatHistoryManager', 'Chat History Manager\n- Unified Chat History\n- Manage Context',
                     shape='ellipse', style='filled', color='lightgreen')
updated_diagram.node('SharedAPI', 'Shared API\n- Fetch/Update Context\n- Multi-Agent Queries',
                     shape='ellipse', style='filled', color='lightcoral')

# Storage Layers
updated_diagram.node('SQLDB', 'SQL Database\n- Store Chat History\n- Session Metadata',
                     shape='cylinder', style='filled', color='lightyellow')
updated_diagram.node('VectorDB', 'Vector Database (Embeddings)\n- Store/Retrieve Embeddings',
                     shape='cylinder', style='filled', color='lightyellow')

# Monitoring
updated_diagram.node('Monitoring', 'Monitoring & Logging\n- Track Performance\n- Log Errors',
                     shape='ellipse', style='dashed', color='grey')

# Define Data Flow
updated_diagram.edge('UI', 'UserServices', label='User Query / Follow-Up')
updated_diagram.edge('UserServices', 'PromptServices', label='Format Query')
updated_diagram.edge('PromptServices', 'Orchestrator', label='Standardized Query')
updated_diagram.edge('Orchestrator', 'ChatHistoryManager', label='Fetch Chat History')
updated_diagram.edge('Orchestrator', 'DataInsights', label='Route to DI')
updated_diagram.edge('Orchestrator', 'EnterpriseSearch', label='Route to ES')
updated_diagram.edge('DataInsights', 'ReportGeneration', label='Send Structured Data Response')
updated_diagram.edge('EnterpriseSearch', 'ReportGeneration', label='Send Unstructured Data Response')
updated_diagram.edge('ReportGeneration', 'ChatHistoryManager', label='Store Aggregated Response')
updated_diagram.edge('ChatHistoryManager', 'SQLDB', label='Persist Chat History')
updated_diagram.edge('SQLDB', 'ChatHistoryManager', label='Retrieve Relevant History')
updated_diagram.edge('EnterpriseSearch', 'VectorDB', label='Store/Retrieve Embeddings')
updated_diagram.edge('VectorDB', 'EnterpriseSearch', label='Provide Embeddings')
updated_diagram.edge('Orchestrator', 'SharedAPI', label='Fetch/Update Context')
updated_diagram.edge('SharedAPI', 'ChatHistoryManager', label='Manage Shared History')
updated_diagram.edge('ChatHistoryManager', 'Monitoring', label='Log Operations')
updated_diagram.edge('Orchestrator', 'Monitoring', label='Log Routing')
updated_diagram.edge('EnterpriseSearch', 'Monitoring', label='Log ES Actions')
updated_diagram.edge('DataInsights', 'Monitoring', label='Log DI Actions')
updated_diagram.edge('ReportGeneration', 'Monitoring', label='Log Reporting Actions')
updated_diagram.edge('Orchestrator', 'UI', label='Return Response')

# Context Reset Flow
updated_diagram.edge('UI', 'SharedAPI', label='Reset Context Command')
updated_diagram.edge('SharedAPI', 'ChatHistoryManager', label='Clear Chat History')

# Generate and render diagram
diagram_path_updated = '/mnt/data/updated_multi_agent_architecture'
updated_diagram.render(diagram_path_updated, format='png')

# Display the updated diagram
display(Image(filename=f'{diagram_path_updated}.png'))
