# AI Money Mentor 💰

**Your Personal Financial AI Team** — 9 specialist agents working together to provide expert financial guidance.

---

## 🎯 Overview

AI Money Mentor is a multi-agent financial intelligence platform that combines:
- **Next.js + TypeScript** frontend for a modern, responsive UI
- **Python FastAPI** backend with specialized financial agents
- **OpenAI GPT-4o-mini** for intelligent conversational responses
- **Coordinator Agent** that intelligently routes queries to 9 specialist agents

Whether you need tax advice, FIRE planning, portfolio analysis, or compliance guidance—the Coordinator instantly routes your question to the right expert.

---

## 🏗️ System Architecture

```mermaid
graph TB
    User["👤 User Interface<br/>Next.js Frontend<br/>localhost:3000"]
    
    Coordinator["🧠 Coordinator Agent<br/>Intelligent Router"]
    
    TaxMaster["🧾 TaxMaster<br/>Tax Calculations"]
    RetirementPro["🎯 RetirementPro<br/>FIRE Planning"]
    PortfolioWise["📊 PortfolioWise<br/>MF Analysis"]
    StockInsight["📈 StockInsight<br/>Stock Market"]
    MoneyHealth["💪 MoneyHealth<br/>Financial Health"]
    LifeGoals["🎉 LifeGoals<br/>Life Events"]
    PartnerFinance["💑 PartnerFinance<br/>Couple Finance"]
    ComplianceHelper["⚖️ ComplianceHelper<br/>Legal & Compliance"]
    Bazaar["📱 Bazaar<br/>Market Utils"]
    
    API["FastAPI Server<br/>localhost:8000"]
    DB[("🗄️ Database<br/>Chat History")]
    
    User -->|Ask Question| API
    API -->|Route Query| Coordinator
    
    Coordinator -->|Tax Question| TaxMaster
    Coordinator -->|FIRE Question| RetirementPro
    Coordinator -->|Portfolio Question| PortfolioWise
    Coordinator -->|Stock Question| StockInsight
    Coordinator -->|Health Question| MoneyHealth
    Coordinator -->|Life Event| LifeGoals
    Coordinator -->|Couple Finance| PartnerFinance
    Coordinator -->|Legal Question| ComplianceHelper
    Coordinator -->|Market Utils| Bazaar
    
    TaxMaster -->|Tax Data| API
    RetirementPro -->|FIRE Calculations| API
    PortfolioWise -->|Portfolio Metrics| API
    StockInsight -->|Stock Data| API
    MoneyHealth -->|Health Score| API
    LifeGoals -->|Event Plan| API
    PartnerFinance -->|Couple Plan| API
    ComplianceHelper -->|Legal Info| API
    Bazaar -->|Market Info| API
    
    API -->|Display Response| User
    API -->|Save Chat| DB
    
    style User fill:#e1f5ff
    style Coordinator fill:#fff3e0
    style TaxMaster fill:#f1f8e9
    style RetirementPro fill:#ffe0b2
    style PortfolioWise fill:#e3f2fd
    style StockInsight fill:#fce4ec
    style MoneyHealth fill:#f3e5f5
    style LifeGoals fill:#e0f2f1
    style PartnerFinance fill:#fce4ec
    style ComplianceHelper fill:#f5f5f5
    style Bazaar fill:#fff8e1
    style API fill:#fff9c4
    style DB fill:#c8e6c9
```

---

## 🔄 Query Flow Diagram

```mermaid
sequenceDiagram
    User->>Frontend: Ask Question
    Frontend->>API: POST /bridge/chat
    API->>Coordinator: Route Query
    
    alt Greeting/Help
        Coordinator->>Coordinator: Handle Directly
    else Finance Query
        Coordinator->>SpecialistAgent: Identify Intent
        SpecialistAgent->>Specialist: Calculate/Analyze
        Specialist->>API: Return Result
        API->>Coordinator: Get AI Response
        Coordinator->>OpenAI: Call GPT-4o
    end
    
    OpenAI->>Coordinator: AI Response
    Coordinator->>API: Format Response
    API->>Database: Save Chat
    API->>Frontend: Send Response
    Frontend->>User: Display Answer
```

