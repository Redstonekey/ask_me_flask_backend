# AskMe API Quick Reference

## 🔗 Base URL
**Development:** `http://localhost:5000`

## 🔐 Authentication
Include in headers: `Authorization: Bearer <token>`

## 📋 Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | ❌ | Register user |
| POST | `/auth/login` | ❌ | Login user |
| POST | `/auth/google` | ❌ | Google OAuth login |
| POST | `/auth/callback` | ❌ | OAuth callback |
| POST | `/auth/refresh` | ❌ | Refresh token |
| POST | `/auth/logout` | ✅ | Logout user |

### Users
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/user/<username>` | ❌ | Get public profile |
| GET | `/user/<username>/questions` | ✅ | Get user's questions |

### Questions
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/questions` | ❌ | Submit question |
| POST | `/questions/<id>/answer` | ✅ | Answer question |
| DELETE | `/questions/<id>` | ✅ | Delete question |

### Dashboard
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/dashboard` | ✅ | Get user dashboard |

## 📝 Request Examples

### Signup
```json
POST /auth/signup
{
  "email": "user@example.com",
  "password": "password123",
  "username": "myusername"
}
```

### Login
```json
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Submit Question
```json
POST /questions
{
  "receiver": "targetuser",
  "question": "What's your favorite color?"
}
```

### Answer Question
```json
POST /questions/1/answer
{
  "answer": "My favorite color is blue!"
}
```

### Google OAuth Login
```json
POST /auth/google
{
  "id_token": "google-id-token-here"
}
```

### Token Refresh
```json
POST /auth/refresh
{
  "refresh_token": "refresh-token-here"
}
```

## 🚨 Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **409** - Conflict
- **500** - Server Error

## 🔄 App Flow

1. **Landing** → No auth, show features
2. **Login/Signup** → Get token, redirect to dashboard
3. **Dashboard** → Show questions, stats, profile link
4. **Profile** → Public view, submit questions
5. **Questions** → Private view, answer/delete
