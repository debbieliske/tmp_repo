
# Chat History Utility Functions

## Utility Module (Reusable Across Agents)
### File: chat_history_utils.py

```python
import sqlite3

def store_chat_history(session_id, chat_id, user_query, response, source_agent, aggregated_response, timestamp):
    # SQL Logic to store chat history
    pass

def fetch_chat_history(session_id, limit=10):
    # SQL Logic to retrieve recent chat history
    pass

def clear_chat_history(session_id):
    # SQL Logic to clear chat history for a session
    pass
```

---

## Example API Endpoints for Chat History Manager Agent

### Store Chat History
```
POST /store_chat_history
```

### Fetch Chat History
```
GET /fetch_chat_history?session_id=<id>&limit=10
```

### Clear Chat History
```
DELETE /clear_chat_history?session_id=<id>
```

---

## Example API Call from Data Insights Agent

```python
import requests

def retrieve_chat_history(session_id):
    response = requests.get(f"http://chat-history-service/fetch_chat_history?session_id={session_id}&limit=10")
    return response.json()
```

---

## Example Local Implementation Inside Agent

```python
def store_chat_history(session_id, chat_id, query, response, agent):
    with sqlite3.connect('chat_history.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (session_id, chat_id, query, response, source_agent) VALUES (?, ?, ?, ?, ?)",
            (session_id, chat_id, query, response, agent)
        )
    conn.commit()
```
