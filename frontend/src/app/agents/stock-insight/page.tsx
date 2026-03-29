"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Loader2, TrendingUp, TrendingDown, Send, Search } from "lucide-react"
import { toast } from "sonner"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function StockInsightPage() {
  const [symbol, setSymbol, hasLoaded] = useLocalStorage("bazaar_symbol", "")
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am StockInsight, your AI Stock Market Analyst. Search for a stock ticker to analyze its fundamentals, or ask me directly about market trends and technical indicators!"
  }])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

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
          agent_id: "stock-insight"
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
          content: "Sorry, the StockInsight agent is offline."
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

  const searchStock = async (querySymbol?: string) => {
    const searchTarget = querySymbol || symbol
    if (!searchTarget.trim()) return
    
    setSymbol(searchTarget)
    setLoading(true)
    try {
      const response = await fetch("/api/stock-insight", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol: searchTarget.toUpperCase() }),
      })
      if (!response.ok) {
        setResult(null)
        toast.error("Ticker not found or API limits executed. Check your symbol.")
        return
      }
      const data = await response.json()
      setResult(data)
      toast.success(`Successfully fetched ${searchTarget}`)

      // Send context to AI
      handleSendMessage(`I just pulled up real-time quotes for ${data.name} (${data.symbol}). It is currently trading at ₹${data.price} with a P/E Ratio of ${data.pe_ratio}. Can you give me a structural analysis of this company? Should I buy, hold, or sell at this valuation?`)

    } catch (error) {
      setResult(null)
      toast.error("Backend is offline. Please ensure the FastAPI server is running.")
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(value)
  }

  const formatNumber = (value: number) => {
    if (value >= 10000000) return (value / 10000000).toFixed(2) + " Cr"
    if (value >= 100000) return (value / 100000).toFixed(2) + " L"
    return value.toLocaleString("en-IN")
  }

  if (!hasLoaded) return null

  // Skeleton Loader Component
  const SkeletonLoader = () => (
    <div className="space-y-3">
      {[1, 2, 3].map(i => (
        <div key={i} className="p-4 bg-gradient-to-r from-slate-200/30 to-slate-100/30 dark:from-slate-800/30 dark:to-slate-700/30 rounded-2xl border border-slate-200/30 dark:border-slate-700/30 animate-pulse h-20" />
      ))}
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50/50 to-slate-100/50 dark:from-slate-950/50 dark:to-slate-900/50">
      <div className="container mx-auto p-4 md:p-8">
        {/* Header Section */}
        <div className="mb-10 animate-fade-in">
          <div className="flex items-center gap-4 mb-3">
            <div className="p-3 bg-gradient-to-br from-pink-500/20 to-pink-600/10 rounded-2xl border border-pink-200/30 dark:border-pink-800/30">
              <span className="text-2xl">📈</span>
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-rose-600 bg-clip-text text-transparent">
                StockInsight
              </h1>
              <p className="text-muted-foreground mt-1">Real-time Stock Analysis & AI-Powered Fundamental Review</p>
            </div>
            <Badge className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white border-0 px-4 py-1.5 text-sm font-semibold">
              Active
            </Badge>
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2 lg:items-start">
          {/* Left Column - Search & Results */}
          <div className="space-y-6">
            {/* Search Card */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
              <div className="h-1 bg-gradient-to-r from-pink-500 via-rose-500 to-pink-600" />
              <CardHeader className="pb-4">
                <div className="space-y-1">
                  <CardTitle className="text-2xl flex items-center gap-2">
                    <span>Stock Lookup</span>
                  </CardTitle>
                  <CardDescription>Search NSE/BSE ticker symbols for real-time quotes</CardDescription>
                </div>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-3">
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Stock Symbol</Label>
                  <div className="flex gap-3">
                    <Input
                      id="symbol"
                      placeholder="e.g., RELIANCE, TCS, INFY"
                      value={symbol}
                      onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault()
                          searchStock()
                        }
                      }}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-pink-400 focus:ring-pink-400/20 h-10 placeholder:text-slate-400 transition-all duration-200"
                    />
                    <Button
                      onClick={() => searchStock()}
                      disabled={loading || !symbol.trim()}
                      className="bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-700 hover:to-rose-700 text-white px-6 h-10 shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                    >
                      {loading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Search className="w-5 h-5" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Quick Symbol Badges */}
                <div className="border-t border-slate-200/20 dark:border-slate-700/20 pt-4">
                  <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3">Popular Stocks</p>
                  <div className="flex flex-wrap gap-2">
                    {["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"].map((sym) => (
                      <Badge
                        key={sym}
                        variant="outline"
                        onClick={() => searchStock(sym)}
                        className="cursor-pointer border-pink-200/50 dark:border-pink-800/50 hover:bg-pink-50 dark:hover:bg-pink-950/30 hover:text-pink-700 dark:hover:text-pink-400 transition-all duration-200 px-3 py-1.5"
                      >
                        {sym}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stock Details Card */}
            {result && (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-6 duration-500">
                <Card className="border-0 shadow-lg overflow-hidden">
                  <div className="h-1 bg-gradient-to-r from-pink-500 via-rose-500 to-pink-600" />
                  <CardHeader className="bg-gradient-to-br from-pink-50/80 to-rose-50/50 dark:from-pink-950/30 dark:to-rose-950/20 pb-4">
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1 space-y-1">
                        <CardTitle className="text-2xl">{result.name}</CardTitle>
                        <CardDescription className="text-sm font-medium">{result.symbol}</CardDescription>
                      </div>
                      <div className="text-right space-y-2">
                        <p className="text-4xl font-black tracking-tight font-mono">₹{result.price.toFixed(2)}</p>
                        <Badge
                          className={`px-3 py-1 text-sm font-bold border-0 ${
                            result.change >= 0
                              ? 'bg-green-500/20 text-green-700 dark:text-green-400'
                              : 'bg-red-500/20 text-red-700 dark:text-red-400'
                          }`}
                        >
                          {result.change >= 0 ? (
                            <>
                              <TrendingUp className="w-4 h-4 inline mr-1" />
                              ₹{Math.abs(result.change).toFixed(2)} (+{(result.change_percent || 0).toFixed(2)}%)
                            </>
                          ) : (
                            <>
                              <TrendingDown className="w-4 h-4 inline mr-1" />
                              ₹{Math.abs(result.change).toFixed(2)} ({(result.change_percent || 0).toFixed(2)}%)
                            </>
                          )}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>

                  <CardContent className="pt-6 space-y-5">
                    {/* Key Metrics */}
                    <div className="grid md:grid-cols-4 gap-4">
                      {[
                        { label: "Day High", value: `₹${result.high.toFixed(2)}`, icon: "📈" },
                        { label: "Day Low", value: `₹${result.low.toFixed(2)}`, icon: "📉" },
                        { label: "Volume", value: formatNumber(result.volume), icon: "📊" },
                        { label: "P/E Ratio", value: (result.pe_ratio || 0).toFixed(2), icon: "💰" },
                      ].map((metric, idx) => (
                        <div key={idx} className="p-4 bg-slate-50/60 dark:bg-slate-900/20 rounded-xl border border-slate-200/30 dark:border-slate-700/30 hover:border-pink-300/50 dark:hover:border-pink-700/30 transition-all duration-200 group">
                          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">{metric.label}</p>
                          <div className="flex items-end justify-between">
                            <p className="text-lg font-bold tracking-tight">{metric.value}</p>
                            <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">{metric.icon}</span>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Market Cap */}
                    <div className="p-5 bg-gradient-to-br from-pink-50/60 to-rose-50/40 dark:from-pink-950/20 dark:to-rose-950/10 rounded-xl border border-pink-200/30 dark:border-pink-800/30">
                      <p className="text-xs font-semibold text-pink-700 dark:text-pink-400 uppercase tracking-wide mb-2">Market Capitalization</p>
                      <p className="text-3xl font-bold text-pink-900 dark:text-pink-300">
                        ₹{formatNumber((result.market_cap || 0) * 10000000)}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>

          {/* Right Column - AI Chat */}
          <div className="lg:sticky lg:top-8">
            <Card className="border-0 shadow-xl overflow-hidden flex flex-col h-[700px] bg-white dark:bg-slate-900">
              <div className="h-1.5 bg-gradient-to-r from-pink-500 via-rose-500 to-pink-600" />

              <CardHeader className="bg-gradient-to-br from-pink-50/80 to-rose-50/50 dark:from-slate-950 dark:to-slate-900 border-b border-pink-200/20 dark:border-pink-900/30 px-6 py-5">
                <div className="space-y-1">
                  <CardTitle className="text-xl flex items-center gap-3">
                    <span className="text-2xl">🧠</span>
                    <span>StockInsight Consult</span>
                  </CardTitle>
                  <CardDescription className="text-sm">Real-time stock analysis from your AI analyst</CardDescription>
                </div>
              </CardHeader>

              <CardContent className="flex-1 flex flex-col p-0 overflow-hidden bg-gradient-to-b from-white/80 to-slate-50/50 dark:from-slate-900/60 dark:to-slate-900">
                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto p-5 space-y-4 max-h-[580px] scrollbar-thin scrollbar-thumb-pink-300 dark:scrollbar-thumb-pink-700 scrollbar-track-transparent">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-3 duration-400`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-sm px-4 py-3 rounded-2xl transition-all duration-200 ${
                          msg.role === "user"
                            ? "bg-gradient-to-br from-pink-600 to-rose-600 text-white shadow-lg hover:shadow-xl"
                            : "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-pink-200/40 dark:border-pink-900/40 shadow-sm"
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
                      <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-5 py-3.5 border border-pink-200/40 dark:border-pink-900/40 shadow-sm flex items-center gap-3">
                        <Loader2 className="w-4 h-4 animate-spin text-pink-500 dark:text-pink-400" />
                        <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">Analyzing market conditions...</span>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="border-t border-pink-200/20 dark:border-pink-900/30 bg-gradient-to-r from-white to-pink-50/30 dark:from-slate-900 dark:to-pink-950/20 p-5 space-y-3">
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
                        placeholder="Ask about valuation, P/E ratio, technical analysis..."
                        disabled={chatLoading}
                        className="border-pink-200/50 dark:border-pink-900/50 dark:bg-slate-800/50 focus:border-pink-400 focus:ring-pink-500/30 rounded-full h-11 px-5 placeholder:text-slate-500 dark:placeholder:text-slate-400 transition-all duration-200 shadow-md focus:shadow-lg"
                      />
                    </div>
                    <Button
                      type="submit"
                      disabled={chatLoading || !chatInput.trim()}
                      className="bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-700 hover:to-rose-700 text-white rounded-full w-11 h-11 p-0 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
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
