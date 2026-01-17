# Quick Reference Guide

## 🚀 Start Application (Choose One)

### Option 1: Manual Start
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd frontend
npm install
npm start
```

### Option 2: One-Command (macOS/Linux)
```bash
cd LipReading1
./start.sh
```

### Option 3: One-Command (Windows)
```bash
cd LipReading1
start.bat
```

### Option 4: Docker
```bash
docker-compose up --build
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React app |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API ReDoc | http://localhost:8000/redoc | Alternative docs |

---

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Process Frame
```bash
curl -X POST http://localhost:8000/api/process-frame \
  -H "Content-Type: application/json" \
  -d '{"frame": "data:image/jpeg;base64,..."}'
```

### Reset Session
```bash
curl -X POST http://localhost:8000/api/reset
```

### Model Info
```bash
curl http://localhost:8000/api/model-info
```

---

## 🛠️ Common Commands

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run with auto-reload
uvicorn main:app --reload

# Format code
black .

# Check types
mypy .

# Run tests
pytest tests/
```

### Frontend

```bash
# Install dependencies
npm install

# Start development
npm start

# Build for production
npm run build

# Run tests
npm test

# Format code
npx prettier --write .
```

### Docker

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose up --build backend
```

---

## 📁 Important Files

### Configuration
- `.env` - Environment variables
- `docker-compose.yml` - Docker configuration
- `app.yaml` - Google App Engine config

### Documentation
- `README.md` - Main documentation
- `GETTING_STARTED.md` - Quick setup
- `API_TESTING.md` - API examples
- `RESEARCH.md` - Research paper

### Backend
- `main.py` - FastAPI server
- `model.py` - Neural network
- `preprocessing.py` - Face/lip detection

### Frontend
- `App.js` - Main React component
- `components/` - React components

---

## 🔧 Environment Variables

### Backend (.env)
```
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000
DEVICE=cpu
LOG_LEVEL=info
```

### Frontend (.env.local)
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 60+ |
| Lines of Code | 5000+ |
| Documentation Lines | 8000+ |
| React Components | 5 |
| Python Modules | 5 |
| API Endpoints | 7 |
| CSS Files | 5 |

---

## 🎓 Architecture Overview

```
Browser
  ↓
React Frontend (http://localhost:3000)
  ├─ VideoContainer (Camera)
  ├─ SubtitleBar (Predictions)
  └─ ControlPanel (Controls)
  ↓ (HTTP + Base64 frames)
FastAPI Backend (http://localhost:8000)
  ├─ Face Detection (MediaPipe)
  ├─ Lip Extraction
  └─ CNN-LSTM Model
  ↓ (JSON response)
Browser Display
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Port 3000 in use | Kill process on port 3000, or use different port |
| Port 8000 in use | Kill process on port 8000, or change PORT=xxxx |
| Camera denied | Check browser permissions in Settings |
| CORS error | Check ALLOWED_ORIGINS in .env |
| Module not found | Run `pip install -r requirements.txt` or `npm install` |
| Slow predictions | Enable GPU with DEVICE=cuda in .env |

---

## 📋 Deployment Checklist

### Before Deploying
- [ ] Update `.env` with production values
- [ ] Set ALLOWED_ORIGINS to frontend URL
- [ ] Review error handling
- [ ] Test thoroughly
- [ ] Check logs for warnings
- [ ] Verify model loads

### Render.com Deployment
1. Create backend web service
2. Create frontend static site
3. Set environment variables
4. Deploy
5. Monitor logs

### Google App Engine Deployment
1. Install Cloud SDK
2. Configure app.yaml
3. Run `gcloud app deploy`
4. View logs with `gcloud app logs read`

---

## 🔐 Security Checklist

- [ ] CORS whitelist configured
- [ ] No hardcoded secrets
- [ ] Input validation enabled
- [ ] Error messages sanitized
- [ ] HTTPS enabled (production)
- [ ] Environment variables used
- [ ] Dependencies up to date

---

## 📱 Responsive Design

The application is responsive and works on:
- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768)
- ✅ Tablet (iPad Pro, etc.)
- ✅ Mobile (smaller viewports)

---

## 🎯 Key Features Summary

✅ **Real-time lip reading** without audio
✅ **WebRTC camera access** via browser
✅ **CNN-LSTM deep learning** model
✅ **500-word vocabulary** predictions
✅ **Confidence scoring** display
✅ **Prediction history** tracking
✅ **Professional UI** with animations
✅ **RESTful API** design
✅ **Docker support** for deployment
✅ **Production ready** code

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete documentation |
| GETTING_STARTED.md | 5-minute setup |
| PROJECT_STRUCTURE.md | File organization |
| PROJECT_SUMMARY.md | Completion summary |
| RESEARCH.md | Academic paper style |
| API_TESTING.md | API examples |
| ENVIRONMENT_SETUP.md | Development setup |
| RENDER_DEPLOYMENT.md | Production deployment |
| IMPLEMENTATION_CHECKLIST.md | Verification checklist |

---

## 🎬 Using the Application

1. **Start Application**
   - See "Start Application" section above

2. **Open Browser**
   - Go to http://localhost:3000

3. **Allow Camera**
   - Click browser permission prompt
   - Click "Allow"

4. **Start Recording**
   - Click "Start Live Video"
   - Face should appear in video

5. **Watch Predictions**
   - Subtitles appear in real-time
   - Confidence score shown
   - History panel updates

6. **Stop Recording**
   - Click "Stop Video"

---

## 🔗 Useful Links

- **React Docs**: https://react.dev
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **PyTorch Docs**: https://pytorch.org
- **MediaPipe**: https://mediapipe.dev
- **Docker Docs**: https://docs.docker.com
- **Render.com**: https://render.com

---

## 💡 Tips & Tricks

1. **Better Accuracy**
   - Good lighting improves predictions
   - Clear face in view
   - Straight-on camera angle

2. **Faster Processing**
   - Enable GPU (DEVICE=cuda)
   - Reduce frame capture rate
   - Close unnecessary programs

3. **Development**
   - Use `--reload` flag with uvicorn
   - Watch CSS/JS changes with npm start
   - Check console logs for errors

4. **Debugging**
   - Use browser DevTools (F12)
   - Check backend logs
   - Test API endpoints with curl

---

## 📞 Support Resources

- Read [README.md](./README.md) for comprehensive guide
- Check [GETTING_STARTED.md](./GETTING_STARTED.md) for setup
- Review [API_TESTING.md](./API_TESTING.md) for examples
- See [ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md) for details

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Status**: Production Ready ✅
