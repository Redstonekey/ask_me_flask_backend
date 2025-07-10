# AskMe Flask Backend

A Flask backend API for the AskMe anonymous question app, integrated with Supabase for authentication and database operations.

## Features

- **Supabase Authentication**: User signup, login, and session management
- **Anonymous Questions**: Submit questions to any user profile
- **Question Management**: Answer, delete, and organize questions
- **Public Profiles**: View user profiles and answered questions
- **Dashboard**: Personal dashboard for managing questions
- **Row Level Security**: Database security implemented with Supabase RLS

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Make sure your `.env` file contains:
```
PUBLIC_SUPABASE_URL=your_supabase_url
PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Database Setup

1. Go to your Supabase dashboard
2. Navigate to the SQL editor
3. Run the SQL commands in `setup_database.sql`

This will create:
- `profiles` table for user profiles
- `questions` table for questions and answers
- Row Level Security policies
- Necessary indexes for performance

### 4. Run the Application

```bash
python api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user (requires auth)

### User Profiles
- `GET /user/<username>` - Get public profile and answered questions
- `GET /user/<username>/questions` - Get all questions for user (requires auth)

### Questions
- `POST /questions` - Submit a new question
- `POST /questions/<id>/answer` - Answer a question (requires auth)
- `DELETE /questions/<id>` - Delete a question (requires auth)

### Dashboard
- `GET /dashboard` - Get user dashboard with stats (requires auth)

### Health Check
- `GET /health` - API health check

## Authentication

The API uses Supabase Auth with JWT tokens. Include the token in requests:

```
Authorization: Bearer <your_jwt_token>
```

## CORS

CORS is enabled for all origins during development. Configure appropriately for production.

## Database Schema

### profiles
- `id` (UUID) - Links to auth.users
- `username` (TEXT) - Unique username
- `email` (TEXT) - User email
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### questions
- `id` (BIGINT) - Primary key
- `created_at` (TIMESTAMP) - When question was asked
- `sender` (TEXT) - Anonymous sender identifier (optional)
- `receiver` (TEXT) - Username of person receiving question
- `answered` (BOOLEAN) - Whether question has been answered
- `question` (TEXT) - The question content
- `answer` (TEXT) - The answer content
- `answered_at` (TIMESTAMP) - When question was answered

## Security

- Row Level Security (RLS) is enabled on all tables
- Users can only manage their own questions
- Public profiles and answered questions are viewable by everyone
- Anonymous question submission is allowed

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error
