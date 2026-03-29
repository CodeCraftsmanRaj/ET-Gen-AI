# AI Money Mentor — Agent Guide

This project uses a multi-agent setup where each agent handles a specific finance domain.

## 1) DhanSarthi (Coordinator)
- Entry-point and router for user questions.
- Detects intent and sends the query to the right specialist agent.
- Handles greetings/help and conversation continuity.

## 2) KarVid (Tax Wizard)
- Income tax calculations for Indian users.
- Old vs New regime comparison.
- Deductions support (80C/80D/HRA/NPS) and capital gains handling.
- Tax section lookups and optimization suggestions.

## 3) YojanaKarta (FIRE Planner)
- FIRE target corpus calculations.
- SIP planning for retirement goals.
- Roadmaps and projections for long-term financial independence.

## 4) DhanRaksha (Money Health Score)
- Financial wellness scoring.
- Evaluates emergency readiness, debt health, savings/investment behavior, insurance, and retirement preparedness.
- Provides recommendations to improve weak areas.

## 5) Life Event Advisor
- Planning for major life milestones.
- Supports events like marriage, child/new baby, education, home purchase, retirement, bonus, inheritance.
- Projects future cost and required monthly investment.

## 6) Couple Planner
- Joint planning for two partners.
- Combined finances, expense split, budgeting, shared-goal SIPs, debt payoff strategy.
- Couple-level optimization for HRA/NPS split, insurance gap, and net-worth view.

## 7) Niveshak (MF Portfolio X-Ray)
- Mutual fund portfolio analysis.
- XIRR and risk metrics.
- CAS parsing support (CAMS/KFintech), overlap analysis, expense drag estimates, benchmark comparison, and rebalance suggestions.

## 8) BazaarGuru (Market Analyst)
- Stock market utilities.
- Quote lookup, top gainers, and index-related helpers.

## 9) Vidhi (Compliance & Legal)
- Financial compliance guidance.
- SEBI/regulatory disclaimers and legal-reference helpers.

---

## Typical flow
1. User asks a question.
2. DhanSarthi identifies intent.
3. Query is routed to one or more specialist agents.
4. Response is returned with domain-specific calculations/guidance.
