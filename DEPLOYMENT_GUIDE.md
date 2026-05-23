# Deployment Guide - Render Backend Hosting

## Step 1: Prepare your Backend

Your backend is now configured for Render deployment. The following files have been created/updated:

- `backend/.env.example` - Template for environment variables
- `render.yaml` - Render deployment configuration
- `backend/requirements.txt` - Updated with gunicorn
- `.gitignore` - Updated to exclude sensitive files

## Step 2: Push to GitHub

### 2.1 Initialize Git (if not already done)
```bash
cd ~/adora
git init
git add .
git commit -m "Initial commit - prepare for Render deployment"
```

### 2.2 Create a GitHub repository
1. Go to https://github.com/new
2. Create a new repository named `adora` (or your preferred name)
3. Do NOT initialize with README (we already have one)
4. Copy the repository URL (HTTPS or SSH)

### 2.3 Add remote and push
```bash
git remote add origin https://github.com/YOUR_USERNAME/adora.git
git branch -M main
git push -u origin main
```

## Step 3: Set Up Render PostgreSQL Database

1. Go to https://dashboard.render.com/
2. Click "Create" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `adora-db` (or your choice)
   - **Database**: `adora`
   - **Region**: Select a region close to you
   - **PostgreSQL Version**: 15
4. Click "Create Database"
5. Wait for the database to be created (5-10 minutes)
6. Copy the connection string (External URL or Internal URL)

## Step 4: Deploy Backend to Render

### 4.1 Connect your GitHub repository
1. Go to https://dashboard.render.com/
2. Click "Create" → "Web Service"
3. Select "Deploy existing project from GitHub"
4. Authorize GitHub and select the `adora` repository
5. Click "Connect"

### 4.2 Configure the service
1. **Name**: `adora-backend` (or your choice)
2. **Region**: Same as your database or close by
3. **Branch**: `main`
4. **Runtime**: `Python 3`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app --access-logfile - --error-logfile -`

### 4.3 Add Environment Variables
In the "Environment" section, add these variables:

- **DATABASE_URL**: Paste your PostgreSQL connection string from step 3
- **SECRET_KEY**: Generate a random secret key or use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- **DERIV_API_TOKEN**: Your Deriv API token
- **PAYSTACK_SECRET_KEY**: Your Paystack secret key (if using payments)
- **ADMIN_EMAIL**: Your admin email
- **ADMIN_PASSWORD**: Your admin password (change this in production!)
- **CORS_ORIGINS**: `["https://yourdomain.com","https://app.yourdomain.com"]` (update with your frontend domain)

### 4.4 Deploy
Click "Create Web Service" and wait for deployment to complete.

## Step 5: Update Frontend Configuration

### 5.1 Update API URLs in Flutter
After your backend is deployed on Render, you'll get a URL like: `https://adora-backend.onrender.com`

Update the URLs in your Flutter app:

**Option 1: Use ConfigService (Recommended)**
```dart
import 'services/config_service.dart';

// In your main.dart or initialization code:
final configService = ConfigService();
await configService.init();

// Switch to production (one-time after deployment)
await configService.switchToProduction(productionApiUrl: 'https://your-backend.onrender.com/api',
                                       productionWsUrl: 'wss://your-backend.onrender.com/ws/market');
```

**Option 2: Manual Update**
Edit `lib/services/api_service.dart` and `lib/services/market_service.dart` and replace the production URLs with your Render URL:
- API URL: `https://adora-backend.onrender.com/api`
- WebSocket URL: `wss://adora-backend.onrender.com/ws/market`

### 5.2 Update .env.example for reference
Update the backend/.env.example with your production URLs for team reference:
```env
DATABASE_URL=postgresql://user:password@your-render-db.internal/adora
# Backend URL (for reference)
# https://adora-backend.onrender.com
```

## Step 6: Verify Deployment

### 6.1 Check Render logs
1. Go to https://dashboard.render.com/
2. Click on your `adora-backend` service
3. Go to "Logs" to check for any errors

### 6.2 Test the API
```bash
curl https://your-backend.onrender.com/

# Expected response:
# {"message": "Welcome to ABBANDAYA Backend API", "version": "1.0.0"}
```

### 6.3 Test a protected endpoint (requires token):
```bash
curl -X GET https://your-backend.onrender.com/api/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Step 7: Set Up Auto-Deployment

Your `render.yaml` file includes `autoDeploy: true`, which means:
- Every push to the `main` branch will automatically trigger a new deployment
- No need to manually redeploy

## Troubleshooting

### Backend won't start
- Check the Render logs for errors
- Ensure all environment variables are set correctly
- Verify the database connection string is correct

### Database connection errors
- Make sure the PostgreSQL database is fully created
- If using internal URL, check that the web service is in the same region as the database
- Try using the external URL if internal doesn't work

### WebSocket connection fails
- Change WebSocket URL from `ws://` to `wss://` (secure WebSocket)
- If still failing, ensure WebSocket is enabled in your Render service

### CORS errors
- Update `CORS_ORIGINS` in environment variables to include your frontend domain
- For development: `["*"]` (not recommended for production)

## Security Checklist

- [ ] Change default admin password in environment variables
- [ ] Generate a strong SECRET_KEY
- [ ] Set CORS_ORIGINS to specific domains (not `["*"]` in production)
- [ ] Enable HTTPS for all connections
- [ ] Keep your `.env` file secret and never commit it to Git
- [ ] Regularly update dependencies for security patches

## Next Steps

1. Test all API endpoints from your Flutter app
2. Set up monitoring and logging
3. Configure backup for your PostgreSQL database
4. Set up a domain name for your Render service
5. Consider upgrading to a paid Render plan for better performance and reliability
