# Render Deployment Guide

This guide will help you deploy the LevelPAP Backend to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Payment provider credentials (M-Pesa, Flutterwave) if using payment features

## Deployment Methods

### Method 1: Using render.yaml (Recommended)

This is the easiest method as it automatically sets up both the web service and database.

#### Steps:

1. **Push your code to Git**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect Repository to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will detect `render.yaml` automatically

3. **Review Configuration**
   - Render will show you the services it will create
   - Review the configuration and click "Apply"

4. **Set Environment Variables**
   After the services are created, go to your web service and set these environment variables manually:
   - `SMTP_USER` - Your email address
   - `SMTP_PASSWORD` - Your email app password
   - `MPESA_CONSUMER_KEY` - M-Pesa consumer key
   - `MPESA_CONSUMER_SECRET` - M-Pesa consumer secret
   - `MPESA_SHORTCODE` - M-Pesa shortcode
   - `MPESA_PASSKEY` - M-Pesa passkey
   - `FLUTTERWAVE_PUBLIC_KEY` - Flutterwave public key
   - `FLUTTERWAVE_SECRET_KEY` - Flutterwave secret key
   - `FLUTTERWAVE_ENCRYPTION_KEY` - Flutterwave encryption key
   - `CORS_ORIGINS` - Your frontend URL(s), comma-separated

5. **Update CORS Origins**
   - In the web service settings, update `CORS_ORIGINS` to include your frontend domain
   - Example: `https://your-frontend.vercel.app,https://your-frontend.netlify.app`

6. **Deploy**
   - Render will automatically build and deploy your application
   - The database migrations will run automatically during build

### Method 2: Manual Setup

If you prefer to set up services manually:

#### 1. Create PostgreSQL Database

