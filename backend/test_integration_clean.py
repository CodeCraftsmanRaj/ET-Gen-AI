#!/usr/bin/env python3
"""
Integration test suite for AI Money Mentor
Tests all 9 agents with their new names (cross-platform compatible)
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TIMEOUT = 10

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = {"passed": 0, "failed": 0, "skipped": 0}
    
    def print_test(self, name: str, status: str, details: str = ""):
        icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⊘"
        color = GREEN if status == "PASS" else RED if status == "FAIL" else YELLOW
        
        status_str = f"{color}{icon} {status}{RESET}"
        detail_str = f" - {details}" if details else ""
        print(f"  {name:40} {status_str}{detail_str}")
    
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.print_test("Health Check", "PASS")
                    self.results["passed"] += 1
                    return True
            self.print_test("Health Check", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("Health Check", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint with new agent names"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                agents = data.get("agents", [])
                
                required_agents = [
                    "portfolio-wise",
                    "tax-master",
                    "retirement-pro",
                    "stock-insight",
                    "money-health",
                    "compliance-helper",
                    "dhan-sarthi",
                    "life-goals",
                    "partner-finance"
                ]
                
                missing = [a for a in required_agents if a not in agents]
                if missing:
                    self.print_test("Root Endpoint (Agents)", "FAIL", f"Missing: {missing}")
                    self.results["failed"] += 1
                    return False
                
                self.print_test("Root Endpoint (Agents)", "PASS", f"All {len(agents)} agents registered")
                self.results["passed"] += 1
                return True
            
            self.print_test("Root Endpoint", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("Root Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_tax_master_endpoint(self) -> bool:
        """Test tax-master endpoint (renamed from karvid)"""
        try:
            response = requests.post(
                f"{self.base_url}/tax-master/calculate-tax",
                json={"income": 1000000, "regime": "new"},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "tax" in data or "regime" in data:
                    self.print_test("tax-master (TaxMaster)", "PASS")
                    self.results["passed"] += 1
                    return True
            
            self.print_test("tax-master", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("tax-master", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_retirement_pro_endpoint(self) -> bool:
        """Test retirement-pro endpoint (renamed from yojana)"""
        try:
            response = requests.post(
                f"{self.base_url}/retirement-pro/fire-number",
                json={"monthly_expenses": 50000},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "fire_number" in data or "monthly_expenses" in data:
                    self.print_test("retirement-pro (RetirementPro)", "PASS")
                    self.results["passed"] += 1
                    return True
            
            self.print_test("retirement-pro", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("retirement-pro", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_money_health_endpoint(self) -> bool:
        """Test money-health endpoint (renamed from dhan)"""
        try:
            response = requests.post(
                f"{self.base_url}/money-health/health-score",
                json={
                    "income": 1200000,
                    "expenses": 800000,
                    "monthly_savings": 40000,
                    "debt": 0
                },
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                self.print_test("money-health (MoneyHealth)", "PASS")
                self.results["passed"] += 1
                return True
            
            self.print_test("money-health", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("money-health", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_stock_insight_endpoint(self) -> bool:
        """Test stock-insight endpoint (renamed from bazaar)"""
        try:
            response = requests.post(
                f"{self.base_url}/stock-insight/stock-quote",
                json={"symbol": "TCS"},
                timeout=TIMEOUT
            )
            
            # Accept 200 or 404 (symbol may not exist)
            if response.status_code in [200, 404]:
                self.print_test("stock-insight (StockInsight)", "PASS", f"Status {response.status_code}")
                self.results["passed"] += 1
                return True
            
            self.print_test("stock-insight", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("stock-insight", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_portfolio_wise_endpoint(self) -> bool:
        """Test portfolio-wise endpoint (renamed from niveshak)"""
        try:
            response = requests.post(
                f"{self.base_url}/portfolio-wise/xirr",
                json={"transactions": [
                    {"date": "2023-01-01", "amount": -100000},
                    {"date": "2024-01-01", "amount": 115000}
                ]},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                self.print_test("portfolio-wise (PortfolioWise)", "PASS")
                self.results["passed"] += 1
                return True
            
            self.print_test("portfolio-wise", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("portfolio-wise", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_compliance_helper_endpoint(self) -> bool:
        """Test compliance-helper endpoint (renamed from vidhi)"""
        try:
            response = requests.get(
                f"{self.base_url}/compliance-helper/disclaimers",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                self.print_test("compliance-helper (ComplianceHelper)", "PASS")
                self.results["passed"] += 1
                return True
            
            self.print_test("compliance-helper", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("compliance-helper", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_life_goals_endpoint(self) -> bool:
        """Test life-goals endpoint (renamed from life_event)"""
        try:
            response = requests.get(
                f"{self.base_url}/life-goals/types",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                self.print_test("life-goals (LifeGoals)", "PASS")
                self.results["passed"] += 1
                return True
            
            self.print_test("life-goals", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("life-goals", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_partner_finance_endpoint(self) -> bool:
        """Test partner-finance endpoint (renamed from couple_planner)"""
        try:
            response = requests.post(
                f"{self.base_url}/partner-finance/finances",
                json={
                    "partner1_income": 1000000,
                    "partner2_income": 800000
                },
                timeout=TIMEOUT
            )
            
            if response.status_code in [200, 400, 422]:  # 422 for validation errors is ok
                self.print_test("partner-finance (PartnerFinance)", "PASS", f"Status {response.status_code}")
                self.results["passed"] += 1
                return True
            
            self.print_test("partner-finance", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("partner-finance", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_dhan_sarthi_coordinator(self) -> bool:
        """Test dhan-sarthi coordinator routing"""
        try:
            response = requests.post(
                f"{self.base_url}/dhan-sarthi/route",
                json={"query": "How do I save taxes?"},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "primary_agent" in data or "agents" in data:
                    self.print_test("dhan-sarthi (Coordinator)", "PASS")
                    self.results["passed"] += 1
                    return True
            
            self.print_test("dhan-sarthi", "FAIL", f"Status {response.status_code}")
            self.results["failed"] += 1
            return False
        except Exception as e:
            self.print_test("dhan-sarthi", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def print_summary(self) -> bool:
        """Print test summary"""
        total = self.results["passed"] + self.results["failed"] + self.results["skipped"]
        
        print(f"\n{'='*60}")
        print(f"Test Summary")
        print(f"{'='*60}")
        print(f"{GREEN}✓ Passed: {self.results['passed']}{RESET}")
        if self.results["failed"] > 0:
            print(f"{RED}✗ Failed: {self.results['failed']}{RESET}")
        if self.results["skipped"] > 0:
            print(f"{YELLOW}⊘ Skipped: {self.results['skipped']}{RESET}")
        print(f"{'='*60}")
        
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.results["failed"] == 0:
            print(f"\n{GREEN}{BOLD}✨ All tests passed! Integration working correctly.{RESET}")
        else:
            print(f"\n{RED}{BOLD}⚠️  Some tests failed. Check details above.{RESET}")
        
        return self.results["failed"] == 0

def main():
    print(f"\n{'='*60}")
    print("AI Money Mentor - Backend Integration Test")
    print(f"Testing 9 agents with new names (cross-platform)")
    print(f"{'='*60}\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except Exception:
        print(f"{RED}✗ Backend server not running at {BASE_URL}{RESET}")
        print(f"\nStart the backend with:")
        print(f"  cd backend")
        print(f"  uv run uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload")
        sys.exit(1)
    
    tester = APITester(BASE_URL)
    
    # Run all tests
    print(f"{BLUE}Running endpoint tests...{RESET}\n")
    tester.test_health()
    tester.test_root_endpoint()
    tester.test_tax_master_endpoint()
    tester.test_retirement_pro_endpoint()
    tester.test_money_health_endpoint()
    tester.test_stock_insight_endpoint()
    tester.test_portfolio_wise_endpoint()
    tester.test_compliance_helper_endpoint()
    tester.test_life_goals_endpoint()
    tester.test_partner_finance_endpoint()
    tester.test_dhan_sarthi_coordinator()
    
    # Print summary
    success = tester.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
