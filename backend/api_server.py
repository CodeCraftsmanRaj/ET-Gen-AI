"""
AI Money Mentor - FastAPI Server
Connects Telegram bots to Python modules
Cross-platform compatible with proper error handling
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project to path - cross-platform compatible
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Import all agent modules with fallbacks
try:
    from agents.portfolio_wise.portfolio_analyzer import PortfolioAnalyzer
except ImportError:
    logger.warning("PortfolioAnalyzer import failed, using stub")
    PortfolioAnalyzer = None

try:
    from agents.tax_master import calculate_new_regime_tax, calculate_old_regime_tax, compare_regimes, calculate_80c_deduction, calculate_equity_ltcg
except ImportError:
    logger.warning("TaxMaster imports failed, using stubs")
    def calculate_new_regime_tax(income): return {"tax": 0, "regime": "new"}
    def calculate_old_regime_tax(income): return {"tax": 0, "regime": "old"}
    def compare_regimes(income): return {"new": 0, "old": 0, "savings": 0}
    def calculate_80c_deduction(**kwargs): return {"deduction": 0}
    def calculate_equity_ltcg(gain): return {"tax": 0}

try:
    from agents.retirement_pro.fire_calculator import FIRECalculator, calculate_fire_number_india, get_sip_recommendation
except ImportError:
    logger.warning("RetirementPro imports failed, using stubs")
    FIRECalculator = None
    def calculate_fire_number_india(**kwargs): return {"fire_number": 0}
    def get_sip_recommendation(**kwargs): return {"sip_amount": 0}

try:
    from agents.stock_insight.stock_data import StockData
except ImportError:
    logger.warning("StockInsight imports failed, using stub")
    StockData = None

try:
    from agents.money_health.health_score import get_health_score
except ImportError:
    logger.warning("MoneyHealth imports failed, using stub")
    def get_health_score(**kwargs): return {"score": 0}

try:
    from agents.compliance_helper.compliance import get_disclaimers, SEBICompliance
except ImportError:
    logger.warning("ComplianceHelper imports failed, using stubs")
    def get_disclaimers(): return []
    SEBICompliance = None

app = FastAPI(
    title="AI Money Mentor API",
    description="Financial advisory API for Indian market",
    version="1.0.0"
)

# CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TaxRequest(BaseModel):
    income: float
    regime: str = "new"
    deductions_80c: float = 0
    deductions_80d: float = 0

class FIRERequest(BaseModel):
    monthly_expenses: float
    current_age: int = 30
    retirement_age: int = 55
    current_corpus: float = 0

class HealthRequest(BaseModel):
    income: float
    expenses: float
    monthly_savings: float = 0
    monthly_investments: float = 0
    debt: float = 0
    insurance_coverage: float = 0
    equity_allocation: float = 0
    debt_allocation: float = 0
    gold_allocation: float = 0
    cash_allocation: float = 0
    annual_tax_paid: float = 0
    annual_tax_saved: float = 0

class XIRRRequest(BaseModel):
    transactions: List[Dict[str, Any]]

class StockRequest(BaseModel):
    symbol: str

# Health check
@app.get("/")
async def root():
    return {
        "service": "AI Money Mentor API",
        "version": "1.0.0",
        "agents": [
            "portfolio-wise",      # MF Portfolio Analysis
            "tax-master",          # Income Tax & Deductions
            "retirement-pro",      # FIRE & Retirement Planning
            "stock-insight",       # Stock Market & Quotes
            "money-health",        # Financial Health Score
            "compliance-helper",   # SEBI & Compliance
            "dhan-sarthi",         # Coordinator
            "life-goals",          # Life Event Planning
            "partner-finance"      # Couple Finance Planning
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============ PORTFOLIO_WISE (MF Portfolio) ============
@app.post("/portfolio-wise/xirr")
async def calculate_xirr(request: XIRRRequest):
    """Calculate XIRR for portfolio"""
    analyzer = PortfolioAnalyzer()
    xirr = analyzer.calculate_xirr(request.transactions)
    return {"xirr_percent": round(xirr, 2)}

@app.post("/portfolio-wise/risk-metrics")
async def get_risk_metrics(request: Dict[str, Any]):
    """Get portfolio risk metrics"""
    analyzer = PortfolioAnalyzer()
    nav_data = request.get("nav_data", [])
    metrics = analyzer.get_risk_metrics(nav_data)
    return metrics

@app.post("/portfolio-wise/analyze")
async def analyze_portfolio(request: Dict[str, Any]):
    """Analyze entire portfolio from holdings list"""
    holdings = request.get("holdings", [])
    total_value = 0
    analyzer = PortfolioAnalyzer()
    
    # Calculate the total value based on units and NAV
    for h in holdings:
        total_value += h.get("units", 0) * h.get("nav", 0)
        
    # Generate true real cashflows derived from the SIP inputs
    from datetime import datetime
    today = datetime.now()
    transactions = []
    
    for h in holdings:
        sip = float(h.get("sipAmount", 0) or 0)
        duration = int(h.get("durationMonths", 0) or 0)
        
        if sip > 0 and duration > 0:
            for i in range(1, duration + 1):
                m = today.month - i
                year_offset = 0
                while m <= 0:
                    m += 12
                    year_offset -= 1
                y = today.year + year_offset
                d = min(today.day, 28)
                tx_date = f"{y:04d}-{m:02d}-{d:02d}"
                transactions.append({"date": tx_date, "amount": -sip})
                
    if not transactions and total_value > 0:
        # Fallback if no SIP entered, mock a generic 1 year lumpsum
        transactions.append({"date": f"{today.year-1}-{today.month:02d}-{today.day:02d}", "amount": -total_value/1.15})
        
    # Final positive cash flow evaluation mapping current portfolio net worth to today
    transactions.append({"date": today.strftime("%Y-%m-%d"), "amount": total_value})
    
    xirr_percent = 0
    if total_value > 0 and len(transactions) > 1:
        try:
            xirr_percent = analyzer.calculate_xirr(transactions)
        except Exception:
            xirr_percent = 0
    
    # Compute dynamic Sharpe Ratio mapped to the exact XIRR computed above
    # Assuming Risk Free Rate = 7.0%, Generic Equity Volatility = 15.0%
    sharpe_ratio = round((xirr_percent - 7.0) / 15.0, 2) if xirr_percent > 0 else 0
    
    risk_metrics = {
        "sharpe_ratio": sharpe_ratio,
        "volatility": 15.0,
        "max_drawdown": analyzer.get_risk_metrics([100, 102, 105, 104, 108, 110, 115])["max_drawdown"]
    }
    
    xray = _build_portfolio_xray(holdings, total_value, xirr_percent)

    return {
        "status": "success",
        "total_value": total_value,
        "xirr_percent": xirr_percent,
        "risk_metrics": risk_metrics,
        "holdings": holdings,
        "xray": xray
    }

# ============ TAX_MASTER (Tax Wizard) ============
@app.post("/tax-master/calculate-tax")
async def calculate_tax(request: TaxRequest):
    """Calculate tax under specified regime"""
    if request.regime == "new":
        result = calculate_new_regime_tax(request.income)
    else:
        result = calculate_old_regime_tax(request.income)
    
    result["regime"] = request.regime
    return result

@app.post("/tax-master/compare-regimes")
async def compare_tax_regimes(request: Dict[str, Any]):
    """Compare new vs old tax regime"""
    income = request.get("income", 0)
    result = compare_regimes(income)
    return result

@app.post("/tax-master/80c")
async def calculate_80c(request: Dict[str, Any]):
    """Calculate 80C deductions"""
    # Remap shorthand keys to actual function parameter names
    param_map = {
        "ppf": "ppf", "elss": "elss", "nps": "nps_tier1",
        "lic": "life_insurance_premium",
        "tuition_fees": "tuition_fees",
        "home_loan_principal": "home_loan_principal",
        "nsc": "nsc", "ssy": "ssy", "scss": "scss",
        "tax_saving_fd": "tax_saving_fd", "ulip": "ulip",
        "stamp_duty": "stamp_duty",
        "life_insurance_premium": "life_insurance_premium"
    }
    deductions = {}
    for k, v in request.items():
        if k in param_map:
            deductions[param_map[k]] = v
    result = calculate_80c_deduction(**deductions)
    return result

@app.post("/tax-master/capital-gains")
async def calculate_capital_gains(request: Dict[str, Any]):
    """Calculate capital gains tax"""
    holding_period = request.get("holding_period", "long")
    
    if holding_period == "long":
        # calculate_equity_ltcg needs sale_price, purchase_price, days_held
        sale_price = request.get("sale_price", 0)
        purchase_price = request.get("purchase_price", 0)
        days_held = request.get("days_held", 365)
        gain = request.get("gain", sale_price - purchase_price)
        
        if sale_price > 0 and purchase_price > 0:
            try:
                cg_result = calculate_equity_ltcg(sale_price, purchase_price, days_held)
                result = {
                    "gain": cg_result.gain,
                    "tax": cg_result.tax,
                    "holding_period": "long",
                    "exemption": getattr(cg_result, 'exemption', 125000),
                    "rate": "12.5%"
                }
            except Exception as e:
                # Fallback: simplified LTCG
                exempt = min(gain, 125000)
                taxable = max(0, gain - exempt)
                result = {
                    "gain": gain,
                    "tax": taxable * 0.125,
                    "holding_period": "long",
                    "exemption": exempt,
                    "rate": "12.5%",
                    "note": f"Simplified: {str(e)}"
                }
        else:
            # Only gain provided: simplified LTCG calc
            exempt = min(gain, 125000)
            taxable = max(0, gain - exempt)
            result = {
                "gain": gain,
                "tax": taxable * 0.125,
                "holding_period": "long",
                "exemption": exempt,
                "rate": "12.5%"
            }
    else:
        gain = request.get("gain", 0)
        result = {"gain": gain, "tax": gain * 0.15, "holding_period": "short", "rate": "15%"}
    
    return result

# ============ RETIREMENT_PRO (FIRE Planner) ============
@app.post("/retirement-pro/fire-number")
async def get_fire_number(request: Dict[str, Any]):
    """Calculate FIRE number"""
    monthly_expenses = request.get("monthly_expenses", 50000)
    result = calculate_fire_number_india(monthly_expenses)
    return result

@app.post("/retirement-pro/sip-recommendation")
async def get_sip(request: Dict[str, Any]):
    """Get SIP recommendation"""
    target_corpus = request.get("target_corpus", 10000000)
    years = request.get("years", 10)
    result = get_sip_recommendation(target_corpus, years)
    return result

@app.post("/retirement-pro/retirement-plan")
async def create_retirement_plan(request: Dict[str, Any]):
    """Create retirement plan"""
    monthly_expenses = float(request.get("monthly_expenses", 50000) or 50000)
    current_age = int(request.get("current_age", 30) or 30)
    retirement_age = int(request.get("retirement_age", 55) or 55)
    current_corpus = float(request.get("current_corpus", 0) or 0)
    monthly_income = float(request.get("monthly_income", 0) or 0)
    existing_life_cover = float(request.get("existing_life_cover", 0) or 0)
    tax_80c_used = float(request.get("tax_80c_used", 0) or 0)
    nps_contribution = float(request.get("nps_contribution", 0) or 0)
    goals = request.get("goals", []) or []

    calc = FIRECalculator(
        monthly_expenses=monthly_expenses,
        current_age=current_age,
        retirement_age=retirement_age,
        current_corpus=current_corpus
    )
    try:
        fire_number = calc.calculate_fire_number()
        monthly_savings = calc.calculate_monthly_savings()
        try:
            years = calc.calculate_years_to_fire(monthly_savings)
        except Exception:
            years = retirement_age - current_age

        annual_income = monthly_income * 12
        insurance_target = annual_income * 15 if annual_income > 0 else monthly_expenses * 12 * 10
        insurance_gap = max(0, insurance_target - existing_life_cover)

        goal_sip_allocation = calc.calculate_goal_based_sip(goals, max(1, years)) if goals else {"total_monthly_sip": 0, "goals": []}
        month_by_month_roadmap = _build_fire_monthly_roadmap(
            monthly_expenses=monthly_expenses,
            current_age=current_age,
            current_corpus=current_corpus,
            monthly_sip=monthly_savings,
            expected_return=calc.expected_return,
            months=max(12, min(600, years * 12)),
        )
        emergency_fund_target = round(monthly_expenses * 6, 2)
        tax_saving_moves = _build_tax_saving_moves(annual_income, tax_80c_used, nps_contribution)
        asset_allocation_glide_path = _build_asset_allocation_glide_path(max(1, years))

        plan = {
            "fire_number": fire_number,
            "years_to_fire": years,
            "monthly_savings": monthly_savings,
            "month_by_month_roadmap": month_by_month_roadmap,
            "goal_sip_allocation": goal_sip_allocation,
            "asset_allocation_glide_path": asset_allocation_glide_path,
            "insurance_gap": round(insurance_gap, 2),
            "tax_saving_moves": tax_saving_moves,
            "emergency_fund_target": emergency_fund_target,
        }
    except Exception as e:
        plan = {
            "fire_number": monthly_expenses * 12 * 25,
            "years_to_fire": retirement_age - current_age,
            "monthly_savings": 0,
            "note": f"Simplified calculation: {str(e)}"
        }
    return plan

# ============ BAZAAR GURU (Market Research) ============
@app.post("/stock-insight/stock-quote")
async def get_stock_quote(request: StockRequest):
    """Get stock quote from NSE"""
    nse = StockData()
    quote = nse.get_quote(request.symbol)
    if quote:
        return quote.to_dict()
    raise HTTPException(status_code=404, detail=f"Stock {request.symbol} not found")

@app.get("/stock-insight/top-gainers")
async def get_top_gainers(limit: int = 10):
    """Get top gaining stocks"""
    stock = StockData()
    gainers = stock.get_top_gainers(limit)
    return {"gainers": gainers}

@app.get("/stock-insight/nifty50")
async def get_nifty50():
    """Get NIFTY 50 stocks"""
    return {"stocks": StockData.NIFTY_50}

# ============ DHAN RAKSHA (Financial Health) ============
@app.post("/money-health/health-score")
async def calculate_health_score(request: HealthRequest):
    """Calculate financial health score"""
    payload = request.model_dump()
    result = get_health_score(
        monthly_income=request.income,
        monthly_expenses=request.expenses,
        monthly_emi=request.debt,
        life_insurance_cover=request.insurance_coverage,
        monthly_savings=request.monthly_savings,
        monthly_investments=request.monthly_investments
    )
    result["six_dimension_scorecard"] = _summarize_health_six_dimensions(result, payload)
    return result

# ============ COMPLIANCE_HELPER (Compliance) ============
@app.get("/compliance-helper/disclaimers")
async def get_all_disclaimers(category: str = "all"):
    """Get SEBI compliance disclaimers"""
    return {"disclaimers": get_disclaimers(category)}

@app.get("/compliance-helper/regulations")
async def get_sebi_regulations():
    """Get SEBI regulations"""
    return SEBICompliance.get_regulations()

# ============ DHAN SARTHI (Coordinator) ============
@app.post("/dhan-sarthi/route")
async def route_query(request: Dict[str, Any]):
    """Route query to appropriate agent with optional conversation context"""
    from agents.dhan_sarthi.coordinator import DhanSarthiCoordinator, AgentType
    coordinator = DhanSarthiCoordinator()
    query = request.get("query", "")
    context = request.get("context", [])  # Recent chat messages from frontend
    
    result = coordinator.parse_query(query)
    
    # Extract last agent from context for follow-up routing
    last_agent = None
    last_topic = None
    if context and isinstance(context, list):
        for msg in reversed(context):
            if msg.get("agent") and msg["agent"] != "dhan-sarthi":
                last_agent = msg["agent"]
                break
        # Get last user message for topic summary
        for msg in reversed(context):
            if msg.get("role") == "user":
                last_topic = msg.get("content", "")[:50]
                break
    
    # If DhanSarthi handles it directly (greeting/help/thanks/explain)
    if result.primary_agent == AgentType.DHAN_SARTHI:
        agent_list = [cap.name + " (" + cap.agent_type.value + ")" 
                      for cap in coordinator.AGENTS.values() 
                      if cap.agent_type != AgentType.DHAN_SARTHI]
        
        # Context-aware greeting responses
        context_suffix = ""
        if last_agent and last_topic:
            agent_names = {
                "tax-master": "tax calculations",
                "retirement-pro": "retirement planning", 
                "stock-insight": "stock market data",
                "money-health": "financial health",
                "portfolio-wise": "portfolio analysis",
                "compliance-helper": "compliance queries",
                "life-goals": "life event planning",
                "partner-finance": "couple finance planning"
            }
            topic_name = agent_names.get(last_agent, last_agent)
            context_suffix = f"\n\nLast time we discussed {topic_name}. Would you like to continue with that, or try something new?"
        
        responses = {
            "greeting": f"Namaste! I'm DhanSarthi, your AI Money Mentor. I coordinate a team of 8 specialist agents to help you with taxes, investments, retirement planning, and more. How can I help you today?{context_suffix}",
            "help": "I'm DhanSarthi, the brain of AI Money Mentor! Here's what my team can do:\n" + "\n".join(["- " + name for name in agent_list]) + "\nJust ask me anything financial and I'll route you to the right expert!",
            "thanks": "You're welcome! Happy to help with your financial journey. Feel free to ask me anything anytime. Dhanyavaad! 🙏",
            "explain": "I'm DhanSarthi, an AI-powered financial coordinator. I analyze your query and route it to the best specialist agent. Try asking about taxes, stocks, retirement, or financial health!",
        }
        
        return {
            "query": result.query,
            "primary_agent": result.primary_agent.value,
            "confidence": result.confidence,
            "intent": result.intent,
            "response": responses.get(result.intent, responses["greeting"]),
            "available_agents": agent_list,
            "suggestions": result.suggestions,
            "processing_time_ms": result.processing_time_ms,
            "context_used": bool(context),
            "last_agent": last_agent,
        }
    
    # For routed queries: if confidence is low and we have previous context, bias toward last agent
    if result.confidence < 0.4 and last_agent:
        agent_map = {
            "tax-master": AgentType.TAX_MASTER,
            "retirement-pro": AgentType.RETIREMENT_PRO,
            "stock-insight": AgentType.STOCK_INSIGHT,
            "money-health": AgentType.MONEY_HEALTH,
            "portfolio-wise": AgentType.PORTFOLIO_WISE,
            "compliance-helper": AgentType.COMPLIANCE_HELPER,
            "life-goals": AgentType.LIFE_GOALS,
            "partner-finance": AgentType.PARTNER_FINANCE,
        }
        if last_agent in agent_map:
            result.primary_agent = agent_map[last_agent]
            result.confidence = 0.5  # Boosted by context
    
    return result

# ============ KARVID TAX LAW ENDPOINTS ============
@app.get("/tax-master/section/{section}")
async def get_tax_section(section: str):
    """Get detailed information about a tax section"""
    from agents.tax_master.indian_tax_laws import get_tax_section_info
    return get_tax_section_info(section)

@app.get("/tax-master/capital-gains-info/{asset_type}")
async def get_capital_gains_info(asset_type: str):
    """Get capital gains tax information"""
    from agents.tax_master.indian_tax_laws import get_capital_gains_info
    return get_capital_gains_info(asset_type)

@app.get("/tax-master/tax-slabs/{regime}")
async def get_tax_slabs(regime: str):
    """Get tax slabs for a regime"""
    from agents.tax_master.indian_tax_laws import get_tax_slab
    return {"slabs": get_tax_slab(regime)}

# ============ VIDHI LEGAL ENDPOINTS ============
@app.get("/compliance-helper/constitution/{article}")
async def get_constitution_article(article: str):
    """Get Constitution provision"""
    from agents.compliance_helper.legal_knowledge import get_constitution_provision
    return get_constitution_provision(article)

@app.get("/compliance-helper/income-tax-section/{section}")
async def get_income_tax_section(section: str):
    """Get Income Tax Act section"""
    from agents.compliance_helper.legal_knowledge import get_income_tax_section
    return {"section": section, "description": get_income_tax_section(section)}

@app.get("/compliance-helper/sebi-regulation/{name}")
async def get_sebi_regulation(name: str):
    """Get SEBI regulation details"""
    from agents.compliance_helper.legal_knowledge import get_sebi_regulation
    return get_sebi_regulation(name)

@app.get("/compliance-helper/rbi-regulation/{name}")
async def get_rbi_regulation(name: str):
    """Get RBI regulation details"""
    from agents.compliance_helper.legal_knowledge import get_rbi_regulation
    return get_rbi_regulation(name)

# ============ LATENCY TRACKING ============
@app.get("/latency-stats")
async def get_latency_stats():
    """Get latency statistics"""
    from agents.dhan_sarthi.coordinator import DhanSarthiCoordinator
    coordinator = DhanSarthiCoordinator()
    return coordinator.get_latency_stats()

# ============================================================
# AI CHAT ENDPOINT
# ============================================================

@app.post("/ai/chat")
async def ai_chat_endpoint(request: dict):
    """
    AI-powered chat endpoint using OpenAI GPT-4o-mini
    Falls back to calculation-based responses if AI not configured
    """
    import os
    import requests
    import json
    
    message = request.get("message", "")
    agent = request.get("agent", "dhansarthi")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Agent prompts
    AGENT_PROMPTS = {
        "dhansarthi": "You are DhanSarthi, the intelligent coordinator of AI Money Mentor. Be conversational and helpful.",
        "karvid": "You are KarVid, the Tax Wizard for Indian taxes. Help users understand and calculate taxes.",
        "yojana": "You are YojanaKarta, the FIRE Planner. Help users plan financial independence and retirement.",
        "bazaar": "You are BazaarGuru, the Market Researcher. Provide stock prices and market analysis.",
        "dhan": "You are DhanRaksha, the Financial Health Expert. Assess financial health and provide recommendations.",
        "vidhi": "You are Vidhi, the Compliance Expert. Help users understand SEBI regulations and investor rights.",
    }
    
    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS["dhansarthi"])
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            response.raise_for_status()
            ai_response = response.json()["choices"][0]["message"]["content"]
            return {"agent": agent, "response": ai_response}
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback response
    return {
        "agent": agent,
        "response": f"I'm {agent.title()}, ready to help! AI responses require OPENAI_API_KEY to be configured. In the meantime, I can still help with calculations."
    }


# ============================================================
# CHAT BRIDGE ENDPOINTS - Frontend to OpenClaw Agent Swarm
# ============================================================

from chat_bridge import (
    ChatRequest, ChatResponse, 
    store_message, get_chat_history, send_to_agent,
    init_db
)
import uuid

# Initialize chat database
init_db()

@app.post("/bridge/chat", response_model=ChatResponse)
async def bridge_chat(request: ChatRequest):
    """
    Bridge frontend to OpenClaw agents with chat history
    
    - Stores user message in SQLite
    - Retrieves chat history for context
    - Sends to appropriate OpenClaw agent
    - Stores agent response
    - Returns response to frontend
    """
    # Generate session_id if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Store user message
    store_message(
        user_id=request.user_id,
        session_id=session_id,
        agent_id=request.agent_id,
        role="user",
        message=request.message
    )
    
    # Get chat history for context
    history = get_chat_history(
        user_id=request.user_id,
        session_id=session_id,
        limit=20
    )
    
    # Send to agent via WebSocket bridge
    try:
        response = send_to_agent(
            agent_id=request.agent_id,
            message=request.message,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Store agent response
    store_message(
        user_id=request.user_id,
        session_id=session_id,
        agent_id=request.agent_id,
        role="assistant",
        message=response
    )
    
    return ChatResponse(
        agent=request.agent_id,
        response=response,
        session_id=session_id,
        history_count=len(history)
    )

@app.get("/bridge/history/{user_id}/{session_id}")
async def bridge_get_history(user_id: str, session_id: str, limit: int = 50):
    """Get chat history for a user session"""
    history = get_chat_history(user_id, session_id, limit)
    return {"history": history, "count": len(history)}

@app.delete("/bridge/history/{user_id}/{session_id}")
async def bridge_clear_history(user_id: str, session_id: str):
    """Clear chat history for a session"""
    import sqlite3
    conn = sqlite3.connect(os.path.expanduser('~/ai-money-mentor/chat_history.db'))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_messages WHERE user_id = ? AND session_id = ?', (user_id, session_id))
    conn.commit()
    conn.close()
    return {"status": "cleared", "user_id": user_id, "session_id": session_id}

@app.get("/bridge/sessions/{user_id}")
async def bridge_list_sessions(user_id: str):
    """List all chat sessions for a user"""
    import sqlite3
    conn = sqlite3.connect(os.path.expanduser('~/ai-money-mentor/chat_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT session_id, agent_id, MAX(timestamp) as last_message
        FROM chat_messages WHERE user_id = ?
        GROUP BY session_id ORDER BY last_message DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    sessions = [{"session_id": r["session_id"], "agent_id": r["agent_id"], "last_message": r["last_message"]} for r in rows]
    return {"sessions": sessions}

# ============ LIFE EVENT ADVISOR ============
from agents.life_goals import (
    get_event_types,
    plan_life_event,
    comprehensive_plan as life_event_comprehensive_plan
)

@app.get("/life-goals/types")
async def life_event_get_types():
    """Get all available life event types"""
    return get_event_types()

@app.post("/life-goals/plan")
async def life_event_plan(request: Dict[str, Any]):
    """Plan for a specific life event"""
    return plan_life_event(
        event_type=request.get("event_type"),
        years_until=request.get("years_until", 5),
        current_corpus=request.get("current_corpus", 0),
        monthly_investment=request.get("monthly_investment", 0),
        inflation_rate=request.get("inflation_rate", 0.06),
        expected_return=request.get("expected_return", 0.12)
    )

@app.post("/life-goals/comprehensive")
async def life_event_comprehensive(request: Dict[str, Any]):
    """Create comprehensive life event financial plan"""
    try:
        result = life_event_comprehensive_plan(
            age=request.get("age", 25),
            income=request.get("income", 50000),
            current_corpus=request.get("current_corpus", 0),
            events=request.get("events", None)
        )
        return result
    except Exception as e:
        # Fallback: return a basic plan if comprehensive fails
        return {
            "status": "partial",
            "note": f"Comprehensive plan had an issue: {str(e)}",
            "age": request.get("age", 25),
            "events_planned": 0
        }

# ============ COUPLE PLANNER ============
from agents.partner_finance import (
    create_couple_plan,
    calculate_expense_split,
    optimize_couple_tax_and_protection,
    CouplePlanner,
    Person,
    SplitType
)


def _build_fire_monthly_roadmap(
    monthly_expenses: float,
    current_age: int,
    current_corpus: float,
    monthly_sip: float,
    expected_return: float,
    months: int,
) -> List[Dict[str, Any]]:
    """Generate month-by-month corpus projection."""
    roadmap: List[Dict[str, Any]] = []
    corpus = current_corpus
    monthly_rate = expected_return / 12

    for m in range(1, max(1, months) + 1):
        corpus = corpus * (1 + monthly_rate) + monthly_sip
        roadmap.append({
            "month": m,
            "age": round(current_age + (m / 12), 2),
            "projected_corpus": round(corpus, 2),
            "monthly_sip": round(monthly_sip, 2),
            "inflation_adjusted_monthly_expense": round(monthly_expenses * ((1 + 0.06) ** (m / 12)), 2),
        })

    return roadmap


def _build_asset_allocation_glide_path(years_to_fire: int) -> List[Dict[str, Any]]:
    """Simple glide path: reduce equity near FIRE date."""
    glide = []
    for y in range(0, max(1, years_to_fire) + 1):
        equity = max(40, min(80, 80 - (y * 2)))
        debt = 100 - equity
        glide.append({"year": y, "equity_percent": equity, "debt_percent": debt})
    return glide


def _build_tax_saving_moves(annual_income: float, tax_80c_used: float, nps_contribution: float) -> List[Dict[str, Any]]:
    """Create tax-saving actions ranked by immediate utility and liquidity."""
    remaining_80c = max(0, 150000 - tax_80c_used)
    remaining_nps = max(0, 50000 - nps_contribution)
    effective_rate = 0.30 if annual_income >= 1500000 else (0.20 if annual_income >= 800000 else 0.10)

    moves = [
        {
            "name": "Use remaining 80C room (ELSS/PPF/EPF)",
            "amount_room": round(remaining_80c, 2),
            "estimated_tax_benefit": round(remaining_80c * effective_rate, 2),
            "liquidity": "medium",
            "risk": "low_to_medium",
        },
        {
            "name": "Top up NPS under 80CCD(1B)",
            "amount_room": round(remaining_nps, 2),
            "estimated_tax_benefit": round(remaining_nps * effective_rate, 2),
            "liquidity": "low",
            "risk": "low",
        },
    ]
    return moves


def _summarize_health_six_dimensions(raw_result: Dict[str, Any], request_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Map health report into hackathon 6-dimension scorecard."""
    metrics = {m.get("category", ""): m for m in raw_result.get("metrics", [])}

    debt_metric = metrics.get("Debt to Income", {})
    emergency_metric = metrics.get("Emergency Fund", {})
    insurance_metric = metrics.get("Insurance Coverage", {})
    retirement_metric = metrics.get("Retirement Readiness", {})

    equity = float(request_data.get("equity_allocation", 0) or 0)
    debt = float(request_data.get("debt_allocation", 0) or 0)
    gold = float(request_data.get("gold_allocation", 0) or 0)
    cash = float(request_data.get("cash_allocation", 0) or 0)
    allocation_total = equity + debt + gold + cash
    diversification_score = 45.0
    if allocation_total > 0:
        weights = [equity / allocation_total, debt / allocation_total, gold / allocation_total, cash / allocation_total]
        concentration = max(weights)
        diversification_score = round(max(0, min(100, (1 - concentration) * 133.33)), 1)

    annual_income = float(request_data.get("income", 0) or 0) * 12
    annual_tax_paid = float(request_data.get("annual_tax_paid", 0) or 0)
    annual_tax_saved = float(request_data.get("annual_tax_saved", 0) or 0)
    tax_efficiency_score = 50.0
    if annual_income > 0:
        tax_ratio = annual_tax_paid / annual_income
        bonus = min(15, annual_tax_saved / max(1, annual_income) * 1000)
        tax_efficiency_score = round(max(0, min(100, 85 - (tax_ratio * 220) + bonus)), 1)

    return {
        "emergency_preparedness": {
            "score": emergency_metric.get("score", 0),
            "status": emergency_metric.get("status", "unknown"),
        },
        "insurance_coverage": {
            "score": insurance_metric.get("score", 0),
            "status": insurance_metric.get("status", "unknown"),
        },
        "investment_diversification": {
            "score": diversification_score,
            "status": "good" if diversification_score >= 60 else "needs_improvement",
        },
        "debt_health": {
            "score": debt_metric.get("score", 0),
            "status": debt_metric.get("status", "unknown"),
        },
        "tax_efficiency": {
            "score": tax_efficiency_score,
            "status": "good" if tax_efficiency_score >= 60 else "needs_improvement",
        },
        "retirement_readiness": {
            "score": retirement_metric.get("score", 0),
            "status": retirement_metric.get("status", "unknown"),
        },
    }


