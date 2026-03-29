"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import CardSwap, { Card as SwapCard } from "@/components/CardSwap"
import { Brain, BarChart3, Calculator, Target, TrendingUp, Shield, Scale, ArrowRight, Wallet, PiggyBank, Activity, Heart, CalendarClock, Zap, MoveRight } from "lucide-react"

const agents = [
  {
    id: "coordinator",
    name: "Coordinator",
    emoji: "🧠",
    title: "Primary Coordinator",
    description: "Ask anything! I will route your query to the right specialist automatically.",
    color: "from-purple-500 to-indigo-600",
    href: "/agents/coordinator",
    featured: true,
  },
  {
    id: "portfolio-wise",
    name: "PortfolioWise",
    emoji: "📊",
    title: "MF Portfolio X-Ray",
    description: "Analyze mutual fund portfolios, calculate XIRR, Sharpe ratio, and get AI-powered insights",
    color: "from-blue-500 to-cyan-600",
    href: "/agents/portfolio-wise",
    icon: BarChart3,
  },
  {
    id: "tax-master",
    name: "TaxMaster",
    emoji: "🧾",
    title: "Tax Calculator",
    description: "Calculate taxes under old & new regimes, compare deductions, optimize tax savings",
    color: "from-green-500 to-emerald-600",
    href: "/agents/tax-master",
    icon: Calculator,
  },
  {
    id: "retirement-pro",
    name: "RetirementPro",
    emoji: "🎯",
    title: "FIRE Planner",
    description: "Plan your Financial Independence, calculate FIRE number, track retirement goals",
    color: "from-orange-500 to-amber-600",
    href: "/agents/retirement-pro",
    icon: Target,
  },
  {
    id: "stock-insight",
    name: "StockInsight",
    emoji: "📈",
    title: "Stock Quotes",
    description: "Real-time stock quotes, market analysis, and investment recommendations",
    color: "from-pink-500 to-rose-600",
    href: "/agents/stock-insight",
    icon: TrendingUp,
  },
  {
    id: "money-health",
    name: "MoneyHealth",
    emoji: "💪",
    title: "Financial Health",
    description: "Assess your financial health score, emergency fund status, savings rate analysis",
    color: "from-red-500 to-orange-600",
    href: "/agents/money-health",
    icon: Shield,
  },
  {
    id: "compliance-helper",
    name: "ComplianceHelper",
    emoji: "⚖️",
    title: "Compliance",
    description: "SEBI disclaimers, regulatory information, and compliance guidelines",
    color: "from-slate-500 to-zinc-600",
    href: "/agents/compliance-helper",
    icon: Scale,
  },
  {
    id: "life-goals",
    name: "LifeGoals",
    emoji: "🎉",
    title: "LifeGoals",
    description: "Plan your finances for major milestones like marriage, education, and purchasing a home using AI",
    color: "from-teal-500 to-emerald-600",
    href: "/agents/life-goals",
    icon: CalendarClock,
  },
  {
    id: "partner-finance",
    name: "PartnerFinance",
    emoji: "💑",
    title: "PartnerFinance",
    description: "Plan your finances together, manage joint budgets, and achieve shared financial goals",
    color: "from-rose-400 to-pink-500",
    href: "/agents/partner-finance",
    icon: Heart,
  },
]

