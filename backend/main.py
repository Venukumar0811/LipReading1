import os
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from preprocessing import FaceAndLipDetector
from model import LipReadingModel
from frame_processor import FrameProcessor

# Initialize FastAPI app
app = FastAPI(
    title="Lip Reading API",
    description="Real-time lip reading using deep learning",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Get environment variable for additional origins
extra_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
origins.extend([origin.strip() for origin in extra_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
face_detector = FaceAndLipDetector()
device = os.getenv("DEVICE", "cpu")  # Default to CPU if not specified
lip_reading_model = LipReadingModel(device=device)  # Use "cuda" if GPU available

# Frame history for sequence prediction
frame_history = []
MAX_HISTORY = 10


# Request/Response models
class FrameRequest(BaseModel):
    frame: str  # Base64 encoded image


class PredictionResponse(BaseModel):
    text: str
    confidence: float
    frame_info: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    model: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model="CNN-LSTM Lip Reading Model",
        version="1.0.0",
    )


@app.post("/api/process-frame", response_model=PredictionResponse)
async def process_frame(request: FrameRequest):
    """
    Process a single video frame and return lip reading prediction.

    Request body:
    - frame: Base64 encoded image (JPEG)

    Response:
    - text: Predicted spoken word/phrase
    - confidence: Confidence score (0.0-1.0)
    - frame_info: Frame metadata
    """
    try:
        # Decode frame
        frame = FrameProcessor.decode_base64_image(request.frame)
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid frame data")

        frame_info = FrameProcessor.get_frame_info(frame)

        # Preprocess frame
        mouth_region = face_detector.preprocess_frame(frame)
        if mouth_region is None:
            return PredictionResponse(
                text="No face detected",
                confidence=0.0,
                frame_info=frame_info,
            )

        # Add to history
        frame_history.append(mouth_region)
        if len(frame_history) > MAX_HISTORY:
            frame_history.pop(0)

        # Predict
        if len(frame_history) >= 5:
            # Use sequence prediction
            frames_array = np.array(frame_history)
            predicted_text, confidence = lip_reading_model.predict_sequence(
                frames_array
            )
        else:
            # Use single frame prediction
            mouth_expanded = np.expand_dims(mouth_region, 0)
            predicted_text, confidence = lip_reading_model.predict(mouth_expanded)

        return PredictionResponse(
            text=predicted_text,
            confidence=confidence,
            frame_info=frame_info,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reset")
async def reset_session():
    """Reset frame history for a new prediction session."""
    global frame_history
    frame_history.clear()
    return {"status": "success", "message": "Frame history cleared"}


@app.get("/api/model-info")
async def get_model_info():
    """Get information about the loaded model."""
    return {
        "model_type": "CNN-LSTM",
        "input_shape": (96, 96, 3),
        "num_classes": 500,
        "vocabulary_size": len(lip_reading_model.vocabulary),
        "device": lip_reading_model.device,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Lip Reading API",
        "documentation": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level=log_level,
    )
