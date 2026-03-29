#!/usr/bin/env python3
"""
Integration Test Suite for AI Money Mentor
Tests backend API endpoints with new agent names
Verifies frontend-backend integration
"""

import requests
import json
import sys
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
TIMEOUT = 10

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class IntegrationTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        
    def print_header(self, text):
        print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{BLUE}{BOLD}{text}{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")
    
    def print_test(self, name, status, details=""):
        symbol = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
        print(f"{symbol} {name}")
        if details:
            print(f"  {YELLOW}{details}{RESET}")
        if status:
            self.passed += 1
        else:
            self.failed += 1
        self.tests.append((name, status))
    
    def test_backend_health(self):
        """Test backend is running and healthy"""
        self.print_header("Backend Health Check")
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=TIMEOUT)
            self.print_test("Backend Health Check", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("Backend Health Check", False, str(e))
            return False
    
    def test_backend_root(self):
        """Test backend root endpoint lists all agents"""
        self.print_header("Backend Agent Registration")
        
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=TIMEOUT)
            if response.status_code != 200:
                self.print_test("Root Endpoint", False, f"Status: {response.status_code}")
                return False
            
            data = response.json()
            agents = data.get("agents", [])
            
            expected_agents = [
                "portfolio-wise",
                "tax-master",
                "retirement-pro",
                "stock-insight",
                "money-health",
                "compliance-helper",
                "coordinator",
                "life-goals",
                "partner-finance"
            ]
            
            all_found = all(agent in agents for agent in expected_agents)
            self.print_test("Root Endpoint", all_found, f"Found {len(agents)} agents")
            
            if all_found:
                for agent in expected_agents:
                    print(f"  {GREEN}✓{RESET} {agent}")
            
            return all_found
        except Exception as e:
            self.print_test("Root Endpoint", False, str(e))
            return False
    
    def test_agent_endpoints(self):
        """Test all agent endpoints"""
        self.print_header("Agent Endpoint Tests")
        
        tests = [
            ("TaxMaster", "POST", "/tax-master/calculate-tax", {"income": 1000000, "regime": "new"}),
            ("RetirementPro", "POST", "/retirement-pro/fire-number", {"monthly_expenses": 50000}),
            ("MoneyHealth", "POST", "/money-health/health-score", {"income": 1000000, "expenses": 500000}),
            ("PortfolioWise", "POST", "/portfolio-wise/xirr", {"transactions": [{"date": "2024-01-01", "amount": -100000}, {"date": "2026-03-29", "amount": 100000}]}),
            ("StockInsight", "POST", "/stock-insight/stock-quote", {"symbol": "RELIANCE"}),
            ("ComplianceHelper", "GET", "/compliance-helper/disclaimers", {}),
            ("LifeGoals", "POST", "/life-goals/plan", {"event_type": "marriage", "target_year": 2027}),
            ("PartnerFinance", "POST", "/partner-finance/finances", {"p1_income": 1000000, "p2_income": 800000}),
        ]
        
        for agent_name, method, endpoint, data in tests:
            try:
                url = f"{BACKEND_URL}{endpoint}"
                if method == "POST":
                    response = requests.post(url, json=data, timeout=TIMEOUT)
                else:
                    response = requests.get(url, timeout=TIMEOUT)
                
                status = response.status_code in [200, 201, 400, 422]  # Accept errors from API too
                details = f"Status: {response.status_code}"
                self.print_test(f"{agent_name:20} {endpoint:35}", status, details)
            except Exception as e:
                self.print_test(f"{agent_name:20} {endpoint:35}", False, str(e)[:50])
    
    def test_frontend_auth_signup(self):
        """Test frontend auth signup endpoint"""
        self.print_header("Frontend Auth Integration")
        
        try:
            response = requests.post(
                f"{FRONTEND_URL}/api/auth/signup",
                json={
                    "email": f"testuser_{int(time.time())}@example.com",
                    "name": "Test User",
                    "phone": "+919876543210"
                },
                timeout=TIMEOUT
            )
            
            status = response.status_code in [201, 409]  # 201 created, 409 already exists
            details = f"Status: {response.status_code}"
            self.print_test("Frontend Signup Endpoint", status, details)
            
            if response.status_code == 201:
                data = response.json()
                has_auth_token = "authToken" in str(data)
                self.print_test("Auth Token Generated", has_auth_token)
                return has_auth_token
            return status
        except Exception as e:
            self.print_test("Frontend Signup Endpoint", False, str(e))
            return False
    
    def test_frontend_auth_login(self):
        """Test frontend auth login endpoint"""
        try:
            response = requests.post(
                f"{FRONTEND_URL}/api/auth/login",
                json={"email": "test@example.com"},
                timeout=TIMEOUT
            )
            
            status = response.status_code in [200, 404]  # 200 found, 404 not found
            details = f"Status: {response.status_code}"
            self.print_test("Frontend Login Endpoint", status, details)
            return status
        except Exception as e:
            self.print_test("Frontend Login Endpoint", False, str(e))
            return False
    
    def test_frontend_pages(self):
        """Test frontend agent pages are accessible"""
        self.print_header("Frontend Pages Accessibility")
        
        pages = [
            "coordinator",
            "money-health",
            "tax-master",
            "retirement-pro",
            "stock-insight",
            "compliance-helper",
            "life-goals",
            "partner-finance",
            "portfolio-wise",
        ]
        
        for page in pages:
            try:
                response = requests.get(
                    f"{FRONTEND_URL}/agents/{page}",
                    timeout=TIMEOUT,
                    allow_redirects=False
                )
                status = response.status_code == 200
                details = f"Status: {response.status_code}"
                self.print_test(f"Agent Page: {page:20}", status, details)
            except Exception as e:
                self.print_test(f"Agent Page: {page:20}", False, "Connection failed")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print(f"\n{BOLD}🚀 AI Money Mentor - Integration Test Suite{RESET}")
        print(f"{BOLD}Testing Frontend-Backend Integration{RESET}\n")
        
        # Check if servers are running
        print("Checking servers...")
        backend_ok = False
        frontend_ok = False
        
        try:
            requests.get(f"{BACKEND_URL}/health", timeout=5)
            backend_ok = True
            print(f"{GREEN}✓ Backend is running on {BACKEND_URL}{RESET}")
        except:
            print(f"{RED}✗ Backend not running on {BACKEND_URL}{RESET}")
            print(f"{YELLOW}Start with: cd backend && uv run uvicorn api_server:app --reload{RESET}")
        
        try:
            requests.get(f"{FRONTEND_URL}/", timeout=5)
            frontend_ok = True
            print(f"{GREEN}✓ Frontend is running on {FRONTEND_URL}{RESET}")
        except:
            print(f"{RED}✗ Frontend not running on {FRONTEND_URL}{RESET}")
            print(f"{YELLOW}Start with: cd frontend && bun run dev{RESET}")
        
        if not backend_ok:
            print(f"\n{RED}Backend is required for testing!{RESET}")
            return
        
        # Run tests
        self.test_backend_health()
        self.test_backend_root()
        self.test_agent_endpoints()
        
        if frontend_ok:
            self.test_frontend_auth_signup()
            self.test_frontend_auth_login()
            self.test_frontend_pages()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}Test Summary{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{GREEN}✓ Passed: {self.passed}{RESET}")
        print(f"{RED}✗ Failed: {self.failed}{RESET}")
        print(f"{BOLD}Total: {total}{RESET}")
        print(f"{BOLD}Success Rate: {success_rate:.1f}%{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")
        
        if self.failed == 0:
            print(f"{GREEN}{BOLD}✨ All tests passed! Integration is working correctly.{RESET}\n")
        else:
            print(f"{YELLOW}{BOLD}⚠️  Some tests failed. Check the logs above.{RESET}\n")



if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_all_tests()
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
                "coordinator",
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
