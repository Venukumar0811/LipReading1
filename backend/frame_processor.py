import cv2
import base64
import numpy as np
from typing import Tuple


class FrameProcessor:
    """Utility class for processing video frames from frontend."""

    @staticmethod
    def decode_base64_image(image_data: str) -> np.ndarray:
        """
        Decode base64 image data to OpenCV format.
        Expects data URL format: 'data:image/jpeg;base64,...'
        """
        if "," in image_data:
            image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame

    @staticmethod
    def encode_image_to_base64(frame: np.ndarray) -> str:
        """Encode OpenCV frame to base64 string."""
        _, buffer = cv2.imencode(".jpg", frame)
        base64_str = base64.b64encode(buffer).decode("utf-8")
        return f"data:image/jpeg;base64,{base64_str}"

    @staticmethod
    def resize_frame(frame: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Resize frame to target size."""
        return cv2.resize(frame, target_size)

    @staticmethod
    def normalize_frame(frame: np.ndarray) -> np.ndarray:
        """Normalize frame to [0, 1] range."""
        return frame.astype(np.float32) / 255.0

    @staticmethod
    def get_frame_info(frame: np.ndarray) -> dict:
        """Get frame metadata."""
        h, w = frame.shape[:2]
        return {
            "height": h,
            "width": w,
            "channels": frame.shape[2] if len(frame.shape) == 3 else 1,
        }
