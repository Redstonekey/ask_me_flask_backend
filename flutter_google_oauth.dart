// Google OAuth Service for Flutter
// Add these dependencies to pubspec.yaml:
// google_sign_in: ^6.1.5
// googleapis_auth: ^1.4.1

import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class GoogleAuthService {
  static const String baseUrl = 'http://localhost:5000';
  
  // Configure Google Sign In
  static final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
    // Add your Google OAuth client ID here
    clientId: 'your-google-client-id.apps.googleusercontent.com',
  );
  
  /// Sign in with Google and authenticate with your backend
  static Future<Map<String, dynamic>> signInWithGoogle() async {
    try {
      // Trigger Google Sign In
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      
      if (googleUser == null) {
        throw Exception('Google sign in was cancelled');
      }
      
      // Get Google authentication details
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      
      if (googleAuth.idToken == null) {
        throw Exception('Failed to get Google ID token');
      }
      
      // Send ID token to your backend
      final response = await http.post(
        Uri.parse('$baseUrl/auth/google'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'id_token': googleAuth.idToken,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // Store the token for future requests
        ApiClient.setToken(data['session']['access_token']);
        return data;
      } else {
        throw Exception(jsonDecode(response.body)['error']);
      }
    } catch (e) {
      throw Exception('Google sign in failed: $e');
    }
  }
  
  /// Sign out from Google
  static Future<void> signOut() async {
    try {
      await _googleSignIn.signOut();
    } catch (e) {
      print('Error signing out from Google: $e');
    }
  }
  
  /// Check if user is signed in to Google
  static Future<bool> isSignedIn() async {
    return await _googleSignIn.isSignedIn();
  }
  
  /// Get current Google user
  static Future<GoogleSignInAccount?> getCurrentUser() async {
    return await _googleSignIn.signInSilently();
  }
}

// Enhanced AuthService with Google OAuth
class AuthService {
  static const String baseUrl = 'http://localhost:5000';
  
  /// Regular email/password signup
  static Future<Map<String, dynamic>> signup(String email, String password, String username) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/signup'),
      headers: {'Content-Type': 'application/json'},
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
  
  /// Regular email/password login
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
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
  
  /// Google OAuth login
  static Future<Map<String, dynamic>> loginWithGoogle() async {
    return await GoogleAuthService.signInWithGoogle();
  }
  
  /// Refresh access token
  static Future<Map<String, dynamic>> refreshToken(String refreshToken) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/refresh'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'refresh_token': refreshToken,
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
  
  /// Logout (both regular and Google)
  static Future<void> logout() async {
    try {
      // Logout from your backend
      await http.post(
        Uri.parse('$baseUrl/auth/logout'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${ApiClient._token}',
        },
      );
    } catch (e) {
      print('Backend logout error: $e');
    }
    
    // Sign out from Google
    await GoogleAuthService.signOut();
    
    // Clear stored token
    ApiClient.clearToken();
  }
}

// Updated ApiClient with token management
class ApiClient {
  static const String baseUrl = 'http://localhost:5000';
  static String? _token;
  
  static void setToken(String token) {
    _token = token;
    // Also save to persistent storage
    _saveTokenToStorage(token);
  }
  
  static void clearToken() {
    _token = null;
    _clearTokenFromStorage();
  }
  
  static String? get token => _token;
  
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    if (_token != null) 'Authorization': 'Bearer $_token',
  };
  
  // Save token to SharedPreferences or secure storage
  static void _saveTokenToStorage(String token) {
    // Implementation depends on your storage choice
    // SharedPreferences.getInstance().then((prefs) => prefs.setString('access_token', token));
  }
  
  static void _clearTokenFromStorage() {
    // Implementation depends on your storage choice
    // SharedPreferences.getInstance().then((prefs) => prefs.remove('access_token'));
  }
}

// Example usage in your Flutter app
class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isLoading = false;
  
  Future<void> _handleGoogleSignIn() async {
    setState(() => _isLoading = true);
    
    try {
      final result = await AuthService.loginWithGoogle();
      
      // Navigate to home screen
      Navigator.pushReplacementNamed(context, '/home');
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Welcome ${result['user']['username']}!')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login failed: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Regular login form here...
            
            SizedBox(height: 20),
            Text('OR'),
            SizedBox(height: 20),
            
            // Google Sign In Button
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _handleGoogleSignIn,
              icon: Icon(Icons.login),
              label: _isLoading 
                ? CircularProgressIndicator() 
                : Text('Sign in with Google'),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