function AnimatedCounter({ value, prefix = "", suffix = "" }: { value: number; prefix?: string; suffix?: string }) {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    if (value <= 0) return
    const duration = 1200
    const steps = 40
    const stepValue = value / steps
    let current = 0
    const timer = setInterval(() => {
      current += stepValue
      if (current >= value) {
        setCount(value)
        clearInterval(timer)
      } else {
        setCount(Math.floor(current))
      }
    }, duration / steps)
    return () => clearInterval(timer)
  }, [value])

  if (value <= 0) return <span>—</span>

  const formatted = new Intl.NumberFormat("en-IN", {
    style: prefix === "₹" ? "currency" : "decimal",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(count)

  return <span>{prefix === "₹" ? formatted : `${formatted}${suffix}`}</span>
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(true)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")

  const [dashboardData, setDashboardData] = useState({
    portfolioValue: 0,
    taxSaved: 0,
    fireProgress: 0,
    healthScore: 0
  })

  useEffect(() => {
    const loadDashboardData = () => {
      setDashboardData({
        portfolioValue: parseFloat(localStorage.getItem('dashboard_portfolio') || '0'),
        taxSaved: parseFloat(localStorage.getItem('dashboard_tax_saved') || '0'),
        fireProgress: parseFloat(localStorage.getItem('dashboard_fire') || '0'),
        healthScore: parseFloat(localStorage.getItem('dashboard_health') || '0')
      })
    }
    
    loadDashboardData()
    window.addEventListener("storage", loadDashboardData)
    
    setIsLoading(false)

    fetch("/api/coordinator")
      .then((res) => {
        if (res.ok) setBackendStatus("online")
        else setBackendStatus("offline")
      })
      .catch(() => setBackendStatus("offline"))
      
    return () => window.removeEventListener("storage", loadDashboardData)
  }, [])

  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return "Good Morning"
    if (hour < 17) return "Good Afternoon"
    return "Good Evening"
  }

  // Skeleton Loader Component
  const SkeletonCard = () => <div className="h-24 bg-muted/50 rounded-2xl border border-border/60 animate-pulse" />

  return (
    <div className="space-y-8 pb-10">
      {/* Greeting Section */}
      <div className="animate-fade-in space-y-3">
        <h1 className="text-3xl md:text-5xl font-black tracking-tight">
          {getGreeting()}, <span className="text-foreground">Welcome</span> 👋
        </h1>
        <p className="text-muted-foreground text-lg max-w-2xl">
          Manage your finances smartly with AI-powered insights.
          <span className={`ml-2 inline-block w-2 h-2 rounded-full ${backendStatus === "online" ? "bg-green-500 animate-pulse" : "bg-red-500"}`} />
        </p>
      </div>

      {/* Quick Stats - Financial Overview */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 animate-fade-in" style={{ animationDelay: "100ms" }}>
        {isLoading ? (
          <>
            <SkeletonCard /> <SkeletonCard /> <SkeletonCard /> <SkeletonCard />
          </>
        ) : (
          [
            { icon: Wallet, label: "Portfolio Value", value: dashboardData.portfolioValue, prefix: "₹", gradient: "from-blue-500/15 to-blue-600/5 dark:from-blue-500/20 dark:to-blue-600/10", iconBg: "bg-blue-500/20 dark:bg-blue-500/30", iconColor: "text-blue-600 dark:text-blue-400", textColor: "text-blue-700 dark:text-blue-300", borderColor: "border-blue-200/50 dark:border-blue-800/30" },
            { icon: PiggyBank, label: "Tax Saved YTD", value: dashboardData.taxSaved, prefix: "₹", gradient: "from-emerald-500/15 to-emerald-600/5 dark:from-emerald-500/20 dark:to-emerald-600/10", iconBg: "bg-emerald-500/20 dark:bg-emerald-500/30", iconColor: "text-emerald-600 dark:text-emerald-400", textColor: "text-emerald-700 dark:text-emerald-300", borderColor: "border-emerald-200/50 dark:border-emerald-800/30" },
            { icon: Target, label: "FIRE Progress", value: dashboardData.fireProgress, suffix: "%", gradient: "from-orange-500/15 to-amber-600/5 dark:from-orange-500/20 dark:to-amber-600/10", iconBg: "bg-orange-500/20 dark:bg-orange-500/30", iconColor: "text-orange-600 dark:text-orange-400", textColor: "text-orange-700 dark:text-orange-300", borderColor: "border-orange-200/50 dark:border-orange-800/30" },
            { icon: Activity, label: "Health Score", value: dashboardData.healthScore, suffix: "/100", gradient: "from-red-500/15 to-rose-600/5 dark:from-red-500/20 dark:to-rose-600/10", iconBg: "bg-red-500/20 dark:bg-red-500/30", iconColor: "text-red-600 dark:text-red-400", textColor: "text-red-700 dark:text-red-300", borderColor: "border-red-200/50 dark:border-red-800/30" },
          ].map((stat, i) => (
            <Card key={stat.label} className={`${stat.borderColor} bg-card border transition-all duration-300 hover:shadow-md group`}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <CardDescription className="text-xs font-semibold uppercase tracking-wider mb-2 opacity-80">
                      {stat.label}
                    </CardDescription>
                    <p className={`text-2xl md:text-3xl font-black ${stat.textColor} tracking-tight leading-none`}>
                      <>
                        {stat.prefix === "₹" ? "₹" : ""}<AnimatedCounter value={stat.value} />
                        {stat.suffix ? <span className="text-lg ml-0.5">{stat.suffix}</span> : ""}
                      </>
                    </p>
                  </div>
                  <div className={`p-2.5 rounded-lg ${stat.iconBg} ${stat.iconColor} group-hover:scale-110 transition-transform duration-300`}>
                    <stat.icon className="w-5 h-5" />
                  </div>
                </div>
              </CardHeader>
            </Card>
          ))
        )}
      </div>

      {/* Featured AI Agent - Coordinator */}
      {isLoading ? (
        <div className="h-48 bg-muted/50 rounded-3xl border border-border/60 animate-pulse" />
      ) : (
        <Card className="overflow-hidden border border-border/70 shadow-sm hover:shadow-md transition-all duration-300 animate-fade-in" style={{ animationDelay: "200ms" }}>
          <div className="relative p-8 md:p-10">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              {/* Icon */}
              <div className="p-4 bg-muted rounded-2xl border border-border/70">
                <Brain className="w-7 h-7 text-foreground" />
              </div>

              {/* Content */}
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-3 mb-3">
                  <h2 className="text-3xl md:text-4xl font-black">Coordinator</h2>
                  <Badge variant="secondary" className="text-xs px-3 py-1.5">AI Coordinator</Badge>
                </div>
                
                <p className="text-base md:text-lg text-muted-foreground mb-6 leading-relaxed max-w-2xl">
                  Your intelligent financial guide. Ask anything about taxes, investments, retirement planning, stock analysis, or financial health — and I will route your query to the right specialist instantly.
                </p>

                <Link href="/agents/coordinator">
                  <Button size="lg" className="font-semibold text-base">
                    <Zap className="w-5 h-5 mr-2" />
                    Ask Coordinator
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </Button>
                </Link>
              </div>

              {/* Stats Badges */}
              <div className="flex flex-col gap-3 md:ml-auto">
                <div className="text-center px-4 py-2 rounded-xl bg-white/50 dark:bg-slate-800/50 border border-slate-200/50 dark:border-slate-700/50">
                  <p className="text-xs text-muted-foreground">Active Agents</p>
                  <p className="text-2xl font-black">9</p>
                </div>
                <div className="text-center px-4 py-2 rounded-xl bg-white/50 dark:bg-slate-800/50 border border-slate-200/50 dark:border-slate-700/50">
                  <p className="text-xs text-muted-foreground">24/7</p>
                  <p className="text-2xl font-black">Available</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* All Agents Section */}
      <div className="space-y-6 animate-fade-in" style={{ animationDelay: "300ms" }}>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold tracking-tight">All AI Agents</h2>
            <p className="text-sm text-muted-foreground mt-2">Browse all 9 agents in a rotating card stack</p>
          </div>
          <Link href="/agents/coordinator" className="text-primary hover:underline text-sm font-semibold flex items-center gap-2 group">
            Open Coordinator <MoveRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        <div className="flex justify-center pt-44 md:pt-48" style={{ height: "700px", position: "relative" }}>
          <CardSwap cardDistance={40} verticalDistance={55} delay={2200} pauseOnHover width="min(700px, 92vw)" height={280} easing="linear">
            {agents.map((agent) => {
              const IconComponent = agent.icon
              return (
                <SwapCard key={agent.id} className="bg-white dark:bg-slate-900 border border-border/60">
                  <Link href={agent.href} className="block h-full">
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        {IconComponent ? <IconComponent className="w-5 h-5 text-primary" /> : <Brain className="w-5 h-5 text-primary" />}
                        <h3 className="text-lg font-bold leading-tight">{agent.name}</h3>
                      </div>
                      <Badge variant="outline">{agent.emoji}</Badge>
                    </div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">{agent.title}</p>
                    <p className="text-sm text-muted-foreground leading-relaxed">{agent.description}</p>
                    <div className="pt-3 mt-3 border-t border-border/50 text-sm font-semibold text-primary inline-flex items-center gap-1">
                      Open <ArrowRight className="w-4 h-4" />
                    </div>
                  </Link>
                </SwapCard>
              )
            })}
          </CardSwap>
        </div>
      </div>

      {/* SEBI Disclaimer Section */}
      <div className="animate-fade-in border border-yellow-200/50 dark:border-yellow-900/30 rounded-2xl bg-card p-6 md:p-8 space-y-3" style={{ animationDelay: "400ms" }}>
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 shrink-0 mt-0.5">
            <Shield className="w-5 h-5" />
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-yellow-900 dark:text-yellow-300 mb-2">SEBI Compliance Notice</h3>
            <p className="text-sm text-yellow-800 dark:text-yellow-200/80 leading-relaxed">
              All investments carry market risk. This platform provides educational guidance only and is not 
              financial advice. Always consult a SEBI-registered investment advisor before making investment decisions. 
              Read all terms and conditions carefully.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
