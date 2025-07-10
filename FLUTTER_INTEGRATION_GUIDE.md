# AskMe Flutter Integration Guide

## 🚀 Backend API Documentation

**Base URL:** `http://localhost:5000` (development)  
**Production URL:** `[Your deployed backend URL]`

## 📋 API Endpoints Overview

### Authentication Endpoints
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `POST /auth/google` - Login with Google
- `POST /auth/refresh` - Refresh access token

### User Profile Endpoints
- `GET /user/<username>` - Get public profile + answered questions
- `GET /user/<username>/questions` - Get all questions for user (auth required)

### Question Endpoints
- `POST /questions` - Submit anonymous question
- `POST /questions/<id>/answer` - Answer question (auth required)
- `DELETE /questions/<id>` - Delete question (auth required)

### Dashboard Endpoint
- `GET /dashboard` - Get user dashboard (auth required)

### Utility
- `GET /health` - API health check

---

## 🔐 Authentication Flow

### 1. User Registration
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "username": "myusername"
}
```

**Success Response (201):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "myusername"
  }
}
```

**Error Response (400/409):**
```json
{
  "error": "Username already exists"
}
```

### 2. User Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "myusername"
  },
  "session": {
    "access_token": "jwt-token-here",
    "refresh_token": "refresh-token-here"
  }
}
```

### 3. Google OAuth Login
```http
POST /auth/google
Content-Type: application/json

{
  "id_token": "google-id-token-here"
}
```

**Success Response (200):**
```json
{
  "message": "Google authentication successful",
  "user": {
    "id": "uuid-here",
    "email": "user@gmail.com",
    "username": "generated-username"
  },
  "session": {
    "access_token": "jwt-token-here",
    "refresh_token": "refresh-token-here"
  }
}
```

### 4. Authenticated Requests
Include the JWT token in all authenticated requests:
```http
Authorization: Bearer <access_token>
```

---

## 👤 User Profile Operations

### Get Public Profile
```http
GET /user/{username}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid-here",
    "username": "myusername",
    "created_at": "2025-01-01T00:00:00Z"
  },
  "answered_questions": [
    {
      "id": 1,
      "question": "What's your favorite color?",
      "answer": "Blue!",
      "created_at": "2025-01-01T00:00:00Z",
      "answered_at": "2025-01-01T01:00:00Z",
      "answered": true,
      "receiver": "myusername"
    }
  ]
}
```

### Get User's Questions (Private)
```http
GET /user/{username}/questions
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "unanswered_questions": [
    {
      "id": 2,
      "question": "What's your hobby?",
      "created_at": "2025-01-01T02:00:00Z",
      "answered": false,
      "receiver": "myusername"
    }
  ],
  "answered_questions": [
    {
      "id": 1,
      "question": "What's your favorite color?",
      "answer": "Blue!",
      "created_at": "2025-01-01T00:00:00Z",
      "answered_at": "2025-01-01T01:00:00Z",
      "answered": true,
      "receiver": "myusername"
    }
  ]
}
```

---

## ❓ Question Operations

### Submit Anonymous Question
```http
POST /questions
Content-Type: application/json

{
  "receiver": "targetusername",
  "question": "What's your favorite movie?"
}
```

**Success Response (201):**
```json
{
  "message": "Question submitted successfully",
  "question": {
    "id": 3,
    "receiver": "targetusername",
    "question": "What's your favorite movie?",
    "answered": false,
    "created_at": "2025-01-01T03:00:00Z"
  }
}
```

### Answer Question
```http
POST /questions/{question_id}/answer
Authorization: Bearer <token>
Content-Type: application/json

{
  "answer": "My favorite movie is Inception!"
}
```

**Success Response (200):**
```json
{
  "message": "Question answered successfully",
  "question": {
    "id": 3,
    "receiver": "myusername",
    "question": "What's your favorite movie?",
    "answer": "My favorite movie is Inception!",
    "answered": true,
    "created_at": "2025-01-01T03:00:00Z",
    "answered_at": "2025-01-01T03:30:00Z"
  }
}
```

### Delete Question
```http
DELETE /questions/{question_id}
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "message": "Question deleted successfully"
}
```

---

## 📊 Dashboard

### Get User Dashboard
```http
GET /dashboard
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": {
    "username": "myusername",
    "profile_url": "/user/myusername"
  },
  "unanswered_questions": [
    {
      "id": 4,
      "question": "What's your dream job?",
      "created_at": "2025-01-01T04:00:00Z",
      "answered": false,
      "receiver": "myusername"
    }
  ],
  "recent_answers": [
    {
      "id": 3,
      "question": "What's your favorite movie?",
      "answer": "My favorite movie is Inception!",
      "answered_at": "2025-01-01T03:30:00Z",
      "answered": true,
      "receiver": "myusername"
    }
  ],
  "stats": {
    "total_questions": 5,
    "unanswered_count": 2,
    "answered_count": 3
  }
}
```

---

## 🚨 Error Handling

### HTTP Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request (validation errors)
- **401** - Unauthorized (invalid/missing token)
- **403** - Forbidden (insufficient permissions)
- **404** - Not Found
- **409** - Conflict (duplicate data)
- **500** - Internal Server Error

### Error Response Format
```json
{
  "error": "Error message here",
  "details": "Optional additional details"
}
```

---

## 🛠️ Flutter Implementation Guide

### 1. HTTP Client Setup
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiClient {
  static const String baseUrl = 'http://localhost:5000';
  static String? _token;
  
  static void setToken(String token) {
    _token = token;
  }
  
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    if (_token != null) 'Authorization': 'Bearer $_token',
  };
}
```

