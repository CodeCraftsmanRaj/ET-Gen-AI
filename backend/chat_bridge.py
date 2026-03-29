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
from dotenv import load_dotenv

from fastapi import HTTPException
from pydantic import BaseModel

backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(backend_dir, ".env"), override=False)
load_dotenv(os.path.join(os.path.dirname(backend_dir), ".env"), override=False)

# Database setup - use project's data directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'chat_history.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

AGENT_PROMPTS = {
    "dhan-sarthi": "You are DhanSarthi, the AI coordinator for personal finance in India. Be concise and practical.",
    "tax-master": "You are TaxMaster, Indian tax advisor. Explain old/new regime, deductions, and legal tax optimization.",
    "retirement-pro": "You are RetirementPro, FIRE and retirement planner. Use clear assumptions and practical SIP guidance.",
    "stock-insight": "You are StockInsight. Provide educational market insights and include a SEBI caution.",
    "portfolio-wise": "You are PortfolioWise. Explain mutual fund portfolio risk, diversification, and rebalancing ideas.",
    "money-health": "You are MoneyHealth. Assess savings, debt, emergency fund, and actionable steps.",
    "compliance-helper": "You are ComplianceHelper. Give concise compliance/regulatory guidance with disclaimers.",
    "life-goals": "You are LifeGoals. Help users plan financial milestones with inflation-aware estimates.",
    "partner-finance": "You are PartnerFinance. Help couples optimize joint budget, goals, and debt strategy.",
}

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
    # NOTE: Avoid calling this same FastAPI service over HTTP from inside a request
    # handler, which can deadlock/time out under single-worker dev mode.
    prompt = AGENT_PROMPTS.get(agent_id, AGENT_PROMPTS["dhan-sarthi"])

    openai_api_key = (os.getenv("OPENAI_API_KEY", "") or "").strip().strip('"')
    openai_model = (os.getenv("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini").strip()

    if not openai_api_key:
        return (
            f"I'm {agent_id}, ready to help. I can still provide guidance without external AI keys. "
            f"For richer responses, set OPENAI_API_KEY in backend/.env and restart the backend."
        )

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": openai_model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ],
                "max_tokens": 700,
                "temperature": 0.7,
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return (
            f"I'm {agent_id}. I couldn't reach external AI right now ({str(e)}). "
            f"Please retry in a moment."
        )

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