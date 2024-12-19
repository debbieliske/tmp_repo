# Epic: Enable Follow-Up Questions in Chat History

As a user, I want the application to maintain context across multiple interactions so that I can ask follow-up questions without repeating previous queries.

---

## 1. Store and Retrieve Chat History

### Story
As a user, I want the application to remember the context of my previous interactions so that it can provide consistent answers to follow-up questions.

### Acceptance Criteria
- Chat history is stored in the MySQL database as part of the payload (including session ID, user query, and response).
- The application retrieves relevant chat history during every user interaction.

### What Needs to Happen in the Code
1. **Database Schema**:
   - Design a MySQL table to store chat history, including fields like `session_id`, `chat_id`, `user_query`, `response`, and `timestamp`.
2. **Storage Logic**:
   - Implement a function to save the chat history after every user interaction.
3. **Retrieval Logic**:
   - Develop a function to retrieve the full chat history or relevant parts for a session using `session_id`.

---

## 2. Maintain Session Context

### Story
As a user, I want my session to persist across multiple requests so that the app knows what we have discussed in this conversation.

### Acceptance Criteria
- Each session is assigned a unique session ID that is maintained for the duration of the chat.
- The session ID is linked to the payload stored in MySQL.

### What Needs to Happen in the Code
1. **Session ID Generation**:
   - Generate and assign a unique session ID for each user session.
2. **Session Persistence**:
   - Store the session ID on the client side (e.g., using cookies or a token) and send it with every request.
3. **Context Association**:
   - Ensure each interaction is tagged with the correct session ID during storage and retrieval.

---

## 3. Enhance Query Understanding with Chat History

### Story
As a user, I want the application to use my previous questions and responses to better understand my follow-up queries.

### Acceptance Criteria
- The application combines embeddings for the current query with relevant embeddings from chat history stored in Databricks.
- The embeddings are retrieved and ranked for relevance to construct a meaningful response.

### What Needs to Happen in the Code
1. **Fetch Relevant History**:
   - Use the session ID to retrieve the last `n` queries and responses from MySQL.
2. **Embed Historical Context**:
   - Use Databricks to retrieve embeddings for historical queries and combine them with the current query's embeddings.
3. **Augmented Query Creation**:
   - Concatenate or augment the current query with the historical context for the LLM to process.

---

## 4. Support Multi-Agent Context Sharing

### Story
As a user, I want different agents to access shared context so that I can seamlessly interact with various functionalities without losing the chat history.

### Acceptance Criteria
- Each agent retrieves the same shared context (via session ID and chat history from MySQL) before processing a user query.
- Agents update the chat history after their response is generated.

### What Needs to Happen in the Code
1. **Shared API**:
   - Develop a REST API that allows agents to fetch and update chat history using the session ID.
2. **Agent Integration**:
   - Ensure each agent container has logic to query the API for context at the beginning of processing.
3. **Payload Updates**:
   - Update the shared chat history payload after the agent completes its task.

---

## 5. Handle Chat History Limits

### Story
As a user, I want the application to prioritize recent context if the chat history is too long so that the app remains responsive and relevant.

### Acceptance Criteria
- The chat history retrieval is limited to the most recent `n` interactions or based on a relevancy score.
- Old or irrelevant entries are archived or ignored during query processing.

### What Needs to Happen in the Code
1. **Retrieve Limited Context**:
   - Implement logic to fetch only the last `n` interactions from MySQL or filter by relevance (e.g., using embedding similarity).
2. **Archive Old History**:
   - Create a mechanism to archive or prune older history to maintain database performance.
3. **Fallback Mechanism**:
   - Handle scenarios where no relevant history is available gracefully.

---

## 6. Provide User Feedback for Follow-Up Questions

### Story
As a user, I want to see which part of my previous conversation is being referenced in the follow-up response so that I understand the app’s reasoning.

### Acceptance Criteria
- The response includes a reference to the specific query or context used from the chat history.
- Users can request to "clear context" to start a fresh conversation.

### What Needs to Happen in the Code
1. **Reference Matching**:
   - Track which part of the chat history was used to generate the response.
2. **Response Annotation**:
   - Append metadata to the LLM response indicating the referenced query or context.
3. **Frontend Update**:
   - Modify the frontend to display highlighted references or context summaries alongside the response.

---

## 7. Enable Context Reset

### Story
As a user, I want to clear my session's chat history so that I can ask unrelated questions without confusion.

### Acceptance Criteria
- A "Reset Context" button or command clears the session ID and removes stored context for the current chat.

### What Needs to Happen in the Code
1. **API Endpoint**:
   - Add an endpoint to clear the session’s chat history from MySQL.
2. **Session Reset Logic**:
   - Reset the session ID or clear its association with the chat history.
3. **Frontend Action**:
   - Add a button or command in the UI to trigger the reset process.

---

## 8. Debug and Monitor Chat History Management

### Story
As a developer, I want to monitor chat history storage and retrieval so that I can identify and fix issues quickly.

### Acceptance Criteria
- Logging is implemented for chat history retrieval and updates.
- Metrics (e.g., retrieval time, storage size) are tracked using Azure Monitor or a similar tool.

### What Needs to Happen in the Code
1. **Logging**:
   - Add logs for chat history read and write operations (e.g., session ID, query, retrieval time).
2. **Monitoring**:
   - Use Azure Monitor or similar tools to collect and display metrics on chat history usage.
3. **Error Handling**:
   - Add error-handling mechanisms to log and recover from issues like failed database queries or retrieval timeouts.

---

## 9. Secure Chat History

### Story
As a user, I want my chat history to remain private so that only authorized agents and services can access it.

### Acceptance Criteria
- Chat history stored in MySQL is encrypted.
- Access to chat history is controlled via Azure RBAC (Role-Based Access Control) or similar mechanisms.

### What Needs to Happen in the Code
1. **Encryption**:
   - Encrypt sensitive data in the MySQL database using AES or another secure encryption mechanism.
2. **Access Control**:
   - Use Azure Role-Based Access Control (RBAC) to ensure only authorized agents and services can access chat history.
3. **API Security**:
   - Secure the API endpoints with OAuth2, API keys, or similar authentication mechanisms.
