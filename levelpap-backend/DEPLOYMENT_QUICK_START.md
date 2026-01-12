# Quick Start: Deploy to Render

## Fastest Way (Using render.yaml)

1. **Push your code:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

3. **Set secrets** (after services are created):
   - Go to your web service → "Environment"
   - Add these manually:
     - `SMTP_USER`
     - `SMTP_PASSWORD`
     - `MPESA_CONSUMER_KEY`
     - `MPESA_CONSUMER_SECRET`
     - `MPESA_SHORTCODE`
     - `MPESA_PASSKEY`
     - `FLUTTERWAVE_PUBLIC_KEY`
     - `FLUTTERWAVE_SECRET_KEY`
     - `FLUTTERWAVE_ENCRYPTION_KEY`
   - Update `CORS_ORIGINS` with your frontend URL

4. **Done!** Your API will be live at: `https://your-service-name.onrender.com`

## What Was Created

✅ `render.yaml` - Render service configuration  
✅ `start.sh` - Production startup script  
✅ `build.sh` - Build script  
✅ `Procfile` - Alternative deployment method  
✅ `runtime.txt` - Python version specification  
✅ `requirements.txt` - Updated with gunicorn  
✅ `RENDER_DEPLOYMENT.md` - Full deployment guide  

## Important Notes

- **Free tier**: Services spin down after 15 min inactivity
- **Database**: Automatically created and linked
- **Migrations**: Run automatically during build
- **Environment**: Set `ENVIRONMENT=production` and `DEBUG=false`

## Need Help?

See `RENDER_DEPLOYMENT.md` for detailed instructions and troubleshooting.