---

## 🤖 The 9 Specialist Agents

### 1️⃣ **Coordinator** — The Intelligent Router
- **Purpose:** Intelligently routes queries to the right specialist agent
- **Capabilities:** Greetings, help, query parsing, intent detection
- **Example:** "What can you help me with?" → Explains all capabilities

### 2️⃣ **TaxMaster** — Tax Wizard
- **Purpose:** Indian income tax calculations & optimization
- **Capabilities:**
  - Old vs New regime comparison
  - Section-wise deductions (80C, 80D, 80CCD, HRA)
  - Capital gains tax (LTCG, STCG)
  - Tax saving strategies
- **Example:** "Calculate tax for ₹15 lakhs income" → Shows tax under both regimes

### 3️⃣ **RetirementPro** — FIRE Planner
- **Purpose:** Financial Independence & Retirement planning
- **Capabilities:**
  - FIRE number calculation (25x annual expenses)
  - SIP roadmaps
  - Retirement corpus planning
  - 4% withdrawal rule guidance
- **Example:** "My monthly expenses are 50K" → Shows FIRE number & monthly SIP needed

### 4️⃣ **PortfolioWise** — MF Portfolio Analyst
- **Purpose:** Mutual fund portfolio analysis & optimization
- **Capabilities:**
  - CAS parsing (CAMS, KFintech)
  - XIRR & CAGR calculations
  - Risk metrics (Sharpe ratio, Sortino ratio)
  - Overlap detection
  - Fund performance comparison
- **Example:** "Analyze my mutual fund portfolio" → Shows XIRR, risk, recommendations

### 5️⃣ **StockInsight** — Market Researcher
- **Purpose:** NSE/BSE stock analysis & market data
- **Capabilities:**
  - Real-time stock quotes
  - Top gainers/losers
  - Index data (Nifty, Sensex)
  - Company information
  - Technical analysis
- **Example:** "RELIANCE stock price?" → Shows current price, change, technical insights

### 6️⃣ **MoneyHealth** — Financial Health Expert
- **Purpose:** Comprehensive financial wellness scoring
- **Capabilities:**
  - 8-factor health assessment
  - Emergency fund readiness
  - Debt-to-income ratio
  - Savings rate analysis
  - Insurance coverage check
  - Investment diversification
- **Example:** "What's my financial health?" → Shows score & improvement areas

### 7️⃣ **LifeGoals** — Life Event Planner
- **Purpose:** Major life milestone financial planning
- **Capabilities:**
  - Marriage planning
  - Child/baby planning
  - Education planning
  - Home purchase planning
  - Bonus/inheritance planning
  - Cost projection & SIP calculation
- **Example:** "I'm getting married next year" → Shows budget & monthly SIP needed

### 8️⃣ **PartnerFinance** — Couple Financial Manager
- **Purpose:** Joint financial planning for partners
- **Capabilities:**
  - Shared budget planning
  - Expense splitting strategies
  - Joint debt payoff
  - Combined FIRE planning
  - HRA/NPS optimization for couples
  - Net-worth calculation
- **Example:** "Budget with my wife" → Shows optimal split & joint goals

### 9️⃣ **ComplianceHelper** — Legal & Compliance Advisor
- **Purpose:** Financial regulations & legal guidance
- **Capabilities:**
  - SEBI regulations
  - Income Tax Act sections
  - Constitution articles (Article 265, etc.)
  - RBI regulations
  - Consumer protection laws
  - Investor rights
- **Example:** "What are SEBI regulations?" → Shows relevant SEBI guidelines

