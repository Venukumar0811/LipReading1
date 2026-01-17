# Environment Setup Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **CPU**: Intel i5 or equivalent
- **RAM**: 8GB minimum
- **Disk**: 10GB free space
- **Webcam**: USB or integrated camera
- **Network**: Broadband internet (for npm/pip packages)

### Recommended Requirements
- **CPU**: Intel i7 / AMD Ryzen 5 or better
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **SSD**: 20GB+ free space
- **Network**: Gigabit connection

---

## Software Installation

### 1. Python Setup

#### Windows
```bash
# Download Python 3.11 from python.org
# Run installer and add to PATH

# Verify installation
python --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3-pip python3-venv

# Verify installation
python3 --version
```

### 2. Node.js Setup

#### Windows
```bash
# Download from nodejs.org (Node 18+)
# Run installer

# Verify installation
node --version
npm --version
```

#### macOS
```bash
# Using Homebrew
brew install node@18

# Verify installation
node --version
npm --version
```

#### Linux
```bash
# Using NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### 3. Git Setup

#### Windows
Download from git-scm.com and run installer

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt-get install git
```

### 4. Docker Setup (Optional)

#### Windows
Download Docker Desktop from docker.com

#### macOS
```bash
brew install docker
```

#### Linux
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

---

## Virtual Environment Setup

### Python Virtual Environment

#### Windows
```bash
cd d:\LipReading1\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### macOS/Linux
```bash
cd ~/LipReading1/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verify Installation
```bash
python -m pip list | grep -E "fastapi|torch|opencv"
```

---

## IDE Setup

### VS Code Setup

1. **Install Extensions**
   - Python (Microsoft)
   - Pylance
   - ES7+ React/Redux/React-Native snippets
   - Prettier - Code formatter
   - REST Client

2. **Python Interpreter**
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choose `./venv/Scripts/python` (Windows) or `./venv/bin/python` (macOS/Linux)

3. **Debug Configuration**
   - Create `.vscode/launch.json`
   - Configure Python debugger
   - Configure Chrome debugger for React

### PyCharm Setup

1. **Create Project**
   - File → Open → Select project folder
   - Configure Python interpreter from venv

2. **Run Configurations**
   - Run → Edit Configurations
   - Add Python configuration: Script path = `backend/main.py`

### WebStorm/IntelliJ Setup

1. **Configure Node**
   - File → Settings → Languages & Frameworks → Node.js
   - Set Node.js interpreter

2. **Run Configuration**
   - Run → Edit Configurations
   - Add npm configuration: Command = `start`

---

## Environment Variables

### Backend (.env)

```bash
# Server Configuration
PORT=8000
DEVICE=cpu  # or "cuda" for GPU

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=info  # debug, info, warning, error

# Model Configuration
MODEL_PATH=lip_reading_model.pt
BATCH_SIZE=1
```

### Frontend (.env.local)

```bash
# API Configuration
REACT_APP_BACKEND_URL=http://localhost:8000

# Feature Flags
REACT_APP_DEBUG_MODE=false
REACT_APP_LOG_LEVEL=info

# API Timeout (ms)
REACT_APP_API_TIMEOUT=30000
```

---

## Dependency Management

### Python Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install fastapi==0.109.0

# Update all packages
pip install --upgrade -r requirements.txt

# List installed packages
pip list

# Generate requirements from current environment
pip freeze > requirements.txt
```

### Node Dependencies

```bash
# Install all dependencies
npm install

# Install specific package
npm install axios@latest

# Update all packages
npm update

# List installed packages
npm list

# Clean install
rm -rf node_modules package-lock.json
npm install
```

---

## Database Setup (Not Required)

This application is stateless and doesn't require a database. However, for future enhancements:

### PostgreSQL (Optional)

```bash
# macOS
brew install postgresql

# Windows
# Download from postgresql.org

# Linux
sudo apt-get install postgresql postgresql-contrib
```

---

## GPU Setup (Optional)

### NVIDIA CUDA

1. **Install CUDA Toolkit**
   - Download from nvidia.com
   - Version 11.8+ required for PyTorch 2.x

2. **Install cuDNN**
   - Download from nvidia.com
   - Extract to CUDA installation directory

3. **Verify Installation**
   ```bash
   nvidia-smi
   ```

4. **Update Dependencies**
   ```bash
   pip uninstall torch torchvision
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Apple Silicon (M1/M2)

```bash
# Install arm64 versions
pip uninstall torch
pip install torch::arm64
```

---

## Network Configuration

### Firewall Rules

Allow these ports through firewall:
- **3000**: Frontend (React)
- **8000**: Backend (FastAPI)
- **5432**: PostgreSQL (optional)

### CORS Configuration

For cross-origin requests, ensure `ALLOWED_ORIGINS` includes:
- Local: `http://localhost:3000`
- Production: `https://your-domain.com`

---

## Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed
- [ ] Virtual environment created
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Environment variables configured
- [ ] IDE configured with Python interpreter
- [ ] Webcam functional
- [ ] Port 3000 and 8000 available

---

## Troubleshooting

### Python Import Errors

```bash
# Verify venv is activated
which python  # macOS/Linux
where python  # Windows

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### npm Package Issues

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

```bash
# macOS/Linux
lsof -i :3000
lsof -i :8000

# Windows
netstat -ano | findstr :3000
```

### Camera Not Detected

```bash
# Check available cameras (Linux)
ls /dev/video*

# Check camera permissions (Linux)
sudo usermod -a -G video $USER
```

---

## Security Notes

1. **Never commit .env files** - Use .env.example instead
2. **Update dependencies regularly** - Run `npm audit` and `pip check`
3. **Use virtual environments** - Isolate project dependencies
4. **Enable HTTPS** - In production, use HTTPS for all connections
5. **Rotate API keys** - If adding authentication

---

## Performance Tips

1. Use SSD for faster npm/pip installs
2. Enable GPU for faster model inference
3. Use Docker for isolated environments
4. Monitor resource usage during development
5. Clear browser cache for React changes

---

For more information, see [README.md](./README.md)
