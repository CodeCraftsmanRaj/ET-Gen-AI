"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Brain, BarChart3, Calculator, Target, TrendingUp, Shield, Scale, ArrowRight, Sparkles, Wallet, PiggyBank, Activity, Heart, CalendarClock, Zap, MoveRight } from "lucide-react"

const agents = [
  {
    id: "dhan-sarthi",
    name: "DhanSarthi",
    emoji: "🧠",
    title: "AI Coordinator",
    description: "Ask anything! I will route your query to the right specialist automatically.",
    color: "from-purple-500 to-indigo-600",
    href: "/agents/dhan-sarthi",
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
    title: "Life Events",
    description: "Plan your finances for major milestones like marriage, education, and purchasing a home using AI",
    color: "from-teal-500 to-emerald-600",
    href: "/agents/life-goals",
    icon: CalendarClock,
  },
  {
    id: "partner-finance",
    name: "PartnerFinance",
    emoji: "💑",
    title: "Joint Finances",
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
  const [user, setUser] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")

  const [dashboardData, setDashboardData] = useState({
    portfolioValue: 0,
    taxSaved: 0,
    fireProgress: 0,
    healthScore: 0
  })

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    
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

    fetch("/api/dhan-sarthi")
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
  const SkeletonCard = () => (
    <div className="h-24 bg-gradient-to-r from-slate-200/30 to-slate-100/30 dark:from-slate-800/30 dark:to-slate-700/30 rounded-2xl border border-slate-200/30 dark:border-slate-700/30 animate-pulse" />
  )

  return (
    <div className="space-y-8 pb-10">
      {/* Greeting Section */}
      <div className="animate-fade-in space-y-3">
        <h1 className="text-3xl md:text-5xl font-black tracking-tight">
          {getGreeting()}, <span className="bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">{user?.name?.split(" ")[0] || "Friend"}</span> 👋
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
            <Card key={stat.label} className={`bg-gradient-to-br ${stat.gradient} ${stat.borderColor} border transition-all duration-300 hover:shadow-lg hover:border-opacity-100 group`}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <CardDescription className="text-xs font-semibold uppercase tracking-wider mb-2 opacity-80">
                      {stat.label}
                    </CardDescription>
                    <p className={`text-2xl md:text-3xl font-black ${stat.textColor} tracking-tight leading-none`}>
                      {user ? (
                        <>
                          {stat.prefix === "₹" ? "₹" : ""}<AnimatedCounter value={stat.value} />
                          {stat.suffix ? <span className="text-lg ml-0.5">{stat.suffix}</span> : ""}
                        </>
                      ) : "—"}
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

      {/* Featured AI Agent - DhanSarthi */}
      {isLoading ? (
        <div className="h-48 bg-gradient-to-r from-slate-200/30 to-slate-100/30 dark:from-slate-800/30 dark:to-slate-700/30 rounded-3xl border border-slate-200/30 dark:border-slate-700/30 animate-pulse" />
      ) : (
        <Card className="overflow-hidden border-0 shadow-2xl bg-gradient-to-br from-slate-50 to-slate-100/50 dark:from-slate-900 dark:to-slate-800/50 hover:shadow-3xl transition-all duration-500 animate-fade-in group" style={{ animationDelay: "200ms" }}>
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-transparent to-indigo-500/10 pointer-events-none" />
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl group-hover:bg-purple-500/10 transition-all duration-500" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl group-hover:bg-indigo-500/10 transition-all duration-500" />

          <div className="relative p-8 md:p-10">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              {/* Icon */}
              <div className="p-5 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-3xl shadow-xl group-hover:shadow-2xl group-hover:scale-110 transition-all duration-300">
                <Brain className="w-8 h-8 text-white" />
              </div>

              {/* Content */}
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-3 mb-3">
                  <h2 className="text-3xl md:text-4xl font-black">DhanSarthi</h2>
                  <Badge className="bg-gradient-to-r from-purple-500 to-indigo-600 border-0 text-white shadow-lg text-xs px-3 py-1.5">
                    <Sparkles className="w-3.5 h-3.5 mr-1.5" />
                    AI Coordinator
                  </Badge>
                </div>
                
                <p className="text-base md:text-lg text-muted-foreground mb-6 leading-relaxed max-w-2xl">
                  Your intelligent financial guide. Ask anything about taxes, investments, retirement planning, stock analysis, or financial health — and I will route your query to the right specialist instantly.
                </p>

                <Link href="/agents/dhan-sarthi">
                  <Button size="lg" className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 font-bold text-base">
                    <Zap className="w-5 h-5 mr-2" />
                    Start Chatting with AI
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

      {/* Specialist Agents Section */}
      <div className="space-y-6 animate-fade-in" style={{ animationDelay: "300ms" }}>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Specialist Agents</h2>
            <p className="text-sm text-muted-foreground mt-2">Choose your financial expert for specialized guidance</p>
          </div>
          <Link href="/agents" className="text-primary hover:underline text-sm font-semibold flex items-center gap-2 group">
            View All Agents <MoveRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {isLoading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {[1, 2, 3, 4, 5, 6].map(i => <SkeletonCard key={i} />)}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {agents.filter(a => !a.featured).map((agent, i) => {
              const IconComponent = agent.icon
              return (
                <Link key={agent.id} href={agent.href}>
                  <Card className="h-full overflow-hidden border border-border/50 dark:border-border/30 hover:border-border/80 dark:hover:border-border/50 transition-all duration-300 hover:shadow-xl hover:scale-105 group cursor-pointer animate-slide-up bg-white dark:bg-slate-950/50 backdrop-blur-sm" style={{ animationDelay: `${i * 50}ms` }}>
                    {/* Top Accent Bar */}
                    <div className={`h-1.5 bg-gradient-to-r ${agent.color} group-hover:h-2 transition-all duration-300`} />

                    <CardHeader className="pb-4">
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div className={`p-3 rounded-xl bg-gradient-to-br ${agent.color} text-white shadow-lg transition-all duration-300 group-hover:scale-110 group-hover:rotate-3`}>
                          {IconComponent && <IconComponent className="w-6 h-6" />}
                        </div>
                        <Badge variant="outline" className="text-xs px-2 py-0.5 border-current/20 group-hover:border-current/40 transition-colors">
                          {agent.emoji}
                        </Badge>
                      </div>

                      <div>
                        <CardTitle className="text-lg md:text-xl font-bold">{agent.name}</CardTitle>
                        <CardDescription className="text-xs font-semibold uppercase tracking-wider mt-1 opacity-70">{agent.title}</CardDescription>
                      </div>
                    </CardHeader>

                    <CardContent className="space-y-4">
                      <p className="text-sm text-muted-foreground leading-relaxed">{agent.description}</p>
                      
                      {/* CTA */}
                      <div className="flex items-center justify-between text-sm font-semibold pt-2 border-t border-border/20 dark:border-border/10">
                        <span className="text-primary group-hover:translate-x-1 transition-transform inline-flex items-center gap-1.5">
                          Try Now <ArrowRight className="w-4 h-4" />
                        </span>
                        <span className="text-xs bg-gradient-to-r from-primary/20 to-primary/10 px-2 py-1 rounded text-primary font-semibold">
                          Instant
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              )
            })}
          </div>
        )}
      </div>

      {/* SEBI Disclaimer Section */}
      <div className="animate-fade-in border border-yellow-200/50 dark:border-yellow-900/30 rounded-2xl bg-gradient-to-br from-yellow-50/50 to-amber-50/30 dark:from-yellow-950/20 dark:to-amber-950/10 p-6 md:p-8 space-y-3" style={{ animationDelay: "400ms" }}>
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5">
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
