from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime
import json
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
url: str = os.getenv("PUBLIC_SUPABASE_URL")
key: str = os.getenv("PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# Auth decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
            # Verify token with Supabase
            user = supabase.auth.get_user(token)
            if not user:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Add user to request context
            request.current_user = user.user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
    
    return decorated_function

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'AskMe API is running'}), 200

# Auth endpoints
@app.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not email or not password or not username:
            return jsonify({'error': 'Email, password, and username are required'}), 400
        
        # Check if username already exists
        existing_user = supabase.table('profiles').select('*').eq('username', username).execute()
        if existing_user.data:
            return jsonify({'error': 'Username already exists'}), 409
        
        # Sign up with Supabase Auth
        response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if response.user:
            # Create profile in profiles table using admin client
            profile_data = {
                'id': response.user.id,
                'username': username,
                'email': email,
                'created_at': datetime.now().isoformat()
            }
            
            try:
                # Create profile in profiles table
                supabase.table('profiles').insert(profile_data).execute()
            except Exception as profile_error:
                # If profile creation fails, we should clean up the auth user
                print(f"Profile creation failed: {profile_error}")
                return jsonify({'error': f'Profile creation failed: {str(profile_error)}'}), 500
            
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': username
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create user', 'details': 'No user returned from Supabase'}), 400
            
    except Exception as e:
        # More detailed error handling
        error_msg = str(e)
        if 'Invalid email' in error_msg or 'email' in error_msg.lower():
            return jsonify({'error': f'Email validation failed: {error_msg}'}), 400
        elif 'Password' in error_msg or 'password' in error_msg.lower():
            return jsonify({'error': f'Password validation failed: {error_msg}'}), 400
        else:
            return jsonify({'error': f'Signup failed: {error_msg}'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Sign in with Supabase Auth
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user and response.session:
            # Get user profile
            profile = supabase.table('profiles').select('*').eq('id', response.user.id).execute()
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': profile.data[0]['username'] if profile.data else None
                },
                'session': {
                    'access_token': response.session.access_token,
                    'refresh_token': response.session.refresh_token
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/google', methods=['POST'])
def google_auth():
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            return jsonify({'error': 'Google ID token is required'}), 400
        
        # Sign in with Google using Supabase
        response = supabase.auth.sign_in_with_id_token({
            'provider': 'google',
            'token': id_token
        })
        
        if response.user and response.session:
            # Check if profile exists, if not create it
            profile = supabase.table('profiles').select('*').eq('id', response.user.id).execute()
            
            if not profile.data:
                # Extract username from email (fallback) or use display name
                email = response.user.email
                username = email.split('@')[0] if email else f"user_{response.user.id[:8]}"
                
                # Check if username exists and make it unique if needed
                existing_username = supabase.table('profiles').select('*').eq('username', username).execute()
                if existing_username.data:
                    username = f"{username}_{response.user.id[:8]}"
                
                # Create profile
                profile_data = {
                    'id': response.user.id,
                    'username': username,
                    'email': response.user.email,
                    'created_at': datetime.now().isoformat()
                }
                
                try:
                    supabase.table('profiles').insert(profile_data).execute()
                    created_profile = profile_data
                except Exception as profile_error:
                    print(f"Profile creation failed: {profile_error}")
                    return jsonify({'error': f'Profile creation failed: {str(profile_error)}'}), 500
            else:
                created_profile = profile.data[0]
            
            return jsonify({
                'message': 'Google authentication successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': created_profile['username']
                },
                'session': {
                    'access_token': response.session.access_token,
                    'refresh_token': response.session.refresh_token
                }
            }), 200
        else:
            return jsonify({'error': 'Google authentication failed'}), 401
            
    except Exception as e:
        print(f"Google auth error: {e}")
        return jsonify({'error': f'Google authentication failed: {str(e)}'}), 500

# OAuth callback endpoint
@app.route('/auth/callback', methods=['POST'])
def oauth_callback():
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': 'OAuth code is required'}), 400
        
        # Exchange code for session using Supabase
        response = supabase.auth.exchange_code_for_session(code)
        
        if response.user and response.session:
            # Check if profile exists, if not create it
            profile = supabase.table('profiles').select('*').eq('id', response.user.id).execute()
            
            if not profile.data:
                # Extract username from email or user metadata
                email = response.user.email
                user_metadata = response.user.user_metadata or {}
                
                # Try to get username from metadata or email
                username = user_metadata.get('preferred_username') or user_metadata.get('name') or email.split('@')[0] if email else f"user_{response.user.id[:8]}"
                
                # Clean username (remove spaces, special chars)
                username = ''.join(c for c in username if c.isalnum() or c in '_-').lower()
                
                # Check if username exists and make it unique if needed
                existing_username = supabase.table('profiles').select('*').eq('username', username).execute()
                if existing_username.data:
                    username = f"{username}_{response.user.id[:8]}"
                
                # Create profile
                profile_data = {
                    'id': response.user.id,
                    'username': username,
                    'email': response.user.email,
                    'created_at': datetime.now().isoformat()
                }
                
                try:
                    supabase.table('profiles').insert(profile_data).execute()
                    created_profile = profile_data
                except Exception as profile_error:
                    print(f"Profile creation failed: {profile_error}")
                    return jsonify({'error': f'Profile creation failed: {str(profile_error)}'}), 500
            else:
                created_profile = profile.data[0]
            
            return jsonify({
                'message': 'OAuth authentication successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': created_profile['username']
                },
                'session': {
                    'access_token': response.session.access_token,
                    'refresh_token': response.session.refresh_token
                }
            }), 200
        else:
            return jsonify({'error': 'OAuth authentication failed'}), 401
            
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return jsonify({'error': f'OAuth authentication failed: {str(e)}'}), 500

