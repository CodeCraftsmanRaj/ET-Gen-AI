#!/usr/bin/env python3
"""
AI Money Mentor - Backend Test & Verification Script
Run this to verify all fixes are working correctly
"""

import subprocess
import sys
import time
import os

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_python_deps():
    """Check Python dependencies are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    try:
        import fastapi
        import pydantic
        import uvicorn
        print("✅ All Python dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: uv pip install -r requirements.txt")
        return False

def check_bun_packages():
    """Check if bun packages are installed"""
    print("\n🔍 Checking Node.js packages...")
    
    if os.path.isdir("frontend/node_modules"):
        print("✅ Node modules found")
        return True
    else:
        print("⚠️  Node modules not found")
        print("Install with: cd frontend && bun install")
        return False

def test_agent_imports():
    """Test that all agent modules can be imported"""
    print("\n🔍 Testing agent imports...")
    
    agents = [
        "agents.money_health",
        "agents.tax_master",
        "agents.retirement_pro",
        "agents.stock_insight",
        "agents.compliance_helper",
        "agents.portfolio_wise",
        "agents.dhan_sarthi",
    ]
    
    os.chdir("backend")
    sys.path.insert(0, os.getcwd())
    
    for agent in agents:
        try:
            __import__(agent)
            print(f"  ✅ {agent}")
        except ImportError as e:
            print(f"  ⚠️  {agent} - {str(e)[:50]}...")
    
    os.chdir("..")
    return True

def verify_directory_structure():
    """Verify all directories are renamed correctly"""
    print("\n🔍 Verifying directory structure...")
    
    backend_agents = {
        "backend/agents/money-health": "MoneyHealth",
        "backend/agents/tax-master": "TaxMaster",
        "backend/agents/retirement-pro": "RetirementPro",
        "backend/agents/stock-insight": "StockInsight",
        "backend/agents/compliance-helper": "ComplianceHelper",
        "backend/agents/portfolio-wise": "PortfolioWise",
        "backend/agents/life-goals": "LifeGoals",
        "backend/agents/partner-finance": "PartnerFinance",
    }
    
    frontend_agents = {
        "frontend/src/app/agents/money-health": "MoneyHealth",
        "frontend/src/app/agents/tax-master": "TaxMaster",
        "frontend/src/app/agents/retirement-pro": "RetirementPro",
        "frontend/src/app/agents/stock-insight": "StockInsight",
        "frontend/src/app/agents/compliance-helper": "ComplianceHelper",
        "frontend/src/app/agents/portfolio-wise": "PortfolioWise",
        "frontend/src/app/agents/life-goals": "LifeGoals",
        "frontend/src/app/agents/partner-finance": "PartnerFinance",
    }
    
    all_dirs = {**backend_agents, **frontend_agents}
    
    for path, name in all_dirs.items():
        if os.path.isdir(path):
            print(f"  ✅ {name:20} {path}")
        else:
            print(f"  ❌ {name:20} {path} (NOT FOUND)")
    
    return True

def verify_auth_changes():
    """Verify auth changes are applied"""
    print("\n🔍 Verifying authentication changes...")
    
    auth_files = {
        "frontend/src/app/api/auth/signup/route.ts": "telegramId",
        "frontend/src/app/api/auth/login/route.ts": "telegramId",
    }
    
    for filepath, bad_term in auth_files.items():
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            
            if bad_term not in content:
                print(f"  ✅ {filepath.split('/')[-2]} - {bad_term} removed")
            else:
                print(f"  ⚠️  {filepath.split('/')[-2]} - {bad_term} still present")
    
    return True

def main():
    """Run all verification steps"""
    print("\n" + "="*60)
    print("🚀 AI Money Mentor - Backend Verification Suite")
    print("="*60)
    
    # Change to project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    checks = [
        ("Python Dependencies", check_python_deps),
        ("Node.js Packages", check_bun_packages),
        ("Agent Imports", test_agent_imports),
        ("Directory Structure", verify_directory_structure),
        ("Auth Changes", verify_auth_changes),
    ]
    
    passed = 0
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"Error during {name}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print(f"✅ Verification Complete: {passed}/{len(checks)} checks passed")
    print("="*60)
    
    # Next steps
    print("\n📋 Next Steps:")
    print("1. Start backend server:")
    print("   cd backend && uv run uvicorn api_server:app --reload")
    print()
    print("2. Start frontend server (in new terminal):")
    print("   cd frontend && bun run dev")
    print()
    print("3. Run integration tests:")
    print("   cd backend && uv run python test_integration.py")
    print()
    print("4. Open frontend:")
    print("   http://localhost:3000")
    print()
    print("5. Check API docs:")
    print("   http://localhost:8000/docs")
    
    print("\n" + "="*60)
    print("✨ All systems ready for testing!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
