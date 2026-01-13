# Render Deployment Guide - EasyXpense Backend

## Required Environment Variables

Set these in your Render dashboard under "Environment":

### Required Variables
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/easyxpense?retryWrites=true&w=majority
FLASK_ENV=production
```

### Optional Variables (with defaults)
```
PORT=10000  # Render sets this automatically
PYTHON_VERSION=3.11.0  # Specified in runtime.txt
```

## Render Service Configuration

### Basic Settings
- **Name**: `easyxpense-backend`
- **Environment**: `Python`
- **Region**: `Oregon (US West)` or closest to your users
- **Branch**: `main`
- **Root Directory**: `backend` (if backend is in subdirectory)

### Build & Deploy Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info`

### Advanced Settings
- **Auto-Deploy**: `Yes`
- **Health Check Path**: `/api/health`

## Pre-Deployment Checklist

### ✅ Code Structure
- [ ] `wsgi.py` exists in backend root
- [ ] `requirements.txt` contains all dependencies
- [ ] `runtime.txt` specifies Python version
- [ ] `Procfile` has correct gunicorn command
- [ ] All Python files pass syntax validation

### ✅ Environment Configuration
- [ ] MongoDB Atlas cluster is running
- [ ] Database user has read/write permissions
- [ ] Network access allows connections from anywhere (0.0.0.0/0)
- [ ] MONGO_URI is correctly formatted
- [ ] FLASK_ENV is set to "production"

### ✅ Application Health
- [ ] Health check endpoint `/api/health` returns 200
- [ ] CORS allows requests from Netlify domain
- [ ] All API endpoints are properly registered
- [ ] Error handlers return JSON responses

### ✅ Render Configuration
- [ ] GitHub repository is connected
- [ ] Environment variables are set
- [ ] Build and start commands are correct
- [ ] Health check path is configured

## Post-Deployment Validation

### 1. Check Deployment Logs
```bash
# Look for these success messages in Render logs:
# "Starting EasyXpense Backend..."
# "MongoDB connection successful"
# "All blueprints registered successfully"
# "EasyXpense Backend initialized successfully"
```

### 2. Test Health Endpoint
```bash
curl https://your-app-name.onrender.com/api/health
# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "database": "connected",
  "environment": "production",
  "version": "1.0.0",
  "database_ping": "success"
}
```

### 3. Test API Endpoints
```bash
# Test friends endpoint
curl https://your-app-name.onrender.com/api/friends

# Test expenses endpoint  
curl https://your-app-name.onrender.com/api/expenses

# Test debts endpoint
curl https://your-app-name.onrender.com/api/debts
```

### 4. Test CORS from Frontend
- Open browser developer tools
- Navigate to your Netlify frontend
- Check that API calls succeed without CORS errors

## Troubleshooting Common Issues

### Build Failures
- **Issue**: `ModuleNotFoundError`
- **Solution**: Check `requirements.txt` has all dependencies

### Runtime Errors
- **Issue**: `MONGO_URI environment variable is required`
- **Solution**: Set MONGO_URI in Render environment variables

### Database Connection Issues
- **Issue**: `MongoDB connection failed`
- **Solutions**:
  - Verify MongoDB Atlas cluster is running
  - Check network access settings (allow 0.0.0.0/0)
  - Verify database user credentials
  - Test connection string format

### CORS Errors
- **Issue**: Frontend can't access backend
- **Solution**: Verify Netlify domain is in CORS origins

### Cold Start Issues
- **Issue**: First request after inactivity is slow
- **Solution**: This is normal for free Render services

## Monitoring & Maintenance

### Health Monitoring
- Render automatically monitors `/api/health` endpoint
- Service restarts if health checks fail
- Check logs regularly for errors

### Performance
- Free tier: Service sleeps after 15 minutes of inactivity
- Paid tier: Always-on service with better performance
- Monitor response times and error rates

### Updates
- Push to main branch triggers automatic deployment
- Monitor deployment logs for issues
- Test thoroughly before pushing to production

## Support Resources

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/
- **MongoDB Atlas**: https://docs.atlas.mongodb.com/