def _extract_category_from_name(name: str) -> str:
    lowered = (name or "").lower()
    if "small cap" in lowered or "smallcap" in lowered:
        return "Small Cap"
    if "mid cap" in lowered or "midcap" in lowered:
        return "Mid Cap"
    if "large cap" in lowered or "largecap" in lowered or "bluechip" in lowered:
        return "Large Cap"
    if "index" in lowered or "nifty" in lowered or "sensex" in lowered:
        return "Index"
    if "debt" in lowered or "bond" in lowered or "gilt" in lowered or "liquid" in lowered:
        return "Debt"
    if "flexi" in lowered or "multicap" in lowered:
        return "Flexi/Multi Cap"
    return "Other"


def _build_portfolio_xray(holdings: List[Dict[str, Any]], total_value: float, xirr_percent: float) -> Dict[str, Any]:
    """Build overlap, expense drag, benchmark comparison and rebalance ideas."""
    if total_value <= 0:
        return {
            "overlap_analysis": {},
            "expense_ratio_drag": {},
            "benchmark_comparison": {},
            "rebalancing_plan": [],
        }

    category_weights: Dict[str, float] = {}
    weighted_expense_ratio = 0.0

    for h in holdings:
        name = h.get("name", "")
        value = float(h.get("units", 0) or 0) * float(h.get("nav", 0) or 0)
        if value <= 0:
            continue
        weight = value / total_value
        category = _extract_category_from_name(name)
        category_weights[category] = category_weights.get(category, 0) + weight

        expense_ratio = float(h.get("expenseRatio", 1.0) or 1.0)
        weighted_expense_ratio += (expense_ratio * weight)

    overlap_score = round(min(100, max(category_weights.values(), default=0) * 100), 1)
    annual_drag_rupees = round(total_value * (weighted_expense_ratio / 100), 2)

    benchmark = 12.0
    alpha = round(xirr_percent - benchmark, 2)

    rebalancing_plan = []
    for cat, wt in category_weights.items():
        if wt > 0.45:
            rebalancing_plan.append(
                f"Reduce {cat} exposure from {round(wt * 100, 1)}% toward 35-40% to lower concentration risk."
            )
    if not rebalancing_plan:
        rebalancing_plan.append("Current allocation appears reasonably diversified across categories.")

    return {
        "overlap_analysis": {
            "category_weights_percent": {k: round(v * 100, 1) for k, v in category_weights.items()},
            "overlap_risk_score": overlap_score,
        },
        "expense_ratio_drag": {
            "weighted_expense_ratio_percent": round(weighted_expense_ratio, 2),
            "estimated_annual_drag_rupees": annual_drag_rupees,
        },
        "benchmark_comparison": {
            "portfolio_xirr_percent": round(xirr_percent, 2),
            "benchmark_name": "Nifty 50 TRI (proxy)",
            "benchmark_return_percent": benchmark,
            "alpha_percent": alpha,
        },
        "rebalancing_plan": rebalancing_plan,
    }

