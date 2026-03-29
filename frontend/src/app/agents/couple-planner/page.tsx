'use client'

import { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Send, Loader2, Users } from 'lucide-react'
import { parseMarkdown } from '@/lib/markdown'

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function CouplePlannerPage() {
  // Person 1
  const [person1Name, setPerson1Name] = useState('Partner 1')
  const [person1Income, setPerson1Income] = useState(50000)
  const [person1Expenses, setPerson1Expenses] = useState(30000)

  // Person 2
  const [person2Name, setPerson2Name] = useState('Partner 2')
  const [person2Income, setPerson2Income] = useState(50000)
  const [person2Expenses, setPerson2Expenses] = useState(30000)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init",
    role: "assistant",
    content: "I am the Couple's Finance Planner. Fill out the joint income form or ask me directly to help plan your shared finances, budgets, and couples' SIPs!",
  }])
  const [input, setInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (customQuery?: string) => {
    const query = customQuery || input.trim()
    if (!query || chatLoading) return

    if (!customQuery) setInput("")
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
          agent_id: "couple-planner"
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
          content: "Sorry, the AI planner is offline."
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

  const handleCreatePlan = () => {
    const query = `Create a joint financial plan for ${person1Name} (Income: ₹${person1Income}, Expenses: ₹${person1Expenses}) and ${person2Name} (Income: ₹${person2Income}, Expenses: ₹${person2Expenses}). How should we split our rent and savings organically?`
    handleSendMessage(query)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50/50 to-slate-100/50 dark:from-slate-950/50 dark:to-slate-900/50">
      <div className="container mx-auto p-4 md:p-8">
        {/* Header Section */}
        <div className="mb-10 animate-fade-in">
          <div className="flex items-center gap-4 mb-3">
            <div className="p-3 bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-2xl border border-purple-200/30 dark:border-purple-800/30">
              <span className="text-2xl">💑</span>
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Couple&apos;s AI Planner
              </h1>
              <p className="text-muted-foreground mt-1">Plan your shared finances together intelligently</p>
            </div>
            <Badge className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white border-0 px-4 py-1.5 text-sm font-semibold">
              Active
            </Badge>
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2 lg:items-start">
          {/* Left Column - Partner Forms */}
          <div className="space-y-6">
            {/* Partner 1 Card */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden group">
              <div className="h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-600" />
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2.5 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl">
                    <span className="text-xl">👤</span>
                  </div>
                  <CardTitle className="text-xl">{person1Name}</CardTitle>
                </div>
                <CardDescription>Partner 1 financial details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2 group/input">
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-purple-600 transition-colors">
                    Name
                  </Label>
                  <Input
                    value={person1Name}
                    onChange={(e) => setPerson1Name(e.target.value)}
                    className="border-slate-200/50 dark:border-slate-700/50 focus:border-purple-400 focus:ring-purple-400/20 h-10 transition-all duration-200"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2 group/input">
                    <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-purple-600 transition-colors">
                      Monthly Income (₹)
                    </Label>
                    <Input
                      type="number"
                      value={person1Income}
                      onChange={(e) => setPerson1Income(parseFloat(e.target.value) || 0)}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-purple-400 focus:ring-purple-400/20 h-10 transition-all duration-200"
                    />
                  </div>
                  <div className="space-y-2 group/input">
                    <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-purple-600 transition-colors">
                      Monthly Expenses (₹)
                    </Label>
                    <Input
                      type="number"
                      value={person1Expenses}
                      onChange={(e) => setPerson1Expenses(parseFloat(e.target.value) || 0)}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-purple-400 focus:ring-purple-400/20 h-10 transition-all duration-200"
                    />
                  </div>
                </div>
                <div className="p-3 bg-purple-50/60 dark:bg-purple-950/20 border border-purple-200/30 dark:border-purple-800/30 rounded-lg">
                  <p className="text-xs text-purple-700 dark:text-purple-400 font-medium">
                    Monthly Savings: <span className="font-bold">₹{(person1Income - person1Expenses).toLocaleString('en-IN')}</span>
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Partner 2 Card */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden group">
              <div className="h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-pink-600" />
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2.5 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-xl">
                    <span className="text-xl">👤</span>
                  </div>
                  <CardTitle className="text-xl">{person2Name}</CardTitle>
                </div>
                <CardDescription>Partner 2 financial details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2 group/input">
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-pink-600 transition-colors">
                    Name
                  </Label>
                  <Input
                    value={person2Name}
                    onChange={(e) => setPerson2Name(e.target.value)}
                    className="border-slate-200/50 dark:border-slate-700/50 focus:border-pink-400 focus:ring-pink-400/20 h-10 transition-all duration-200"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2 group/input">
                    <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-pink-600 transition-colors">
                      Monthly Income (₹)
                    </Label>
                    <Input
                      type="number"
                      value={person2Income}
                      onChange={(e) => setPerson2Income(parseFloat(e.target.value) || 0)}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-pink-400 focus:ring-pink-400/20 h-10 transition-all duration-200"
                    />
                  </div>
                  <div className="space-y-2 group/input">
                    <Label className="text-sm font-medium text-slate-700 dark:text-slate-300 group-focus-within/input:text-pink-600 transition-colors">
                      Monthly Expenses (₹)
                    </Label>
                    <Input
                      type="number"
                      value={person2Expenses}
                      onChange={(e) => setPerson2Expenses(parseFloat(e.target.value) || 0)}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-pink-400 focus:ring-pink-400/20 h-10 transition-all duration-200"
                    />
                  </div>
                </div>
                <div className="p-3 bg-pink-50/60 dark:bg-pink-950/20 border border-pink-200/30 dark:border-pink-800/30 rounded-lg">
                  <p className="text-xs text-pink-700 dark:text-pink-400 font-medium">
                    Monthly Savings: <span className="font-bold">₹{(person2Income - person2Expenses).toLocaleString('en-IN')}</span>
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Combined Summary Card */}
            <Card className="border-0 shadow-lg overflow-hidden bg-gradient-to-br from-slate-50 to-slate-100/50 dark:from-slate-900/30 dark:to-slate-800/20">
              <div className="h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-600" />
              <CardContent className="pt-6">
                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-1 text-center">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Combined Income</p>
                    <p className="text-xl font-bold tracking-tight">₹{(person1Income + person2Income).toLocaleString('en-IN')}</p>
                  </div>
                  <div className="space-y-1 text-center border-l border-r border-slate-200 dark:border-slate-600/20">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Combined Expenses</p>
                    <p className="text-xl font-bold tracking-tight">₹{(person1Expenses + person2Expenses).toLocaleString('en-IN')}</p>
                  </div>
                  <div className="space-y-1 text-center">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Joint Savings</p>
                    <p className="text-xl font-bold text-purple-600 dark:text-purple-400 tracking-tight">₹{(person1Income + person2Income - person1Expenses - person2Expenses).toLocaleString('en-IN')}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Generate Plan Button */}
            <Button
              onClick={handleCreatePlan}
              disabled={chatLoading}
              className="w-full h-12 text-base font-semibold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {chatLoading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Generating Plan...
                </>
              ) : (
                <>
                  <Users className="w-5 h-5 mr-2" />
                  Generate Joint Financial Plan
                </>
              )}
            </Button>
          </div>

          {/* Right Column - AI Chat */}
          <div className="lg:sticky lg:top-8">
            <Card className="border-0 shadow-xl overflow-hidden flex flex-col h-[700px] bg-gradient-to-b from-slate-50 to-slate-100/50 dark:from-slate-900/30 dark:to-slate-800/20">
              <div className="h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-600" />

              <CardHeader className="bg-gradient-to-br from-purple-50/80 to-pink-50/50 dark:from-purple-950/30 dark:to-pink-950/20 border-b border-purple-200/20 dark:border-purple-800/20">
                <div className="space-y-1">
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-lg">💬 Plan Discussion</span>
                  </CardTitle>
                  <CardDescription>Chat with your joint planning advisor</CardDescription>
                </div>
              </CardHeader>

              <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto p-4 space-y-3 max-h-[580px] scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-600 scrollbar-track-transparent">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}
                    >
                      <div
                        className={`max-w-xs md:max-w-sm px-4 py-3 rounded-2xl transition-all duration-200 ${
                          msg.role === 'user'
                            ? 'bg-gradient-to-br from-purple-600 to-pink-600 text-white shadow-md'
                            : 'bg-slate-200/60 dark:bg-slate-700/60 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-600/30'
                        }`}
                      >
                        <div className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                          {parseMarkdown(msg.content)}
                        </div>
                      </div>
                    </div>
                  ))}

                  {chatLoading && (
                    <div className="flex justify-start animate-in fade-in duration-300">
                      <div className="bg-slate-200/60 dark:bg-slate-700/60 rounded-2xl px-4 py-3 border border-slate-200 dark:border-slate-600/30 flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin text-purple-600 dark:text-purple-400" />
                        <span className="text-sm text-slate-600 dark:text-slate-300">Planning your finances...</span>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="border-t border-slate-200/30 dark:border-slate-700/30 bg-gradient-to-r from-slate-50/50 to-slate-100/50 dark:from-slate-900/20 dark:to-slate-800/20 p-4">
                  <form
                    onSubmit={(e) => {
                      e.preventDefault()
                      handleSendMessage()
                    }}
                    className="flex gap-3"
                  >
                    <Input
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Ask about splits, shared goals..."
                      disabled={chatLoading}
                      className="border-slate-200/50 dark:border-slate-700/50 focus:border-purple-400 focus:ring-purple-400/20 rounded-full h-11 px-5 placeholder:text-slate-400 transition-all duration-200"
                    />
                    <Button
                      type="submit"
                      disabled={chatLoading || !input.trim()}
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-full w-11 h-11 p-0 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                    >
                      <Send className="w-5 h-5" />
                    </Button>
                  </form>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}