# User profile endpoints
@app.route('/user/<username>', methods=['GET'])
def get_user_profile(username):
    try:
        # Get user profile
        profile = supabase.table('profiles').select('*').eq('username', username).execute()
        
        if not profile.data:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = profile.data[0]
        
        # Get answered questions for this user
        answered_questions = supabase.table('questions').select('*').eq('receiver', username).eq('answered', True).order('answered_at', desc=True).execute()
        
        return jsonify({
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'created_at': user_data['created_at']
            },
            'answered_questions': answered_questions.data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<username>/questions', methods=['GET'])
@require_auth
def get_user_questions(username):
    try:
        # Verify user can only access their own questions
        current_user_profile = supabase.table('profiles').select('*').eq('id', request.current_user.id).execute()
        if not current_user_profile.data or current_user_profile.data[0]['username'] != username:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all questions for this user
        questions = supabase.table('questions').select('*').eq('receiver', username).order('created_at', desc=True).execute()
        
        unanswered = [q for q in questions.data if not q['answered']]
        answered = [q for q in questions.data if q['answered']]
        
        return jsonify({
            'unanswered_questions': unanswered,
            'answered_questions': answered
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Question endpoints
@app.route('/questions', methods=['POST'])
def submit_question():
    try:
        data = request.get_json()
        receiver = data.get('receiver')
        question = data.get('question')
        
        if not receiver or not question:
            return jsonify({'error': 'Receiver and question are required'}), 400
        
        # Verify receiver exists
        profile = supabase.table('profiles').select('*').eq('username', receiver).execute()
        if not profile.data:
            return jsonify({'error': 'User not found'}), 404
        
        # Insert question
        question_data = {
            'receiver': receiver,
            'question': question,
            'answered': False,
            'created_at': datetime.now().isoformat()
        }
        
        result = supabase.table('questions').insert(question_data).execute()
        
        return jsonify({
            'message': 'Question submitted successfully',
            'question': result.data[0]
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/questions/<int:question_id>/answer', methods=['POST'])
@require_auth
def answer_question(question_id):
    try:
        data = request.get_json()
        answer = data.get('answer')
        
        if not answer:
            return jsonify({'error': 'Answer is required'}), 400
        
        # Get the question
        question = supabase.table('questions').select('*').eq('id', question_id).execute()
        if not question.data:
            return jsonify({'error': 'Question not found'}), 404
        
        # Verify user can answer this question
        current_user_profile = supabase.table('profiles').select('*').eq('id', request.current_user.id).execute()
        if not current_user_profile.data or current_user_profile.data[0]['username'] != question.data[0]['receiver']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update question with answer
        update_data = {
            'answer': answer,
            'answered': True,
            'answered_at': datetime.now().isoformat()
        }
        
        result = supabase.table('questions').update(update_data).eq('id', question_id).execute()
        
        return jsonify({
            'message': 'Question answered successfully',
            'question': result.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
@require_auth
def delete_question(question_id):
    try:
        # Get the question
        question = supabase.table('questions').select('*').eq('id', question_id).execute()
        if not question.data:
            return jsonify({'error': 'Question not found'}), 404
        
        # Verify user can delete this question
        current_user_profile = supabase.table('profiles').select('*').eq('id', request.current_user.id).execute()
        if not current_user_profile.data or current_user_profile.data[0]['username'] != question.data[0]['receiver']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete question
        supabase.table('questions').delete().eq('id', question_id).execute()
        
        return jsonify({'message': 'Question deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard endpoint
@app.route('/dashboard', methods=['GET'])
@require_auth
def get_dashboard():
    try:
        # Get current user profile
        profile = supabase.table('profiles').select('*').eq('id', request.current_user.id).execute()
        if not profile.data:
            return jsonify({'error': 'User profile not found'}), 404
        
        username = profile.data[0]['username']
        
        # Get recent unanswered questions
        unanswered = supabase.table('questions').select('*').eq('receiver', username).eq('answered', False).order('created_at', desc=True).limit(10).execute()
        
        # Get recent answered questions
        answered = supabase.table('questions').select('*').eq('receiver', username).eq('answered', True).order('answered_at', desc=True).limit(10).execute()
        
        return jsonify({
            'user': {
                'username': username,
                'profile_url': f'/user/{username}'
            },
            'unanswered_questions': unanswered.data,
            'recent_answers': answered.data,
            'stats': {
                'total_questions': len(unanswered.data) + len(answered.data),
                'unanswered_count': len(unanswered.data),
                'answered_count': len(answered.data)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Refresh the session using Supabase
        response = supabase.auth.refresh_session(refresh_token)
        
        if response.session:
            return jsonify({
                'message': 'Token refreshed successfully',
                'session': {
                    'access_token': response.session.access_token,
                    'refresh_token': response.session.refresh_token
                }
            }), 200
        else:
            return jsonify({'error': 'Token refresh failed'}), 401
            
    except Exception as e:
        print(f"Token refresh error: {e}")
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)