1. Go to Render Dashboard → "New +" → "PostgreSQL"
2. Name it: `levelpap-db`
3. Select your plan (Free tier available)
4. Click "Create Database"
5. Note the connection string (you'll need it later)

#### 2. Create Web Service

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your Git repository
3. Configure the service:
   - **Name**: `levelpap-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `levelpap-backend` (if your repo root is parent directory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

#### 3. Set Environment Variables

In your web service settings, add these environment variables:

**Required:**
- `DATABASE_URL` - Copy from your PostgreSQL service (Render sets this automatically if you link services)
- `SECRET_KEY` - Generate a strong random string (you can use: `openssl rand -hex 32`)
- `ALGORITHM` - `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
- `ENVIRONMENT` - `production`
- `DEBUG` - `false`
- `CORS_ORIGINS` - Your frontend URL(s), comma-separated

**Email (Optional):**
- `SMTP_HOST` - `smtp.gmail.com`
- `SMTP_PORT` - `587`
- `SMTP_USER` - Your email address
- `SMTP_PASSWORD` - Your email app password
- `FROM_EMAIL` - `noreply@levelpap.com`

**Payment Providers (Optional):**
- `MPESA_CONSUMER_KEY` - Your M-Pesa consumer key
- `MPESA_CONSUMER_SECRET` - Your M-Pesa consumer secret
- `MPESA_SHORTCODE` - Your M-Pesa shortcode
- `MPESA_PASSKEY` - Your M-Pesa passkey
- `MPESA_ENVIRONMENT` - `sandbox` or `production`
- `FLUTTERWAVE_PUBLIC_KEY` - Your Flutterwave public key
- `FLUTTERWAVE_SECRET_KEY` - Your Flutterwave secret key
- `FLUTTERWAVE_ENCRYPTION_KEY` - Your Flutterwave encryption key

#### 4. Deploy

1. Click "Create Web Service"
2. Render will build and deploy your application
3. Wait for the build to complete
4. Your API will be available at: `https://your-service-name.onrender.com`

## Post-Deployment

### 1. Verify Deployment

- Visit `https://your-service-name.onrender.com/health` - Should return `{"status": "healthy"}`
- Visit `https://your-service-name.onrender.com/docs` - Should show FastAPI Swagger UI
- Visit `https://your-service-name.onrender.com/` - Should return API info

### 2. Test Database Connection

The database migrations should have run automatically. Verify by:
- Checking the Render logs for migration output
- Testing an endpoint that requires database access

### 3. Update Frontend

Update your frontend application to use the new API URL:
```
https://your-service-name.onrender.com/api
```

## Environment Variables Reference

Create a `.env` file locally (not committed to Git) with these variables for local development:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/levelpap_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@levelpap.com

# Payment Providers - M-Pesa
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_ENVIRONMENT=sandbox

# Payment Providers - Flutterwave
FLUTTERWAVE_PUBLIC_KEY=your-flutterwave-public-key
FLUTTERWAVE_SECRET_KEY=your-flutterwave-secret-key
FLUTTERWAVE_ENCRYPTION_KEY=your-flutterwave-encryption-key

# App Settings
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Troubleshooting

### Build Fails

1. **Check logs** in Render dashboard
2. **Verify requirements.txt** is correct
3. **Check Python version** - Render uses Python 3.11 by default
4. **Verify build command** - Should be: `pip install -r requirements.txt && alembic upgrade head`

### Database Connection Issues

1. **Verify DATABASE_URL** is set correctly
2. **Check database is running** in Render dashboard
3. **Verify migrations ran** - Check build logs for `alembic upgrade head` output
4. **Check database credentials** - Ensure they're correct

### Application Crashes

1. **Check application logs** in Render dashboard
2. **Verify all required environment variables** are set
3. **Check SECRET_KEY** is set (required for JWT)
4. **Verify CORS_ORIGINS** includes your frontend URL

### Migrations Not Running

If migrations don't run automatically:
1. Go to your web service → "Shell"
2. Run: `alembic upgrade head`
3. Or add to build command: `pip install -r requirements.txt && alembic upgrade head`

## Production Considerations

### 1. Upgrade Plans

- **Free tier** is great for testing but has limitations:
  - Services spin down after 15 minutes of inactivity
  - Limited resources
- **Starter/Standard plans** recommended for production:
  - Always-on services
  - Better performance
  - More resources

### 2. Security

- **Never commit** `.env` file or secrets to Git
- **Use Render's environment variables** for all secrets
- **Generate strong SECRET_KEY** for production
- **Set DEBUG=false** in production
- **Use HTTPS** (Render provides this automatically)

### 3. Database Backups

- Enable automatic backups in Render dashboard
- Consider upgrading database plan for production

### 4. Monitoring

- Monitor logs in Render dashboard
- Set up health check alerts
- Monitor database connections

### 5. CORS Configuration

- Only allow your frontend domain(s) in `CORS_ORIGINS`
- Don't use `*` in production
- Use HTTPS URLs only

## Custom Domain (Optional)

1. Go to your web service → "Settings" → "Custom Domains"
2. Add your domain
3. Follow Render's DNS configuration instructions
4. Update `CORS_ORIGINS` to include your custom domain

## Scaling

If you need to scale:
1. Upgrade your web service plan
2. Increase worker count in start command: `--workers 4`
3. Upgrade database plan if needed
4. Consider using Redis for caching (future enhancement)

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- FastAPI Documentation: https://fastapi.tiangolo.com

## Quick Deploy Checklist

- [ ] Code pushed to Git repository
- [ ] Repository connected to Render
- [ ] Database service created (or using render.yaml)
- [ ] Web service created
- [ ] All environment variables set
- [ ] CORS_ORIGINS updated with frontend URL
- [ ] Build successful
- [ ] Health check endpoint working
- [ ] API documentation accessible
- [ ] Database migrations completed
- [ ] Frontend updated with new API URL

---

**Your API will be live at:** `https://your-service-name.onrender.com`

**API Documentation:** `https://your-service-name.onrender.com/docs`

**Health Check:** `https://your-service-name.onrender.com/health`




