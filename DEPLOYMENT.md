# Vercel Deployment Guide

## ⚠️ Important Limitations

### TensorFlow Issue
- **Problem**: TensorFlow (~400MB) exceeds Vercel's 250MB serverless function limit
- **Solutions**:
  1. Disable ML prediction feature for Vercel deployment
  2. Use a separate ML API service (AWS Lambda, Google Cloud Functions)
  3. Deploy to Heroku/Railway/Render instead (recommended)

### File Upload Issue
- **Problem**: Vercel is serverless - uploaded files don't persist
- **Solution**: Use cloud storage (AWS S3, Cloudinary, Vercel Blob)

### Database Issue
- **Problem**: SQLite doesn't work on serverless platforms
- **Solution**: Use PostgreSQL (Vercel Postgres, Neon, Supabase)

## Deployment Steps

### Option 1: Without ML Features (Quick Deploy)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Disable ML prediction temporarily**:
   Comment out the TensorFlow import in `reliamed/trained_model.py`

3. **Deploy**:
   ```bash
   vercel
   ```

### Option 2: Deploy to Heroku (Recommended for this app)

1. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 3: Deploy to Railway

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

## Environment Variables Needed

For any platform, set these:
- `SECRET_KEY`: Random secret key for Flask
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: production

## Files Created for Vercel

- `vercel.json` - Vercel configuration
- `requirements-vercel.txt` - Minimal dependencies (no TensorFlow)
- `.vercelignore` - Files to exclude from deployment

## Recommendation

Given this app uses TensorFlow for ML predictions, **Heroku, Railway, or Render** are better choices than Vercel. They support larger apps and persistent storage better.