### 2. User Authentication
```dart
class AuthService {
  static Future<Map<String, dynamic>> signup(String email, String password, String username) async {
    final response = await http.post(
      Uri.parse('${ApiClient.baseUrl}/auth/signup'),
      headers: ApiClient.headers,
      body: jsonEncode({
        'email': email,
        'password': password,
        'username': username,
      }),
    );
    
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
  
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${ApiClient.baseUrl}/auth/login'),
      headers: ApiClient.headers,
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      ApiClient.setToken(data['session']['access_token']);
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
  
  static Future<Map<String, dynamic>> googleLogin(String idToken) async {
    final response = await http.post(
      Uri.parse('${ApiClient.baseUrl}/auth/google'),
      headers: ApiClient.headers,
      body: jsonEncode({
        'id_token': idToken,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      ApiClient.setToken(data['session']['access_token']);
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
}
```

### 3. Question Operations
```dart
class QuestionService {
  static Future<Map<String, dynamic>> submitQuestion(String receiver, String question) async {
    final response = await http.post(
      Uri.parse('${ApiClient.baseUrl}/questions'),
      headers: ApiClient.headers,
      body: jsonEncode({
        'receiver': receiver,
        'question': question,
      }),
    );
    
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
  
  static Future<Map<String, dynamic>> answerQuestion(int questionId, String answer) async {
    final response = await http.post(
      Uri.parse('${ApiClient.baseUrl}/questions/$questionId/answer'),
      headers: ApiClient.headers,
      body: jsonEncode({
        'answer': answer,
      }),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
}
```

### 4. User Profile
```dart
class UserService {
  static Future<Map<String, dynamic>> getProfile(String username) async {
    final response = await http.get(
      Uri.parse('${ApiClient.baseUrl}/user/$username'),
      headers: ApiClient.headers,
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
  
  static Future<Map<String, dynamic>> getUserQuestions(String username) async {
    final response = await http.get(
      Uri.parse('${ApiClient.baseUrl}/user/$username/questions'),
      headers: ApiClient.headers,
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
}
```

### 5. Dashboard
```dart
class DashboardService {
  static Future<Map<String, dynamic>> getDashboard() async {
    final response = await http.get(
      Uri.parse('${ApiClient.baseUrl}/dashboard'),
      headers: ApiClient.headers,
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception(jsonDecode(response.body)['error']);
    }
  }
}
```

---

## 🔄 App Flow Integration

### Landing Page (`/`)
- **No authentication required**
- Show app features and benefits
- Provide login/signup buttons

### Home Dashboard (`/home`)
- **Authentication required**
- Use `GET /dashboard` to get user's questions and stats
- Show profile sharing link: `https://yourapp.com/user/{username}`

### Login (`/login`)
- Use `POST /auth/login`
- Store token securely (SharedPreferences/Keychain)
- Redirect to `/home` on success

### Signup (`/signup`)
- Use `POST /auth/signup`
- Automatically log in after signup
- Redirect to `/home` on success

### User Profile (`/user/<username>`)
- **Public access** (no auth required)
- Use `GET /user/{username}` to get profile and answered questions
- Show "Login to see answers" for unanswered questions
- Provide question submission form

### User Questions (`/user/<username>/questions`)
- **Authentication required**
- Use `GET /user/{username}/questions` to get all questions
- Only allow access to own questions
- Provide answer/delete options

---

## 🔧 Environment Configuration

### Development
```dart
class Config {
  static const String apiBaseUrl = 'http://localhost:5000';
  static const bool isDevelopment = true;
}
```

### Production
```dart
class Config {
  static const String apiBaseUrl = 'https://your-production-api.com';
  static const bool isDevelopment = false;
}
```

---

## 📱 Required Dependencies

Add these to your `pubspec.yaml`:
```yaml
dependencies:
  http: ^1.1.0
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
```

---

## 🧪 Testing

### Test the backend is running
```dart
static Future<bool> healthCheck() async {
  try {
    final response = await http.get(
      Uri.parse('${ApiClient.baseUrl}/health'),
    );
    return response.statusCode == 200;
  } catch (e) {
    return false;
  }
}
```

---

## 🚀 Ready to Start!

Your Flutter team now has:
- ✅ Complete API documentation
- ✅ Request/response examples
- ✅ Flutter code samples
- ✅ Error handling patterns
- ✅ Authentication flow
- ✅ App integration guide

The backend is ready and waiting for your Flutter app to connect!
