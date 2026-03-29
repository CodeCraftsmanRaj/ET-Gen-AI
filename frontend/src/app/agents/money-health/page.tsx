"use client"

import { useState, useRef, useEffect, useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Loader2, Send, TrendingUp, AlertCircle } from "lucide-react"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function MoneyHealthPage() {
  const [formData, setFormData, hasLoaded] = useLocalStorage("dhan_form", {
    monthlyIncome: 100000,
    monthlyExpenses: 60000,
    emergencyFund: 200000,
    totalDebt: 500000,
    investments: 2000000,
    age: 30,
  })
  
  const [calculating, setCalculating] = useState(false)
  const [result, setResult] = useState<any>(null)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am MoneyHealth, your Health Diagnostics AI Agent. Fill out the form to generate a unified financial health score, or ask me directly to formulate an emergency fund strategy."
  }])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || 0 }))
  }

  const handleSendMessage = async (customQuery?: string) => {
    const query = customQuery || chatInput.trim()
    if (!query || chatLoading) return

    if (!customQuery) setChatInput("")
    setMessages(prev => [...prev, { id: Date.now().toString(), role: "user", content: query }])
    setChatLoading(true)

    try {
      const userStr = localStorage.getItem('user')
      const userId = userStr ? JSON.parse(userStr).id : "anonymous"

      const response = await fetch("/api/bridge/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          user_id: userId,
          agent_id: "dhan"
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setMessages(prev => [...prev, {
          id: String(Date.now() + 1),
          role: "assistant",
          content: data.response || "I encountered an error analyzing that."
        }])
      } else {
        setMessages(prev => [...prev, {
          id: String(Date.now() + 1),
          role: "assistant",
          content: "Sorry, the DhanRaksha agent is offline."
        }])
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        id: String(Date.now() + 1),
        role: "assistant",
        content: "Error connecting to the AI agent."
      }])
    } finally {
      setChatLoading(false)
    }
  }

  const calculateHealthScore = async () => {
    setCalculating(true)
    try {
      const { monthlyIncome, monthlyExpenses, emergencyFund, totalDebt, investments, age } = formData
      
      const safeIncome = Math.max(1, monthlyIncome)
      const safeExpenses = Math.max(1, monthlyExpenses)
      
      const savingsRate = ((monthlyIncome - monthlyExpenses) / safeIncome) * 100
      const emergencyMonths = emergencyFund / safeExpenses
      const debtToIncome = (totalDebt / (safeIncome * 12)) * 100
      
      let score = 0
      
      if (savingsRate >= 30) score += 20
      else if (savingsRate >= 20) score += 15
      else if (savingsRate >= 10) score += 10
      else if (savingsRate >= 5) score += 5
      
      if (emergencyMonths >= 6) score += 20
      else if (emergencyMonths >= 4) score += 15
      else if (emergencyMonths >= 2) score += 10
      else if (emergencyMonths >= 1) score += 5
      
      if (debtToIncome <= 20) score += 20
      else if (debtToIncome <= 40) score += 15
      else if (debtToIncome <= 60) score += 10
      else if (debtToIncome <= 80) score += 5
      
      const investmentRatio = investments / (safeIncome * 12)
      if (investmentRatio >= 3) score += 20
      else if (investmentRatio >= 2) score += 15
      else if (investmentRatio >= 1) score += 10
      else if (investmentRatio >= 0.5) score += 5
      
      const actualMultiple = investments / (safeIncome * 12)
      if (actualMultiple >= age * 0.1) score += 20
      else if (actualMultiple >= age * 0.05) score += 15
      else if (actualMultiple >= age * 0.03) score += 10
      else if (actualMultiple >= age * 0.01) score += 5
      
      const recommendations = []
      if (savingsRate < 20) recommendations.push("Increase your savings rate to at least 20% of income")
      if (emergencyMonths < 6) recommendations.push("Build emergency fund to cover 6 months of expenses")
      if (debtToIncome > 40) recommendations.push("Focus on reducing debt before increasing investments")
      if (investmentRatio < 1) recommendations.push("Aim to have at least 1x annual income in investments")

      const finalScore = Math.min(100, score)
      
      setResult({
        overallScore: finalScore,
        savingsRate,
        emergencyMonths,
        debtToIncome,
        investmentRatio,
        recommendations,
        breakdown: {
          savings: Math.min(20, Math.floor(savingsRate / 1.5)),
          emergency: Math.min(20, Math.floor(emergencyMonths * 3.33)),
          debt: debtToIncome <= 20 ? 20 : Math.max(0, 20 - Math.floor((debtToIncome - 20) / 4)),
          investment: Math.min(20, Math.floor(investmentRatio * 6.67)),
          age: Math.min(20, Math.floor(actualMultiple / (Math.max(1, age) * 0.005))),
        }
      })

      // Update dashboard state
      localStorage.setItem('dashboard_health', finalScore.toString())
      window.dispatchEvent(new Event("storage"))

      // Alert AI context
      handleSendMessage(`I just generated my financial health score. My overall score is ${finalScore}/100. I have ${emergencyMonths.toFixed(1)} months of emergency savings, a ${debtToIncome.toFixed(1)}% Debt-to-Income ratio, and a savings rate of ${savingsRate.toFixed(1)}%. What actionable steps should I take to improve these specific bottlenecks over the next quarter?`)

    } finally {
      setCalculating(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600"
    if (score >= 60) return "text-yellow-600"
    if (score >= 40) return "text-orange-600"
    return "text-red-600"
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent"
    if (score >= 60) return "Good"
    if (score >= 40) return "Fair"
    return "Needs Improvement"
  }

  if (!hasLoaded) return null

  // Skeleton Loader Component
  const SkeletonLoader = () => (
    <div className="space-y-4">
      {[1, 2, 3, 4].map(i => (
        <div key={i} className="p-4 bg-gradient-to-r from-slate-200/30 to-slate-100/30 dark:from-slate-800/30 dark:to-slate-700/30 rounded-2xl border border-slate-200/30 dark:border-slate-700/30 animate-pulse h-24" />
      ))}
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50/50 to-slate-100/50 dark:from-slate-950/50 dark:to-slate-900/50">
      <div className="container mx-auto p-4 md:p-8">
        {/* Header Section */}
        <div className="mb-10 animate-fade-in">
          <div className="flex items-center gap-4 mb-3">
            <div className="p-3 bg-gradient-to-br from-red-500/20 to-red-600/10 rounded-2xl border border-red-200/30 dark:border-red-800/30">
              <span className="text-2xl">💪</span>
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">
                DhanRaksha
              </h1>
              <p className="text-muted-foreground mt-1">Financial Health Diagnostic & Wellness Score</p>
            </div>
            <Badge className="bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white border-0 px-4 py-1.5 text-sm font-semibold">
              Active
            </Badge>
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2 lg:items-start">
          {/* Left Column - Form & Results */}
          <div className="space-y-6">
            {/* Assessment Form Card */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
              <div className="h-1 bg-gradient-to-r from-red-500 via-orange-500 to-red-600" />
              <CardHeader className="pb-4">
                <div className="space-y-1">
                  <CardTitle className="text-2xl flex items-center gap-2">
                    <span>Health Assessment</span>
                  </CardTitle>
                  <CardDescription>Fill in your financial metrics to generate insights</CardDescription>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-5">
                  {[
                    { label: "Monthly Income (₹)", field: "monthlyIncome" },
                    { label: "Monthly Expenses (₹)", field: "monthlyExpenses" },
                    { label: "Emergency Fund (₹)", field: "emergencyFund" },
                    { label: "Total Debt (₹)", field: "totalDebt" },
                    { label: "Total Investments (₹)", field: "investments" },
                    { label: "Age (years)", field: "age" },
                  ].map(({ label, field }) => (
                    <div key={field} className="space-y-2 group">
                      <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within:text-red-600 transition-colors">
                        {label}
                      </Label>
                      <Input
                        type="number"
                        value={formData[field as keyof typeof formData]}
                        onChange={(e) => handleChange(field, e.target.value)}
                        className="border-slate-200/50 dark:border-slate-700/50 focus:border-red-400 focus:ring-red-400/20 h-10 placeholder:text-slate-400 transition-all duration-200"
                        placeholder="0"
                      />
                    </div>
                  ))}
                </div>
                
                <Button
                  onClick={calculateHealthScore}
                  disabled={calculating}
                  className="w-full h-12 text-base font-semibold bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {calculating ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="w-5 h-5 mr-2" />
                      Generate Health Score
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Results Cards */}
            {result && (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-6 duration-500">
                {/* Overall Score Card */}
                <Card className="border-0 shadow-lg overflow-hidden bg-gradient-to-br from-slate-50 to-slate-100/50 dark:from-slate-900/50 dark:to-slate-800/30">
                  <div className="h-1 bg-gradient-to-r from-red-500 via-orange-500 to-red-600" />
                  <CardHeader>
                    <CardTitle className="text-xl">Overall Health Score</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-4">
                      <div className="flex items-end gap-4">
                        <div className="flex-1">
                          <p className={`text-6xl font-black tracking-tight ${getScoreColor(result.overallScore)}`}>
                            {result.overallScore}
                          </p>
                          <p className="text-sm text-muted-foreground mt-1">out of 100</p>
                        </div>
                        <Badge className={`px-4 py-2 text-sm font-semibold ${
                          result.overallScore >= 80 ? 'bg-green-500/20 text-green-700 dark:text-green-400' :
                          result.overallScore >= 60 ? 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-400' :
                          result.overallScore >= 40 ? 'bg-orange-500/20 text-orange-700 dark:text-orange-400' :
                          'bg-red-500/20 text-red-700 dark:text-red-400'
                        } border-0`}>
                          {getScoreLabel(result.overallScore)}
                        </Badge>
                      </div>
                      <div className="space-y-2">
                        <Progress
                          value={result.overallScore}
                          className="h-3 bg-slate-200/50 dark:bg-slate-700/50"
                        />
                        <p className="text-xs text-muted-foreground">Based on 5 key financial metrics</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Metrics Grid */}
                <div className="grid md:grid-cols-2 gap-4">
                  {[
                    { title: "Savings Rate", value: result.savingsRate.toFixed(1), unit: "%", icon: "📊" },
                    { title: "Emergency Fund", value: result.emergencyMonths.toFixed(1), unit: " months", icon: "🛡️" },
                    { title: "Debt-to-Income", value: result.debtToIncome.toFixed(1), unit: "%", icon: "💳" },
                    { title: "Investment Ratio", value: result.investmentRatio.toFixed(1), unit: "x", icon: "📈" },
                  ].map((metric, idx) => (
                    <Card key={idx} className="border-slate-200/30 dark:border-slate-700/30 hover:shadow-md transition-all duration-300 overflow-hidden group">
                      <CardContent className="p-5 space-y-3">
                        <div className="flex items-start justify-between">
                          <div className="space-y-1 flex-1">
                            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">{metric.title}</p>
                            <p className="text-3xl font-bold tracking-tight">
                              {metric.value}<span className="text-lg font-semibold text-muted-foreground">{metric.unit}</span>
                            </p>
                          </div>
                          <span className="text-2xl opacity-60 group-hover:opacity-100 transition-opacity">{metric.icon}</span>
                        </div>
                        <Progress
                          value={Math.min(100, parseFloat(metric.value) * 10)}
                          className="h-2 bg-slate-200/50 dark:bg-slate-700/50"
                        />
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {/* Recommendations Card */}
                {result.recommendations.length > 0 && (
                  <Card className="border-0 shadow-lg overflow-hidden bg-gradient-to-br from-red-50/50 to-orange-50/30 dark:from-red-950/20 dark:to-orange-950/10 border border-red-200/30 dark:border-red-800/30">
                    <div className="h-1 bg-gradient-to-r from-red-500 to-orange-600" />
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2 text-red-900 dark:text-red-400">
                        <AlertCircle className="w-5 h-5" />
                        Areas to Improve
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-3">
                        {result.recommendations.map((rec: string, idx: number) => (
                          <li key={idx} className="flex gap-3 p-3 bg-white/50 dark:bg-slate-900/30 rounded-lg border border-red-200/20 dark:border-red-800/20 group hover:bg-white dark:hover:bg-slate-900/50 transition-colors">
                            <span className="flex-shrink-0 text-red-600 dark:text-red-400 font-bold mt-0.5">→</span>
                            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </div>

          {/* Right Column - AI Chat */}
          <div className="lg:sticky lg:top-8">
            <Card className="border-0 shadow-xl overflow-hidden flex flex-col h-[700px] bg-white dark:bg-slate-900">
              <div className="h-1.5 bg-gradient-to-r from-red-500 via-orange-500 to-red-600" />
              
              <CardHeader className="bg-gradient-to-br from-red-50/80 to-orange-50/50 dark:from-slate-950 dark:to-slate-900 border-b border-red-200/20 dark:border-red-900/30 px-6 py-5">
                <div className="space-y-1">
                  <CardTitle className="text-xl flex items-center gap-3">
                    <span className="text-2xl">🩺</span>
                    <span>DhanRaksha Consult</span>
                  </CardTitle>
                  <CardDescription className="text-sm">Get personalized financial wellness advice</CardDescription>
                </div>
              </CardHeader>

              <CardContent className="flex-1 flex flex-col p-0 overflow-hidden bg-gradient-to-b from-white/80 to-slate-50/50 dark:from-slate-900/60 dark:to-slate-900">
                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto p-5 space-y-4 max-h-[580px] scrollbar-thin scrollbar-thumb-red-300 dark:scrollbar-thumb-red-700 scrollbar-track-transparent">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-3 duration-400`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-sm px-4 py-3 rounded-2xl transition-all duration-200 ${
                          msg.role === "user"
                            ? "bg-gradient-to-br from-red-600 to-orange-600 text-white shadow-lg hover:shadow-xl"
                            : "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-red-200/40 dark:border-red-900/40 shadow-sm"
                        }`}
                      >
                        <div className="text-sm leading-relaxed whitespace-pre-wrap break-words font-medium">
                          {parseMarkdown(msg.content)}
                        </div>
                      </div>
                    </div>
                  ))}

                  {chatLoading && (
                    <div className="flex justify-start animate-in fade-in slide-in-from-left-2 duration-300">
                      <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-5 py-3.5 border border-red-200/40 dark:border-red-900/40 shadow-sm flex items-center gap-3">
                        <Loader2 className="w-4 h-4 animate-spin text-red-500 dark:text-red-400" />
                        <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">DhanRaksha is analyzing...</span>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="border-t border-red-200/20 dark:border-red-900/30 bg-gradient-to-r from-white to-red-50/30 dark:from-slate-900 dark:to-red-950/20 p-5 space-y-3">
                  <form
                    onSubmit={(e) => {
                      e.preventDefault()
                      handleSendMessage()
                    }}
                    className="flex gap-3 items-center"
                  >
                    <div className="flex-1 relative">
                      <Input
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        placeholder="Ask about debt, savings, health score..."
                        disabled={chatLoading}
                        className="border-red-200/50 dark:border-red-900/50 dark:bg-slate-800/50 focus:border-red-400 focus:ring-red-500/30 rounded-full h-11 px-5 placeholder:text-slate-500 dark:placeholder:text-slate-400 transition-all duration-200 shadow-md focus:shadow-lg"
                      />
                    </div>
                    <Button
                      type="submit"
                      disabled={chatLoading || !chatInput.trim()}
                      className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white rounded-full w-11 h-11 p-0 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
                    >
                      <Send className="w-5 h-5" />
                    </Button>
                  </form>
                  <p className="text-xs text-slate-500 dark:text-slate-400 px-2">Press Enter or click send</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
