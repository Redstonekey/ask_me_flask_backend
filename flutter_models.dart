// AskMe Flutter Models
// Save this as: lib/models/

// User model
class User {
  final String id;
  final String email;
  final String username;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.username,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      username: json['username'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

// Question model
class Question {
  final int id;
  final String receiver;
  final String question;
  final String? answer;
  final bool answered;
  final DateTime createdAt;
  final DateTime? answeredAt;

  Question({
    required this.id,
    required this.receiver,
    required this.question,
    this.answer,
    required this.answered,
    required this.createdAt,
    this.answeredAt,
  });

  factory Question.fromJson(Map<String, dynamic> json) {
    return Question(
      id: json['id'],
      receiver: json['receiver'],
      question: json['question'],
      answer: json['answer'],
      answered: json['answered'] ?? false,
      createdAt: DateTime.parse(json['created_at']),
      answeredAt: json['answered_at'] != null 
          ? DateTime.parse(json['answered_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'receiver': receiver,
      'question': question,
      'answer': answer,
      'answered': answered,
      'created_at': createdAt.toIso8601String(),
      'answered_at': answeredAt?.toIso8601String(),
    };
  }
}

// Auth response model
class AuthResponse {
  final String message;
  final User user;
  final AuthSession? session;

  AuthResponse({
    required this.message,
    required this.user,
    this.session,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      message: json['message'],
      user: User.fromJson(json['user']),
      session: json['session'] != null 
          ? AuthSession.fromJson(json['session'])
          : null,
    );
  }
}

// Auth session model
class AuthSession {
  final String accessToken;
  final String refreshToken;

  AuthSession({
    required this.accessToken,
    required this.refreshToken,
  });

  factory AuthSession.fromJson(Map<String, dynamic> json) {
    return AuthSession(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
    );
  }
}

// Profile response model
class ProfileResponse {
  final User user;
  final List<Question> answeredQuestions;

  ProfileResponse({
    required this.user,
    required this.answeredQuestions,
  });

  factory ProfileResponse.fromJson(Map<String, dynamic> json) {
    return ProfileResponse(
      user: User.fromJson(json['user']),
      answeredQuestions: (json['answered_questions'] as List)
          .map((q) => Question.fromJson(q))
          .toList(),
    );
  }
}

// Questions response model
class QuestionsResponse {
  final List<Question> unansweredQuestions;
  final List<Question> answeredQuestions;

  QuestionsResponse({
    required this.unansweredQuestions,
    required this.answeredQuestions,
  });

  factory QuestionsResponse.fromJson(Map<String, dynamic> json) {
    return QuestionsResponse(
      unansweredQuestions: (json['unanswered_questions'] as List)
          .map((q) => Question.fromJson(q))
          .toList(),
      answeredQuestions: (json['answered_questions'] as List)
          .map((q) => Question.fromJson(q))
          .toList(),
    );
  }
}

// Dashboard response model
class DashboardResponse {
  final DashboardUser user;
  final List<Question> unansweredQuestions;
  final List<Question> recentAnswers;
  final DashboardStats stats;

  DashboardResponse({
    required this.user,
    required this.unansweredQuestions,
    required this.recentAnswers,
    required this.stats,
  });

  factory DashboardResponse.fromJson(Map<String, dynamic> json) {
    return DashboardResponse(
      user: DashboardUser.fromJson(json['user']),
      unansweredQuestions: (json['unanswered_questions'] as List)
          .map((q) => Question.fromJson(q))
          .toList(),
      recentAnswers: (json['recent_answers'] as List)
          .map((q) => Question.fromJson(q))
          .toList(),
      stats: DashboardStats.fromJson(json['stats']),
    );
  }
}

// Dashboard user model
class DashboardUser {
  final String username;
  final String profileUrl;

  DashboardUser({
    required this.username,
    required this.profileUrl,
  });

  factory DashboardUser.fromJson(Map<String, dynamic> json) {
    return DashboardUser(
      username: json['username'],
      profileUrl: json['profile_url'],
    );
  }
}

// Dashboard stats model
class DashboardStats {
  final int totalQuestions;
  final int unansweredCount;
  final int answeredCount;

  DashboardStats({
    required this.totalQuestions,
    required this.unansweredCount,
    required this.answeredCount,
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      totalQuestions: json['total_questions'],
      unansweredCount: json['unanswered_count'],
      answeredCount: json['answered_count'],
    );
  }
}

// API Error model
class ApiError {
  final String error;
  final String? details;

  ApiError({
    required this.error,
    this.details,
  });

  factory ApiError.fromJson(Map<String, dynamic> json) {
    return ApiError(
      error: json['error'],
      details: json['details'],
    );
  }
}

// Question submission model
class QuestionSubmission {
  final String receiver;
  final String question;

  QuestionSubmission({
    required this.receiver,
    required this.question,
  });

  Map<String, dynamic> toJson() {
    return {
      'receiver': receiver,
      'question': question,
    };
  }
}

// Answer submission model
class AnswerSubmission {
  final String answer;

  AnswerSubmission({
    required this.answer,
  });

  Map<String, dynamic> toJson() {
    return {
      'answer': answer,
    };
  }
}