### 🔟 **Bazaar** — Market Utilities
- **Purpose:** Advanced market screening & utilities
- **Capabilities:** Stock screening, custom market analysis, data exports

---

## 🏢 Project Structure

```
AI_Money_Mentor/
├── backend/
│   ├── agents/
│   │   ├── coordinator/          # Main routing agent
│   │   ├── tax-master/           # Tax calculations
│   │   ├── retirement-pro/       # FIRE planning
│   │   ├── portfolio-wise/       # MF analysis
│   │   ├── stock-insight/        # Stock data
│   │   ├── money-health/         # Financial health
│   │   ├── life-goals/           # Life events
│   │   ├── partner-finance/      # Couple finance
│   │   ├── compliance-helper/    # Legal guidance
│   │   └── bazaar/               # Market utilities
│   ├── bots/
│   │   └── telegram_bot.py       # Telegram integration
│   ├── api_server.py             # FastAPI main server
│   ├── chat_bridge.py            # Frontend-backend bridge
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Homepage with CardSwap
│   │   │   ├── agents/           # Agent pages (9 agents)
│   │   │   └── api/              # API routes (9 routes)
│   │   ├── components/
│   │   │   ├── CardSwap.tsx      # Rotating card animation
│   │   │   └── ui/               # Shadcn UI components
│   │   └── lib/
│   │       ├── api.ts            # API client
│   │       └── markdown.tsx      # Markdown parser
│   ├── prisma/
│   │   └── schema.prisma         # Database schema
│   ├── package.json              # JS dependencies
│   └── tsconfig.json             # TypeScript config
│
├── AGENTS.md                     # Detailed agent guide
├── ARCHITECTURE_DOCUMENT.md      # Technical architecture
├── CLAUDE.md                     # Development guidelines
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** + **Bun** (package manager)
- **Python 3.10+** + **UV** (package manager)
- **OpenAI API Key** (optional for AI responses)

---

### Backend Setup (FastAPI)

```bash
cd backend

# Initialize Python environment with UV
uv init
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv add -r requirements.txt

# Start FastAPI server
uv run uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

✅ API running at `http://localhost:8000`  
📚 API Docs at `http://localhost:8000/docs`

---

### Frontend Setup (Next.js + Bun)

```bash
cd frontend

# Install dependencies with Bun
bun install

# Generate Prisma client
bunx prisma generate

# Start dev server
bun run dev
```

✅ Frontend running at `http://localhost:3000`

---

## 🔑 Environment Variables

Create `.env` and `backend/.env`:

```env
# Backend API
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# OpenAI (optional, for AI responses)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini

# Telegram Bot (optional)
COORDINATOR_BOT_TOKEN=your-telegram-token

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/ai_mentor
```

---

## 🧪 Testing

```bash
cd backend

# Run all tests
uv run python test_all.py

# Run specific agent test
uv run python tests/test_karvid.py

# Run E2E tests
uv run python run_e2e_tests.py
```

---

## 📊 Data Flow Diagram

```mermaid
graph LR
    subgraph Frontend["Frontend (Next.js)"]
        HomePage["Home Page<br/>CardSwap Stack"]
        CoordinatorChat["Coordinator Chat UI"]
        AgentPages["9 Agent Pages"]
    end
    
    subgraph Backend["Backend (FastAPI)"]
        BridgeAPI["Bridge API<br/>/bridge/chat"]
        Coordinator["Coordinator<br/>Route Engine"]
        Agents["9 Specialist Agents"]
        AIResponder["AI Responder<br/>GPT-4o Integration"]
    end
    
    subgraph External["External Services"]
        OpenAI["OpenAI GPT-4o"]
        StockData["Stock Data API"]
        FundData["Mutual Fund Data"]
    end
    
    subgraph Storage["Storage"]
        PostgresDB["PostgreSQL<br/>Chat History"]
        LocalCache["Local Storage<br/>User Preferences"]
    end
    
    HomePage -->|Browse Agents| AgentPages
    HomePage -->|Click Ask| CoordinatorChat
    
    CoordinatorChat -->|POST Query| BridgeAPI
    AgentPages -->|Agent-specific| BridgeAPI
    
    BridgeAPI -->|Parse Query| Coordinator
    Coordinator -->|Route to| Agents
    
    Agents -->|Get AI Response| AIResponder
    AIResponder -->|Call API| OpenAI
    
    Agents -->|Fetch Data| StockData
    Agents -->|Fetch Data| FundData
    
    AIResponder -->|Format Response| BridgeAPI
    BridgeAPI -->|Save Chat| PostgresDB
    BridgeAPI -->|Return Response| CoordinatorChat
    
    CoordinatorChat -->|Save Preferences| LocalCache
    
    style Frontend fill:#e3f2fd
    style Backend fill:#fff3e0
    style External fill:#f3e5f5
    style Storage fill:#e8f5e9
```

