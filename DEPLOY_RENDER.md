# Quick Deploy to Render

## 🚀 One-Click Deploy

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to https://dashboard.render.com
   - Click **"New +" → "Blueprint"**
   - Connect your GitHub repository
   - Click **"Apply"**
   - Wait 10-15 minutes for first deploy

3. **Done!** Your app will be live at `https://reliamed-app.onrender.com`

## Files Created for Render

✅ `render.yaml` - Configuration file  
✅ `build.sh` - Automated build script  
✅ `requirements.txt` - Python dependencies (cleaned)  
✅ `RENDER_DEPLOYMENT.md` - Full deployment guide  

## What Happens When You Deploy

1. Render creates a PostgreSQL database
2. Installs Python 3.10.12
3. Installs all dependencies (including TensorFlow)
4. Runs database migrations
5. Starts your app with Gunicorn
6. Provides a public URL

## Environment Variables (Auto-Configured)

- ✅ `DATABASE_URL` - PostgreSQL connection
- ✅ `SECRET_KEY` - Auto-generated
- ✅ `PYTHON_VERSION` - 3.10.12

## After First Deploy

### Optional: Create Admin User
Go to your service → Shell tab, then run:
```bash
python
>>> from reliamed import db
>>> from reliamed.models import User
>>> admin = User(username='admin', email_address='admin@example.com', password='yourpassword', is_admin=True)
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

## Free Tier Notes

⚠️ **Service spins down after 15 min of inactivity**  
⏱️ **Cold starts take ~30 seconds**  
💾 **Uploaded files don't persist** (see RENDER_DEPLOYMENT.md for cloud storage solution)

## Troubleshooting

**Build fails?**
- Check logs in Render Dashboard
- Ensure Python version is 3.10.12

**Database errors?**
- Migrations run automatically via build.sh
- Check DATABASE_URL is connected

**Need help?** See full guide in `RENDER_DEPLOYMENT.md`
