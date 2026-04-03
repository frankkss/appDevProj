# Render Deployment Guide

## Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)
- Your code pushed to a GitHub repository

## Deployment Steps

### Option 1: Deploy via Render Dashboard (Easiest)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Go to Render Dashboard**:
   - Visit https://dashboard.render.com
   - Click "New +" → "Blueprint"

3. **Connect Repository**:
   - Connect your GitHub account
   - Select your repository
   - Render will automatically detect `render.yaml`

4. **Review and Deploy**:
   - Review the services (Web Service + PostgreSQL Database)
   - Click "Apply"
   - Render will create both services automatically

### Option 2: Manual Setup

1. **Create PostgreSQL Database**:
   - Click "New +" → "PostgreSQL"
   - Name: `reliamed-db`
   - Database: `reliamed`
   - User: `reliamed_user`
   - Click "Create Database"
   - **Copy the Internal Database URL** (starts with `postgres://`)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `reliamed-app`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

3. **Add Environment Variables**:
   - `PYTHON_VERSION`: `3.10.12`
   - `SECRET_KEY`: (generate a random string, e.g., `openssl rand -hex 32`)
   - `DATABASE_URL`: (paste the Internal Database URL from step 1)

4. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy your app

### After Deployment

1. **Initialize Database**:
   Once deployed, you need to run migrations. Go to your web service shell:
   - In Render Dashboard → Your Web Service → "Shell" tab
   - Run:
     ```bash
     flask db upgrade
     ```

2. **Create Admin User** (Optional):
   In the shell, run:
   ```bash
   python
   >>> from reliamed import db
   >>> from reliamed.models import User
   >>> admin = User(username='admin', email_address='admin@reliamed.com', password='admin123', is_admin=True)
   >>> db.session.add(admin)
   >>> db.session.commit()
   >>> exit()
   ```

## Environment Variables

Your app needs these environment variables:
- `DATABASE_URL`: Provided automatically by Render PostgreSQL
- `SECRET_KEY`: Random secret for Flask sessions
- `PYTHON_VERSION`: `3.10.12` (important for TensorFlow compatibility)

## Important Notes

### File Uploads
- **Problem**: Uploaded files (profile pics, medicine images) won't persist on Render's free tier
- **Solution**: Use cloud storage:
  - **Cloudinary** (recommended, free tier): https://cloudinary.com
  - **AWS S3**
  - **Render Disk** (paid feature)

### First Deploy
- First deployment will take 10-15 minutes (TensorFlow is large)
- Subsequent deploys are faster (~5 minutes)

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- 750 hours/month free (enough for one service running 24/7)

### Upgrading to Paid Tier
For better performance:
- No spin-down (always on)
- Faster builds
- More resources
- Starting at $7/month

## Troubleshooting

### Build Fails
- Check Python version is `3.10.12`
- Verify all dependencies in requirements.txt are compatible

### Database Connection Issues
- Ensure DATABASE_URL is set correctly
- Check if migrations have been run (`flask db upgrade`)

### App Not Starting
- Check logs in Render Dashboard → Your Service → "Logs"
- Verify start command: `gunicorn app:app`

## Monitoring
- **Logs**: Render Dashboard → Your Service → "Logs"
- **Metrics**: Dashboard shows CPU, memory usage
- **Events**: Track deployments and restarts

## Custom Domain (Optional)
1. Go to your web service → "Settings"
2. Add your custom domain
3. Update DNS records as instructed
4. SSL certificate is added automatically

## Cost Estimate
- **Free Tier**: $0/month (with limitations)
- **Starter Plan**: $7/month (no spin-down, better performance)
- **PostgreSQL**: Free tier available, or $7/month for more storage

---

Your app will be available at: `https://reliamed-app.onrender.com`
(or your custom domain)
