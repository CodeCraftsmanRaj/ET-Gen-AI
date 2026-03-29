"""
AI Money Mentor - Chat Bridge
Connects Frontend to FastAPI Backend with Database Storage
Routes queries to appropriate agents
"""

import sqlite3
import requests
import json
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import HTTPException
from pydantic import BaseModel

# Database setup - use project's data directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'chat_history.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def init_db():
    """Initialize SQLite database for chat history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_session ON chat_messages(user_id, session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_messages(timestamp)')
    conn.commit()
    conn.close()

def store_message(user_id: str, session_id: str, agent_id: str, role: str, message: str):
    """Store a message in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_messages (user_id, session_id, agent_id, role, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, session_id, agent_id, role, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id: str, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve chat history for context"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, message, agent_id, timestamp
        FROM chat_messages
        WHERE user_id = ? AND session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, session_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse to get chronological order
    history = []
    for row in reversed(rows):
        history.append({
            'role': row['role'],
            'content': row['message'],
            'agent_id': row['agent_id'],
            'timestamp': row['timestamp']
        })
    return history

def send_to_agent(agent_id: str, message: str, session_id: str = None) -> str:
    """
    Send message to backend agent via HTTP
    
    Routes to appropriate agent endpoint based on agent_id
    """
    try:
        # Chat payloads are free-text. Use conversational endpoint for all agents.
        # This avoids 422 errors from strict calculator endpoints that require structured numeric bodies.
        endpoint = f"{BACKEND_URL}/ai/chat"

        # Backward-compatible agent aliases expected by /ai/chat
        ai_agent_alias = {
            "dhan-sarthi": "dhansarthi",
            "tax-master": "karvid",
            "retirement-pro": "yojana",
            "stock-insight": "bazaar",
            "money-health": "dhan",
            "compliance-helper": "vidhi",
            "portfolio-wise": "niveshak",
            "life-goals": "lifeevent",
            "partner-finance": "coupleplanner",
        }.get(agent_id, "dhansarthi")

        payload = {
            "message": message,
            "agent": ai_agent_alias,
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            return f"[Agent {agent_id} error: Status {response.status_code}]"
        
        # Parse the response
        try:
            data = response.json()
            # Extract the response text from various possible response formats
            if isinstance(data, dict):
                if "response" in data:
                    return data["response"]
                elif "message" in data:
                    return data["message"]
                elif "result" in data:
                    return str(data["result"])
                else:
                    return json.dumps(data, indent=2)
            return str(data)
        except:
            return response.text
        
    except requests.Timeout:
        return f"[Agent {agent_id} timed out after 30 seconds]"
    except requests.ConnectionError:
        return f"[Cannot connect to agent {agent_id} - backend offline at {BACKEND_URL}]"
    except Exception as e:
        return f"[Error reaching {agent_id}: {str(e)}]"

# FastAPI Models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: Optional[str] = None
    agent_id: str = 'dhan-sarthi'

class ChatResponse(BaseModel):
    agent: str
    response: str
    session_id: str
    history_count: int

# Initialize database on import
init_db()

# Export for FastAPI router
__all__ = ['ChatRequest', 'ChatResponse', 'init_db', 'store_message', 'get_chat_history', 'send_to_agent']