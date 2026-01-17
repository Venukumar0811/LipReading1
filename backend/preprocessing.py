import cv2
import numpy as np
from mediapipe.python.solutions import face_detection
import mediapipe as mp


class FaceAndLipDetector:
    """
    Detects face and extracts lip region from frames using MediaPipe.
    """

    def __init__(self):
        self.face_detection = face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_face(self, frame):
        """
        Detects face in the frame and returns bounding box.
        Returns: (x, y, w, h) or None if no face detected
        """
        h, w, c = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                return (x, y, width, height)
        return None

    def extract_mouth_region(self, frame, face_bbox):
        """
        Extracts mouth region from the face.
        Returns: mouth_region (96x96) or None
        """
        if face_bbox is None:
            return None

        x, y, w, h = face_bbox
        # Mouth region is roughly in lower half of face
        mouth_y = y + int(h * 0.5)
        mouth_height = int(h * 0.4)
        mouth_x = x + int(w * 0.1)
        mouth_width = int(w * 0.8)

        mouth_region = frame[mouth_y : mouth_y + mouth_height, mouth_x : mouth_x + mouth_width]

        if mouth_region.size == 0:
            return None

        # Resize to 96x96 for model input
        mouth_region = cv2.resize(mouth_region, (96, 96))
        return mouth_region

    def preprocess_frame(self, frame):
        """
        Full preprocessing pipeline: detect face, extract mouth, normalize.
        Returns: processed_mouth or None
        """
        face_bbox = self.detect_face(frame)
        if face_bbox is None:
            return None

        mouth_region = self.extract_mouth_region(frame, face_bbox)
        if mouth_region is None:
            return None

        # Normalize
        mouth_region = mouth_region.astype(np.float32) / 255.0
        return mouth_region