---

## 🎨 Frontend Architecture

```mermaid
graph TD
    subgraph Pages["Pages"]
        Home["/ - Home<br/>CardSwap, Stats, CTA"]
        CoordinatorPage["/agents/coordinator<br/>Chat Interface"]
        AgentPages["/agents/[agent]<br/>9 Agent Chats"]
        Login["/login - Login"]
        Profile["/profile - Profile"]
    end
    
    subgraph Components["Components"]
        CardSwap["CardSwap.tsx<br/>Rotating Card Stack<br/>GSAP Animations"]
        UI["UI Components<br/>Shadcn + Custom"]
        Layout["ClientLayout.tsx<br/>Header & Footer"]
    end
    
    subgraph Services["Services"]
        APIClient["api.ts<br/>Axios Client"]
        Markdown["markdown.tsx<br/>MD Parser"]
        Store["store.ts<br/>State Management"]
    end
    
    Home -->|Display Agents| CardSwap
    Home -->|Show Stats| UI
    CoordinatorPage -->|Chat Interface| UI
    AgentPages -->|Agent UI| UI
    
    CoordinatorPage -->|Fetch Data| APIClient
    AgentPages -->|Fetch Data| APIClient
    
    APIClient -->|Parse Response| Markdown
    APIClient -->|Save State| Store
    
    Layout -->|Wrap All| Pages
    
    style Pages fill:#bbdefb
    style Components fill:#ffe0b2
    style Services fill:#c8e6c9
```

---

## 🔧 Backend Architecture

```mermaid
graph TD
    subgraph API["FastAPI Server"]
        MainServer["api_server.py<br/>Main Entry Point"]
        BridgeAPI["chat_bridge.py<br/>Frontend Bridge"]
        TelegramBot["telegram_bot.py<br/>Telegram Integration"]
    end
    
    subgraph Agents["Agent Modules"]
        CoordinatorAgent["Coordinator<br/>Route Engine"]
        TaxAgent["TaxMaster<br/>Tax Calculations"]
        RetirementAgent["RetirementPro<br/>FIRE Planning"]
        PortfolioAgent["PortfolioWise<br/>MF Analysis"]
        StockAgent["StockInsight<br/>Stock Data"]
        HealthAgent["MoneyHealth<br/>Health Scoring"]
        LifeAgent["LifeGoals<br/>Event Planning"]
        CoupleAgent["PartnerFinance<br/>Couple Finance"]
        ComplianceAgent["ComplianceHelper<br/>Legal Guidance"]
    end
    
    subgraph AILayer["AI/Responder Layer"]
        AIResponder["ai_responder.py<br/>AI Response Generation"]
        OpenAI["OpenAI GPT-4o-mini"]
    end
    
    subgraph DataLayer["Data & Utilities"]
        IndianData["indian_tax_laws.py<br/>Tax Database"]
        FundData["mf_data.py<br/>Mutual Fund Data"]
        CASParser["cas_parser.py<br/>CAS Statement Parser"]
        StockData["stock_data.py<br/>Stock Database"]
    end
    
    MainServer -->|Routes| BridgeAPI
    BridgeAPI -->|Parse Query| CoordinatorAgent
    
    CoordinatorAgent -->|Route Tax| TaxAgent
    CoordinatorAgent -->|Route Retirement| RetirementAgent
    CoordinatorAgent -->|Route Portfolio| PortfolioAgent
    CoordinatorAgent -->|Route Stock| StockAgent
    CoordinatorAgent -->|Route Health| HealthAgent
    CoordinatorAgent -->|Route Life| LifeAgent
    CoordinatorAgent -->|Route Couple| CoupleAgent
    CoordinatorAgent -->|Route Legal| ComplianceAgent
    
    TaxAgent -->|Use Data| IndianData
    PortfolioAgent -->|Use Data| CASParser
    PortfolioAgent -->|Use Data| FundData
    StockAgent -->|Use Data| StockData
    
    TaxAgent -->|Get AI| AIResponder
    RetirementAgent -->|Get AI| AIResponder
    AIResponder -->|Call API| OpenAI
    
    style API fill:#fff9c4
    style Agents fill:#ffe0b2
    style AILayer fill:#f3e5f5
    style DataLayer fill:#c8e6c9
```

