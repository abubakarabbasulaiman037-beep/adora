# Quick START: Rendering Backend Deployment

## What's Been Prepared

✅ Backend configured for production deployment
✅ Environment variables template created
✅ Flutter app ready to switch to production URLs
✅ Deployment configuration files added
✅ Git ignore updated for security

## QUICK STEPS (5 minutes)

### 1. Push to GitHub
```bash
cd ~/adora

# If not already initialized
git init
git add .
git commit -m "Deploy to Render"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/adora.git
git branch -M main
git push -u origin main
```

### 2. Create Render PostgreSQL
- Go to https://dashboard.render.com/
- Create → PostgreSQL
- Copy the connection string

### 3. Deploy Backend to Render
- Create → Web Service
- Connect GitHub repo (adora)
- Build: `pip install -r requirements.txt`
- Start: `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app --access-logfile - --error-logfile -`
- Add environment variables (see below)

### 4. Environment Variables to Add
```
DATABASE_URL = [your PostgreSQL connection string]
SECRET_KEY = [generate random: python -c "import secrets; print(secrets.token_urlsafe(32))"]
DERIV_API_TOKEN = [your token]
PAYSTACK_SECRET_KEY = [your key]
ADMIN_EMAIL = kingalameen@admin.com
ADMIN_PASSWORD = [change this!]
CORS_ORIGINS = ["*"]
```

### 5. Update Flutter App
After deployment, update these lines:

**In api_service.dart:**
```dart
static const String defaultProductionUrl = 'https://your-app.onrender.com/api';
```

**In market_service.dart:**
```dart
static const String defaultProductionWsUrl = 'wss://your-app.onrender.com/ws/market';
```

Then use ConfigService to switch:
```dart
final config = ConfigService();
await config.init();
await config.switchToProduction();
```

## Files Created/Modified

- ✅ `backend/.env.example` - Environment variable template
- ✅ `backend/requirements.txt` - Added gunicorn
- ✅ `render.yaml` - Render deployment config
- ✅ `lib/services/api_service.dart` - Configurable API URL
- ✅ `lib/services/market_service.dart` - Configurable WebSocket URL
- ✅ `lib/services/config_service.dart` - URL configuration manager
- ✅ `.gitignore` - Updated for security
- ✅ `DEPLOYMENT_GUIDE.md` - Full deployment guide

## Your Backend URL Will Be
`https://adora-backend.onrender.com` (or similar)

Update all references in your Flutter app after deployment!

See `DEPLOYMENT_GUIDE.md` for full instructions.
