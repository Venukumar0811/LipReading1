# Getting Started Guide

## Quick Setup (5 Minutes)

### Step 1: Install Dependencies

**Windows:**
```bash
cd d:\LipReading1\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ..\frontend
npm install
```

**macOS/Linux:**
```bash
cd ~/LipReading1/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install
```

### Step 2: Start Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start Frontend (New Terminal)

```bash
cd frontend
npm start
```

Browser should open automatically to http://localhost:3000

### Step 4: Test Application

1. Allow camera permission
2. Click "Start Live Video"
3. Position your face in front of camera
4. Watch predictions appear in real-time!

---

## Detailed Setup

### Backend Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run backend
python main.py
```

### Frontend Setup

```bash
# 1. Install Node packages
npm install

# 2. Create .env file
echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env

# 3. Start development server
npm start
```

### Verify Installation

**Backend Health Check:**
```bash
curl http://localhost:8000/health
```

**API Documentation:**
Open http://localhost:8000/docs in browser

---

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Camera Permission Issue

1. Check browser settings for camera permission
2. Reload page
3. Try in incognito/private mode

### Dependencies Installation Fails

```bash
# Clear pip cache
pip cache purge

# Reinstall
pip install -r requirements.txt --no-cache-dir
```

---

For more details, see [README.md](../README.md)
