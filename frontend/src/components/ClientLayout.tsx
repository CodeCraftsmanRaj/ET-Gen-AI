"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Menu, X } from "lucide-react"
import { Toaster } from "sonner"

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [mounted, setMounted] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  if (!mounted) return null

  return (
    <>
      <header
        className={`sticky top-0 z-50 transition-all duration-300 gradient-border ${
          scrolled
            ? "bg-background/80 backdrop-blur-xl shadow-lg"
            : "bg-background/60 backdrop-blur-md"
        }`}
      >
        <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <span className="text-2xl transition-transform duration-300 group-hover:scale-110">💰</span>
            <span className="hidden sm:inline text-xl font-bold gradient-text">AI Money Mentor</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden sm:flex items-center gap-3">
            <Link href="/" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">Home</Link>
            <Link href="/agents/coordinator" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">Ask Coordinator</Link>
          </div>

          {/* Mobile Toggle */}
          <div className="flex sm:hidden items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-muted-foreground"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </nav>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="sm:hidden border-t border-border bg-background/95 backdrop-blur-xl animate-fade-in">
            <div className="container mx-auto px-4 py-3 space-y-2">
              <Link
                href="/"
                className="block py-2 text-sm font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                🏠 Home
              </Link>
              <Link href="/agents/coordinator" className="block py-2 text-sm font-medium hover:text-primary transition-colors" onClick={() => setMobileMenuOpen(false)}>🧠 Ask Coordinator</Link>
            </div>
          </div>
        )}
      </header>

      <main className="flex-1 container mx-auto px-4 py-6">{children}</main>

      <footer className="border-t border-border bg-card/80 backdrop-blur-sm py-6">
        <div className="container mx-auto px-4 text-center space-y-2">
          <p className="text-sm text-muted-foreground">
            ⚠️ SEBI Disclaimer: This is for educational purposes only. Not financial advice.
          </p>
          <p className="text-xs text-muted-foreground/60">
            © 2026 AI Money Mentor | ET AI Hackathon
          </p>
        </div>
      </footer>

      <Toaster richColors position="top-right" />
    </>
  )
}