---

## 🔐 Security & Compliance

✅ **SEBI Disclaimers** — All investment advice includes SEBI compliance notices  
✅ **Tax Accuracy** — Based on FY 2025-26 Indian tax laws  
✅ **Data Privacy** — Chat history stored securely (optional PostgreSQL)  
✅ **API Security** — CORS configured, environment variables protected  
✅ **Regulatory** — Follows Income Tax Act, SEBI guidelines, RBI regulations

---

## 📱 Chat Interface Features

- **Real-time Streaming** — Word-by-word response streaming
- **Markdown Support** — Formatted responses with bold, lists, tables
- **Agent Identification** — See which agent answered your question
- **Session History** — Save and load chat history
- **Quick Prompts** — One-click example queries
- **Status Indicator** — Backend online/offline status

---

## 🎯 Typical User Journey

```
1. User visits homepage (localhost:3000)
   ↓
2. Sees 9 agents in rotating CardSwap stack
   ↓
3. Clicks "Ask Coordinator" or specific agent
   ↓
4. Coordinator receives query
   ↓
5. Coordinator parses intent & routes to specialist
   ↓
6. Specialist calculates/analyzes
   ↓
7. AI Responder generates conversational response
   ↓
8. Chat saves to history
   ↓
9. User sees answer with formatting & data
```

---

## 📈 Future Enhancements

- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Mobile app (React Native)
- [ ] Real-time market data integration
- [ ] Advanced portfolio optimization
- [ ] PDF report generation
- [ ] Voice input/output
- [ ] Team collaboration features

---

## 📚 Documentation

- [AGENTS.md](AGENTS.md) — Detailed agent capabilities
- [ARCHITECTURE_DOCUMENT.md](ARCHITECTURE_DOCUMENT.md) — Technical deep dive
- [DEMO_SPEECH.md](DEMO_SPEECH.md) — 2-minute demo script

---

## 📞 Support

For issues or questions:
1. Check [AGENTS.md](AGENTS.md) for agent-specific details
2. Review [ARCHITECTURE_DOCUMENT.md](ARCHITECTURE_DOCUMENT.md) for technical info
3. See [CLAUDE.md](CLAUDE.md) for development help

---

## ⚖️ Legal Disclaimer

**SEBI Compliance Notice:** This platform provides educational financial guidance only and is NOT financial advice. Always consult a SEBI-registered investment advisor before making investment decisions. All investments carry market risk.

---

## 📄 License

MIT License — See LICENSE file for details

---

**Built with ❤️ for the ET AI Hackathon**

🚀 **Your Personal Financial AI Team — Always Available, Always Accurate**
