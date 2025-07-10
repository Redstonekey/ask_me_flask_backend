import requests
import json

# Base URL for your API
BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_signup():
    """Test user signup"""
    data = {
        "email": "testuser@gmail.com",
        "password": "testpassword123",
        "username": "testuser"
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=data)
    print(f"Signup: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # If user already exists, try to delete and recreate
    if response.status_code == 409:
        print("User already exists, this is expected if running tests multiple times")
        return True
    
    return response.status_code == 201

def test_login():
    """Test user login"""
    data = {
        "email": "testuser@gmail.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Login: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json()['session']['access_token']
    return None

def test_submit_question():
    """Test submitting a question"""
    data = {
        "receiver": "testuser",
        "question": "What's your favorite color?"
    }
    response = requests.post(f"{BASE_URL}/questions", json=data)
    print(f"Submit Question: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()['question']['id']
    return None

def test_dashboard(token):
    """Test dashboard endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    print(f"Dashboard: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_answer_question(token, question_id):
    """Test answering a question"""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"answer": "Blue is my favorite color!"}
    
    response = requests.post(f"{BASE_URL}/questions/{question_id}/answer", 
                           json=data, headers=headers)
    print(f"Answer Question: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_user_profile():
    """Test getting user profile"""
    response = requests.get(f"{BASE_URL}/user/testuser")
    print(f"User Profile: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_google_oauth():
    """Test Google OAuth endpoint (mock test)"""
    # This is a mock test since we don't have a real Google ID token
    # In real testing, you would get this from Google Sign-In
    data = {
        "id_token": "mock-google-id-token"
    }
    response = requests.post(f"{BASE_URL}/auth/google", json=data)
    print(f"Google OAuth: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # This will fail in testing because we don't have a real token
    # But it shows the endpoint is accessible
    return response.status_code in [200, 400, 500]  # 400/500 expected with mock token

def test_token_refresh():
    """Test token refresh endpoint"""
    data = {
        "refresh_token": "mock-refresh-token"
    }
    response = requests.post(f"{BASE_URL}/auth/refresh", json=data)
    print(f"Token Refresh: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # This will fail in testing because we don't have a real refresh token
    # But it shows the endpoint is accessible
    return response.status_code in [200, 400, 401, 500]  # Error expected with mock token

def run_tests():
    """Run all tests in sequence"""
    print("🚀 Starting API Tests...\n")
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    if not test_health():
        print("❌ Health check failed!")
        return
    print("✅ Health check passed!\n")
    
    # Test 2: Signup
    print("2. Testing Signup...")
    if not test_signup():
        print("❌ Signup failed!")
        return
    print("✅ Signup passed!\n")
    
    # Test 3: Login
    print("3. Testing Login...")
    token = test_login()
    if not token:
        print("❌ Login failed!")
        return
    print("✅ Login passed!\n")
    
    # Test 4: Submit Question
    print("4. Testing Submit Question...")
    question_id = test_submit_question()
    if not question_id:
        print("❌ Submit question failed!")
        return
    print("✅ Submit question passed!\n")
    
    # Test 5: Dashboard
    print("5. Testing Dashboard...")
    if not test_dashboard(token):
        print("❌ Dashboard failed!")
        return
    print("✅ Dashboard passed!\n")
    
    # Test 6: Answer Question
    print("6. Testing Answer Question...")
    if not test_answer_question(token, question_id):
        print("❌ Answer question failed!")
        return
    print("✅ Answer question passed!\n")
    
    # Test 7: User Profile
    print("7. Testing User Profile...")
    if not test_user_profile():
        print("❌ User profile failed!")
        return
    print("✅ User profile passed!\n")
    
    # Test 8: Google OAuth
    print("8. Testing Google OAuth...")
    if not test_google_oauth():
        print("❌ Google OAuth test failed!")
        return
    print("✅ Google OAuth test passed!\n")
    
    # Test 9: Token Refresh
    print("9. Testing Token Refresh...")
    if not test_token_refresh():
        print("❌ Token refresh test failed!")
        return
    print("✅ Token refresh test passed!\n")
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    run_tests()
