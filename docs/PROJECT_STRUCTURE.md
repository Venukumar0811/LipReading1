# Project Structure Documentation

## Directory Overview

```
LipReading1/
├── frontend/                    # React.js web application
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── VideoContainer.js    # Video feed display
│   │   │   ├── VideoContainer.css
│   │   │   ├── SubtitleBar.js       # Real-time subtitles
│   │   │   ├── SubtitleBar.css
│   │   │   ├── ControlPanel.js      # Start/Stop buttons
│   │   │   ├── ControlPanel.css
│   │   │   ├── ErrorMessage.js      # Error notifications
│   │   │   └── ErrorMessage.css
│   │   ├── App.js              # Main application logic
│   │   ├── App.css             # Application styles
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # Node dependencies
│   ├── Dockerfile              # Docker image definition
│   ├── .dockerignore           # Docker ignore patterns
│   ├── .env.local              # Local environment variables
│   └── .gitignore             # Git ignore patterns
│
├── backend/                     # Python FastAPI server
│   ├── main.py                 # FastAPI application & endpoints
│   ├── model.py                # CNN-LSTM neural network
│   ├── preprocessing.py        # Face & lip detection
│   ├── frame_processor.py      # Frame utilities
│   ├── train.py               # Model training script
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-prod.txt   # Production dependencies
│   ├── .env                    # Environment variables
│   ├── .dockerignore           # Docker ignore patterns
│   └── app.yaml                # Google App Engine config
│
├── models/                      # Pre-trained model weights
│   └── lip_reading_model.pt    # Serialized model (58MB)
│
├── docs/                        # Documentation
│   └── RESEARCH.md             # Research paper & methodology
│
├── .github/
│   └── workflows/              # GitHub Actions CI/CD
│       └── config.yml
│
├── .vscode/
│   └── settings.json           # VS Code configuration
│
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Docker Compose orchestration
├── LICENSE                     # MIT License
├── README.md                   # Main documentation
├── GETTING_STARTED.md         # Quick start guide
├── RENDER_DEPLOYMENT.md       # Deployment instructions
├── start.sh                    # Start script (Linux/macOS)
├── start.bat                   # Start script (Windows)
├── start-docker.sh             # Docker start (Linux/macOS)
└── start-docker.bat            # Docker start (Windows)
```

## File Descriptions

### Frontend Files

| File | Purpose |
|------|---------|
| `App.js` | Main React component, state management, camera logic |
| `VideoContainer.js` | Video element display with loading indicator |
| `SubtitleBar.js` | Real-time subtitle display with confidence |
| `ControlPanel.js` | Start/Stop buttons and status badge |
| `ErrorMessage.js` | Error notification component |
| `index.js` | React DOM render entry point |
| `package.json` | NPM dependencies and scripts |

### Backend Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server and API endpoints |
| `model.py` | CNN-LSTM architecture definition |
| `preprocessing.py` | Face detection and lip extraction |
| `frame_processor.py` | Base64 encoding/decoding utilities |
| `train.py` | Model training and testing script |
| `requirements.txt` | Python package dependencies |

### Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `.env.example` | Template for environment variables |
| `.gitignore` | Files to exclude from git |
| `Dockerfile` | Docker image build instructions |
| `docker-compose.yml` | Multi-container orchestration |
| `.vscode/settings.json` | VS Code IDE settings |

---

## Module Descriptions

### Frontend Architecture

```
App.js (Main)
├── VideoContainer (Camera Feed)
├── SubtitleBar (Predictions)
├── ControlPanel (Start/Stop)
├── ErrorMessage (Notifications)
└── Hidden Canvas (Frame Capture)
```

### Backend Architecture

```
main.py (FastAPI)
├── /health (Health Check)
├── /api/process-frame (Frame Processing)
├── /api/reset (Reset Session)
├── /api/model-info (Model Details)
└── / (Root)

model.py
├── LipReadingCNNLSTM (Neural Network)
│   ├── CNN Layers (Feature Extraction)
│   ├── LSTM Layers (Sequence Modeling)
│   └── Output Layer (Classification)
└── LipReadingModel (Wrapper)

preprocessing.py
├── FaceAndLipDetector (Detection)
│   ├── detect_face()
│   ├── extract_mouth_region()
│   └── preprocess_frame()

frame_processor.py
├── FrameProcessor (Utilities)
│   ├── decode_base64_image()
│   ├── encode_image_to_base64()
│   └── normalize_frame()
```

---

## Data Flow

```
User Browser
    ↓
[Camera Feed via WebRTC]
    ↓
[React VideoContainer]
    ↓
[Canvas: Capture Frame]
    ↓
[Base64 Encode]
    ↓
[POST /api/process-frame]
    ↓ HTTP
FastAPI Backend
    ↓
[Decode Base64]
    ↓
[Face Detection (MediaPipe)]
    ↓
[Lip Region Extraction]
    ↓
[Frame Preprocessing]
    ↓
[Add to History Buffer]
    ↓
[CNN-LSTM Forward Pass]
    ↓
[Get Prediction & Confidence]
    ↓
[Return JSON Response]
    ↓ HTTP
React Frontend
    ↓
[SubtitleBar: Display Text]
    ↓
[ControlPanel: Update Status]
    ↓
[History Panel: Add Record]
```

---

## Key Design Decisions

1. **Functional Components**: Modern React with hooks for state management
2. **CORS Enabled**: Explicit origin allowlist for security
3. **Stateless Backend**: No sessions, pure request-response model
4. **Frame History Buffer**: Maintains last 10 frames for sequence prediction
5. **Async Processing**: Non-blocking API calls using Axios
6. **Error Handling**: Graceful degradation with user-friendly messages
7. **Container Orchestration**: Docker Compose for local development

---

For detailed information, see [README.md](./README.md)
