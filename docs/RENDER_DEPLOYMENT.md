# Render.com deployment configuration
# Push to Render.com and it will automatically detect this file

# For Backend (Python/FastAPI)
# 1. Go to https://render.com
# 2. Create new Web Service
# 3. Connect GitHub repository
# 4. Set:
#    - Root Directory: backend
#    - Build Command: pip install -r requirements.txt
#    - Start Command: gunicorn -w 1 -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker main:app
#    - Environment: Python 3.11
# 5. Add environment variables:
#    - ALLOWED_ORIGINS: https://your-frontend-url.onrender.com
#    - DEVICE: cpu

# For Frontend (React)
# 1. Create new Static Site
# 2. Connect GitHub repository
# 3. Set:
#    - Build Command: npm run build
#    - Publish Directory: build
#    - Environment: Node 18
# 4. Set environment variable:
#    - REACT_APP_BACKEND_URL: https://your-backend-url.onrender.com

# Then update frontend .env with:
# REACT_APP_BACKEND_URL=https://your-backend-url.onrender.com
