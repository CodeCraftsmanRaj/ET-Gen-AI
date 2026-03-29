"""
Integration Test Suite for AI Money Mentor Backend
Tests all endpoints with new agent names to verify cross-platform compatibility
"""

import requests
import json
import sys
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 5

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(name: str, status: str, message: str = ""):
    """Print test result with color coding"""
    status_symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
    status_color = GREEN if status == "PASS" else RED if status == "FAIL" else YELLOW
    
    print(f"{status_color}{status_symbol} {name}{RESET}")
    if message:
        print(f"  → {message}")

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = {"passed": 0, "failed": 0, "skipped": 0}
        
    def test_health(self) -> bool:
        """Test basic health check"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=TIMEOUT)
            if response.status_code == 200:
                print_test("Health Check", "PASS")
                self.results["passed"] += 1
                return True
            else:
                print_test("Health Check", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
        except Exception as e:
            print_test("Health Check", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint with new agent names"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=TIMEOUT)
            if response.status_code != 200:
                print_test("Root Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
            
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
                print_test("Root Endpoint", "FAIL", f"Missing agents: {missing}")
                self.results["failed"] += 1
                return False
            
            print_test("Root Endpoint", "PASS", f"All {len(agents)} agents registered")
            self.results["passed"] += 1
            return True
            
        except Exception as e:
            print_test("Root Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_tax_master_endpoint(self) -> bool:
        """Test TaxMaster (renamed from KarVid)"""
        try:
            response = requests.post(
                f"{self.base_url}/tax-master/calculate-tax",
                json={"income": 1000000, "regime": "new"},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "tax" in data or "regime" in data:
                    print_test("TaxMaster Endpoint", "PASS")
                    self.results["passed"] += 1
                    return True
                else:
                    print_test("TaxMaster Endpoint", "FAIL", "Response missing expected fields")
                    self.results["failed"] += 1
                    return False
            else:
                print_test("TaxMaster Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("TaxMaster Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_retirement_pro_endpoint(self) -> bool:
        """Test RetirementPro (renamed from YojanaKarta)"""
        try:
            response = requests.post(
                f"{self.base_url}/retirement-pro/fire-number",
                json={"monthly_expenses": 50000},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "fire_number" in data or "monthly_expenses" in data:
                    print_test("RetirementPro Endpoint", "PASS")
                    self.results["passed"] += 1
                    return True
                else:
                    print_test("RetirementPro Endpoint", "FAIL", "Response missing expected fields")
                    self.results["failed"] += 1
                    return False
            else:
                print_test("RetirementPro Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("RetirementPro Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_money_health_endpoint(self) -> bool:
        """Test MoneyHealth (renamed from DhanRaksha)"""
        try:
            response = requests.post(
                f"{self.base_url}/money-health/health-score",
                json={
                    "income": 1200000,
                    "expenses": 800000,
                    "monthly_savings": 40000,
                    "debt": 0,
                    "insurance_coverage": 2500000
                },
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "score" in data or "savings_rate" in data:
                    print_test("MoneyHealth Endpoint", "PASS")
                    self.results["passed"] += 1
                    return True
                else:
                    print_test("MoneyHealth Endpoint", "FAIL", "Response missing expected fields")
                    self.results["failed"] += 1
                    return False
            else:
                print_test("MoneyHealth Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("MoneyHealth Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_stock_insight_endpoint(self) -> bool:
        """Test StockInsight (renamed from BazaarGuru)"""
        try:
            response = requests.post(
                f"{self.base_url}/stock-insight/stock-quote",
                json={"symbol": "TCS"},
                timeout=TIMEOUT
            )
            
            # Either 200 or 404 is acceptable (symbol might not exist in stub)
            if response.status_code in [200, 404]:
                print_test("StockInsight Endpoint", "PASS", f"Status {response.status_code}")
                self.results["passed"] += 1
                return True
            else:
                print_test("StockInsight Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("StockInsight Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_portfolio_wise_endpoint(self) -> bool:
        """Test PortfolioWise (renamed from Niveshak)"""
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
                data = response.json()
                if "xirr_percent" in data:
                    print_test("PortfolioWise Endpoint", "PASS")
                    self.results["passed"] += 1
                    return True
                else:
                    print_test("PortfolioWise Endpoint", "FAIL", "Response missing xirr_percent")
                    self.results["failed"] += 1
                    return False
            else:
                print_test("PortfolioWise Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("PortfolioWise Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_compliance_helper_endpoint(self) -> bool:
        """Test ComplianceHelper (renamed from Vidhi)"""
        try:
            response = requests.get(
                f"{self.base_url}/compliance-helper/disclaimers",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                print_test("ComplianceHelper Endpoint", "PASS")
                self.results["passed"] += 1
                return True
            else:
                print_test("ComplianceHelper Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("ComplianceHelper Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_life_goals_endpoint(self) -> bool:
        """Test LifeGoals (renamed from LifeEvent)"""
        try:
            response = requests.get(
                f"{self.base_url}/life-goals/types",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                print_test("LifeGoals Endpoint", "PASS")
                self.results["passed"] += 1
                return True
            else:
                print_test("LifeGoals Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("LifeGoals Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def test_partner_finance_endpoint(self) -> bool:
        """Test PartnerFinance (renamed from CouplePlanner)"""
        try:
            response = requests.post(
                f"{self.base_url}/partner-finance/finances",
                json={
                    "partner1_income": 1000000,
                    "partner2_income": 800000,
                    "combined_expenses": 800000
                },
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                print_test("PartnerFinance Endpoint", "PASS")
                self.results["passed"] += 1
                return True
            else:
                print_test("PartnerFinance Endpoint", "FAIL", f"Status {response.status_code}")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            print_test("PartnerFinance Endpoint", "FAIL", str(e))
            self.results["failed"] += 1
            return False
    
    def print_summary(self):
        """Print test summary"""
        total = self.results["passed"] + self.results["failed"] + self.results["skipped"]
        
        print(f"\n{'='*60}")
        print(f"Test Results: {total} total")
        print(f"{GREEN}✓ Passed: {self.results['passed']}{RESET}")
        print(f"{RED}✗ Failed: {self.results['failed']}{RESET}")
        if self.results["skipped"] > 0:
            print(f"{YELLOW}⚠ Skipped: {self.results['skipped']}{RESET}")
        print(f"{'='*60}")
        
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        return self.results["failed"] == 0

def main():
    print(f"\n{'='*60}")
    print("AI Money Mentor - Backend Integration Test Suite")
    print(f"Testing new agent names (cross-platform compatible)")
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
    
    # Run tests
    print(f"{YELLOW}Running endpoint tests...{RESET}\n")
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
    
    # Print summary
    success = tester.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
