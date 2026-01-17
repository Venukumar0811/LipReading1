# Render Deployment Setup Guide

Your project is now configured for deployment on Render.com. Follow these steps:

## Prerequisites
- Render.com account (free tier available)
- GitHub repository with this project pushed

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Deploy Backend

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `lip-reading-backend`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3.11
   - **Build Command:** `pip install -r requirements-prod.txt`
   - **Start Command:** `gunicorn -w 1 -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker main:app`
   - **Free tier:** Select if using free plan (slower, sleeps after 15 min inactivity)

5. Add Environment Variables:
   - `ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://lip-reading-frontend.onrender.com`)
   - `DEVICE`: `cpu`
   - `LOG_LEVEL`: `info`

6. Click **"Create Web Service"** and wait for deployment

### 3. Deploy Frontend

1. Once backend is deployed, note its URL (e.g., `https://lip-reading-backend.onrender.com`)
2. Click **"New +"** → **"Static Site"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `lip-reading-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Publish Directory:** `build`

5. Add Environment Variable:
   - `REACT_APP_BACKEND_URL`: Your backend URL (e.g., `https://lip-reading-backend.onrender.com`)

6. Click **"Create Static Site"** and wait for deployment

## After Deployment

1. Update `backend/requirements-prod.txt` if you add new dependencies
2. Test the API at `https://your-backend-url.onrender.com/docs`
3. Access your app at `https://your-frontend-url.onrender.com`

## Important Notes

- **Free Tier Limitations:**
  - Spins down after 15 minutes of inactivity
  - Slower startup time
  - Limited to 1 worker process

- **Production Considerations:**
  - Use a paid plan for production deployments
  - Add error monitoring (e.g., Sentry)
  - Set up automated deployments with GitHub integration

## Troubleshooting

If deployment fails:
1. Check the deployment logs in Render dashboard
2. Ensure all environment variables are set correctly
3. Verify `requirements-prod.txt` has all necessary packages
4. Check that your GitHub repo is public or Render has access

## Configuration Files Used

- `render.yaml` - Render deployment configuration
- `Dockerfile` - Docker image definition
- `backend/requirements-prod.txt` - Production dependencies
- `frontend/package.json` - Frontend dependencies