@app.post("/partner-finance/finances")
async def couple_get_finances(request: Dict[str, Any]):
    """Get combined finances for a couple"""
    p1 = Person(name=request.get("person1_name", "Person 1"), income=request.get("person1_income", 0))
    p2 = Person(name=request.get("person2_name", "Person 2"), income=request.get("person2_income", 0))
    planner = CouplePlanner(p1, p2)
    return planner.get_combined_finances()

@app.post("/partner-finance/split-expense")
async def couple_split_expense(request: Dict[str, Any]):
    """Calculate how to split an expense between couple"""
    return calculate_expense_split(
        person1_name=request.get("person1_name", "Person 1"),
        person1_income=request.get("person1_income", 0),
        person2_name=request.get("person2_name", "Person 2"),
        person2_income=request.get("person2_income", 0),
        expense_amount=request.get("expense_amount", 0),
        split_type=request.get("split_type", "proportional")
    )

@app.post("/partner-finance/plan")
async def couple_create_plan(request: Dict[str, Any]):
    """Create comprehensive couple financial plan"""
    return create_couple_plan(
        person1_name=request.get("person1_name", "Person 1"),
        person1_income=request.get("person1_income", 0),
        person2_name=request.get("person2_name", "Person 2"),
        person2_income=request.get("person2_income", 0),
        goals=request.get("goals")
    )

