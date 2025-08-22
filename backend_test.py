import requests
import sys
import json
from datetime import datetime
import time

class ZKAuthAPITester:
    def __init__(self, base_url="https://privacyauth.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_username = f"testuser{int(time.time())}"
        self.test_password = "password123"

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Status: {data.get('status', 'unknown')}, DB: {data.get('database_connected', False)}, Blockchain: {data.get('blockchain_connected', False)}"
            else:
                details = f"- Status Code: {response.status_code}"
                
            return self.log_test("Health Check", success, details)
        except Exception as e:
            return self.log_test("Health Check", False, f"- Error: {str(e)}")

    def test_api_root(self):
        """Test /api/ root endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Version: {data.get('version', 'unknown')}"
            else:
                details = f"- Status Code: {response.status_code}"
                
            return self.log_test("API Root", success, details)
        except Exception as e:
            return self.log_test("API Root", False, f"- Error: {str(e)}")

    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            payload = {
                "username": self.test_username,
                "password": self.test_password
            }
            
            response = requests.post(
                f"{self.api_url}/auth/register", 
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.user_data = data
                did = data.get('did', 'unknown')
                address = data.get('address', 'unknown')
                details = f"- DID: {did[:20]}..., Address: {address[:10]}..."
            else:
                try:
                    error_data = response.json()
                    details = f"- Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"- Status: {response.status_code}, Raw response: {response.text[:100]}"
                
            return self.log_test("User Registration", success, details)
        except Exception as e:
            return self.log_test("User Registration", False, f"- Error: {str(e)}")

    def test_duplicate_registration(self):
        """Test duplicate username registration (should fail)"""
        try:
            payload = {
                "username": self.test_username,
                "password": self.test_password
            }
            
            response = requests.post(
                f"{self.api_url}/auth/register", 
                json=payload,
                timeout=10
            )
            
            # Should fail with 400 status code
            success = response.status_code == 400
            
            if success:
                error_data = response.json()
                details = f"- Correctly rejected: {error_data.get('detail', 'Username already exists')}"
            else:
                details = f"- Unexpected status: {response.status_code}"
                
            return self.log_test("Duplicate Registration Prevention", success, details)
        except Exception as e:
            return self.log_test("Duplicate Registration Prevention", False, f"- Error: {str(e)}")

    def test_user_login(self):
        """Test user login with ZK proof authentication"""
        try:
            payload = {
                "username": self.test_username,
                "password": self.test_password
            }
            
            response = requests.post(
                f"{self.api_url}/auth/login", 
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.token = data.get('access_token')
                user_info = data.get('user_info', {})
                details = f"- Token received, User: {user_info.get('username', 'unknown')}, DID: {user_info.get('did', 'unknown')[:20]}..."
            else:
                try:
                    error_data = response.json()
                    details = f"- Status: {response.status_code}, Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details = f"- Status: {response.status_code}"
                
            return self.log_test("User Login (ZK Auth)", success, details)
        except Exception as e:
            return self.log_test("User Login (ZK Auth)", False, f"- Error: {str(e)}")

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            payload = {
                "username": self.test_username,
                "password": "wrongpassword"
            }
            
            response = requests.post(
                f"{self.api_url}/auth/login", 
                json=payload,
                timeout=10
            )
            
            # Should fail with 401 status code
            success = response.status_code == 401
            
            if success:
                details = "- Correctly rejected invalid credentials"
            else:
                details = f"- Unexpected status: {response.status_code}"
                
            return self.log_test("Invalid Login Prevention", success, details)
        except Exception as e:
            return self.log_test("Invalid Login Prevention", False, f"- Error: {str(e)}")

    def test_get_current_user(self):
        """Test /api/auth/me endpoint with JWT token"""
        if not self.token:
            return self.log_test("Get Current User", False, "- No token available")
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_url}/auth/me", headers=headers, timeout=10)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Username: {data.get('username', 'unknown')}, Login count: {data.get('login_count', 0)}"
            else:
                details = f"- Status: {response.status_code}"
                
            return self.log_test("Get Current User", success, details)
        except Exception as e:
            return self.log_test("Get Current User", False, f"- Error: {str(e)}")

    def test_dashboard_stats(self):
        """Test /api/dashboard/stats endpoint"""
        if not self.token:
            return self.log_test("Dashboard Stats", False, "- No token available")
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_url}/dashboard/stats", headers=headers, timeout=10)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Total users: {data.get('total_users', 0)}, Activities: {data.get('total_activities', 0)}, Recent activities: {len(data.get('recent_activities', []))}"
            else:
                details = f"- Status: {response.status_code}"
                
            return self.log_test("Dashboard Stats", success, details)
        except Exception as e:
            return self.log_test("Dashboard Stats", False, f"- Error: {str(e)}")

    def test_user_activities(self):
        """Test /api/user/activities endpoint"""
        if not self.token:
            return self.log_test("User Activities", False, "- No token available")
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_url}/user/activities", headers=headers, timeout=10)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                activities_count = len(data) if isinstance(data, list) else 0
                details = f"- Activities found: {activities_count}"
                if activities_count > 0:
                    latest_activity = data[0] if data else {}
                    details += f", Latest: {latest_activity.get('activity_type', 'unknown')}"
            else:
                details = f"- Status: {response.status_code}"
                
            return self.log_test("User Activities", success, details)
        except Exception as e:
            return self.log_test("User Activities", False, f"- Error: {str(e)}")

    def test_unauthorized_access(self):
        """Test accessing protected endpoints without token"""
        try:
            response = requests.get(f"{self.api_url}/dashboard/stats", timeout=10)
            
            # Should fail with 403 or 401 status code
            success = response.status_code in [401, 403]
            
            if success:
                details = f"- Correctly rejected unauthorized access (Status: {response.status_code})"
            else:
                details = f"- Unexpected status: {response.status_code}"
                
            return self.log_test("Unauthorized Access Prevention", success, details)
        except Exception as e:
            return self.log_test("Unauthorized Access Prevention", False, f"- Error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting Decentralized Identity & ZK Authentication API Tests")
        print(f"📡 Testing against: {self.base_url}")
        print("=" * 70)
        
        # Basic connectivity tests
        self.test_api_root()
        self.test_health_endpoint()
        
        # Authentication flow tests
        self.test_user_registration()
        self.test_duplicate_registration()
        self.test_user_login()
        self.test_invalid_login()
        
        # Protected endpoint tests
        self.test_get_current_user()
        self.test_dashboard_stats()
        self.test_user_activities()
        
        # Security tests
        self.test_unauthorized_access()
        
        # Print summary
        print("=" * 70)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Backend API is working correctly.")
            return 0
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"⚠️  {failed_tests} test(s) failed. Please check the issues above.")
            return 1

def main():
    """Main test execution"""
    tester = ZKAuthAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())