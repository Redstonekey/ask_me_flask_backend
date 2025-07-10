import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test if Supabase connection is working"""
    try:
        url = os.getenv("PUBLIC_SUPABASE_URL")
        key = os.getenv("PUBLIC_SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Environment variables not found!")
            print(f"URL: {url}")
            print(f"Key: {key}")
            return False
        
        print(f"✅ Environment variables loaded")
        print(f"URL: {url}")
        print(f"Key: {key[:20]}...")
        
        # Create Supabase client
        supabase = create_client(url, key)
        print("✅ Supabase client created successfully")
        
        # Test a simple query
        result = supabase.table('profiles').select('*').limit(1).execute()
        print(f"✅ Database connection successful")
        print(f"Profiles table exists: {result is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False

def test_auth_signup():
    """Test Supabase auth signup directly"""
    try:
        url = os.getenv("PUBLIC_SUPABASE_URL")
        key = os.getenv("PUBLIC_SUPABASE_ANON_KEY")
        supabase = create_client(url, key)
        
        # Try to sign up
        response = supabase.auth.sign_up({
            'email': 'bennet-wegener@web.de',
            'password': 'testpassword123'
        })
        
        print(f"✅ Direct signup test successful")
        print(f"User created: {response.user is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct signup test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Supabase Connection...\n")
    
    if test_supabase_connection():
        print("\n🔧 Testing Direct Auth Signup...\n")
        test_auth_signup()
    else:
        print("\n❌ Fix Supabase connection before proceeding")