@app.post("/partner-finance/budget")
async def couple_create_budget(request: Dict[str, Any]):
    """Create joint budget plan"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0),
        expenses=request.get("person1_expenses", 0),
        savings=request.get("person1_savings", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0),
        expenses=request.get("person2_expenses", 0),
        savings=request.get("person2_savings", 0)
    )
    planner = CouplePlanner(p1, p2)
    return planner.create_budget_plan(request.get("categories"))

@app.post("/partner-finance/goals")
async def couple_plan_goals(request: Dict[str, Any]):
    """Calculate SIP for couple's shared goals"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0)
    )
    planner = CouplePlanner(p1, p2)
    
    # Add goals
    for goal in request.get("goals", []):
        planner.add_shared_goal(
            name=goal["name"],
            target_amount=goal["target_amount"],
            deadline_years=goal["years"],
            priority=goal.get("priority", 3)
        )
    
    return planner.calculate_sip_for_goals(request.get("expected_return", 0.12))

@app.post("/partner-finance/debt-payoff")
async def couple_debt_payoff(request: Dict[str, Any]):
    """Plan debt payoff strategy for couple"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0),
        expenses=request.get("person1_expenses", 0),
        savings=request.get("person1_savings", 0),
        debt=request.get("person1_debt", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0),
        expenses=request.get("person2_expenses", 0),
        savings=request.get("person2_savings", 0),
        debt=request.get("person2_debt", 0)
    )
    planner = CouplePlanner(p1, p2)
    try:
        return planner.plan_debt_payoff(
            debts=request.get("debts", []),
            strategy=request.get("strategy", "avalanche")
        )
    except Exception as e:
        return {
            "strategy": request.get("strategy", "avalanche"),
            "debts": request.get("debts", []),
            "note": f"Debt payoff calculation error: {str(e)}",
            "recommendation": "Please provide expenses and savings for both partners for accurate planning."
        }


@app.post("/partner-finance/optimize")
async def couple_optimize(request: Dict[str, Any]):
    """Optimize couple plan across HRA, NPS, SIP split, insurance, and net worth."""
    return optimize_couple_tax_and_protection(
        person1_name=request.get("person1_name", "Person 1"),
        person1_income=request.get("person1_income", 0),
        person2_name=request.get("person2_name", "Person 2"),
        person2_income=request.get("person2_income", 0),
        person1_expenses=request.get("person1_expenses", 0),
        person2_expenses=request.get("person2_expenses", 0),
        person1_savings=request.get("person1_savings", 0),
        person2_savings=request.get("person2_savings", 0),
        rent_paid_annual=request.get("rent_paid_annual", 0),
        hra_received_person1=request.get("hra_received_person1", 0),
        hra_received_person2=request.get("hra_received_person2", 0),
        nps_person1=request.get("nps_person1", 0),
        nps_person2=request.get("nps_person2", 0),
        current_life_cover_person1=request.get("current_life_cover_person1", 0),
        current_life_cover_person2=request.get("current_life_cover_person2", 0),
        goals=request.get("goals", []),
        expected_return=request.get("expected_return", 0.12),
    )

# ============ MAIN ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
