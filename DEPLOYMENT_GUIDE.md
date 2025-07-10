# AskMe Deployment Guide

## 🚀 Production Deployment Options

### Option 1: Railway (Recommended)
1. Connect your GitHub repo to Railway
2. Set environment variables:
   ```
   PUBLIC_SUPABASE_URL=your_supabase_url
   PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   FLASK_ENV=production
   ```
3. Railway will auto-deploy on git push

### Option 2: Heroku
1. Create Heroku app
2. Add Python buildpack
3. Create `Procfile`:
   ```
   web: python api.py
   ```
4. Set environment variables in Heroku dashboard
5. Deploy via git push

### Option 3: DigitalOcean App Platform
1. Connect GitHub repo
2. Select Python app type
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python api.py`
5. Configure environment variables

### Option 4: AWS/Google Cloud
1. Use their respective Python/Flask deployment guides
2. Set up environment variables
3. Configure load balancer and SSL

## 🔧 Production Configuration

### Environment Variables
```bash
PUBLIC_SUPABASE_URL=https://your-project.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-anon-key
FLASK_ENV=production
FLASK_DEBUG=False
```

### Update api.py for Production
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
```

### CORS Configuration
Update CORS for production domains:
```python
CORS(app, origins=['https://your-flutter-app.com'])
```

## 📱 Flutter App Updates

### Update API Base URL
```dart
class Config {
  static const String apiBaseUrl = 'https://your-backend.railway.app';
  static const bool isDevelopment = false;
}
```

### Add Network Security Config (Android)
Add to `android/app/src/main/res/xml/network_security_config.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">your-backend.railway.app</domain>
    </domain-config>
</network-security-config>
```

## 🔒 Security Checklist

- [ ] Use HTTPS in production
- [ ] Set proper CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable Supabase RLS policies
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates

## 📊 Monitoring

### Add Health Check Endpoint
Already included in your API:
```http
GET /health
```

### Logging
Add to your deployment platform:
- Request/response logging
- Error tracking (Sentry)
- Performance monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/cli@v2
        with:
          command: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 🧪 Testing in Production

### Health Check
```bash
curl https://your-backend.railway.app/health
```

### Test Authentication
```bash
curl -X POST https://your-backend.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Your backend is production-ready!
