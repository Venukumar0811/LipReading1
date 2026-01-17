import torch
import torch.nn as nn
import numpy as np
from typing import List, Tuple


class LipReadingCNNLSTM(nn.Module):
    """
    Combined CNN-LSTM architecture for lip reading.
    Processes video frames to predict spoken words.
    """

    def __init__(
        self,
        num_classes: int = 500,
        lstm_hidden: int = 256,
        num_lstm_layers: int = 2,
    ):
        super(LipReadingCNNLSTM, self).__init__()
        self.num_classes = num_classes

        # CNN for feature extraction (ResNet-based)
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # Additional convolutional layers
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1)
        self.bn4 = nn.BatchNorm2d(512)

        # LSTM layers for sequence modeling
        self.lstm = nn.LSTM(
            input_size=512,
            hidden_size=lstm_hidden,
            num_layers=num_lstm_layers,
            batch_first=True,
            bidirectional=True,
        )

        # Output layer
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(lstm_hidden * 2, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        Input shape: (batch_size, seq_len, 3, 96, 96)
        Output shape: (batch_size, seq_len, num_classes)
        """
        batch_size, seq_len, c, h, w = x.size()
        x = x.view(batch_size * seq_len, c, h, w)

        # CNN feature extraction
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu(x)

        # Global average pooling
        x = torch.nn.functional.adaptive_avg_pool2d(x, 1)
        x = x.view(batch_size * seq_len, -1)

        # Reshape for LSTM
        x = x.view(batch_size, seq_len, -1)

        # LSTM sequence modeling
        lstm_out, _ = self.lstm(x)
        x = self.dropout(lstm_out)

        # Output layer
        x = self.fc(x)
        return x


class LipReadingModel:
    """
    Wrapper for the lip reading model with prediction utilities.
    """

    def __init__(self, model_path: str = None, device: str = "cpu"):
        self.device = device
        self.model = LipReadingCNNLSTM(num_classes=500)

        if model_path:
            self.load_weights(model_path)

        self.model = self.model.to(device)
        self.model.eval()

        # Sample vocabulary (in production, use actual vocabulary)
        self.vocabulary = self._load_vocabulary()

    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary for decoding predictions."""
        # Extended common vocabulary for lip reading
        vocab = [
            "hello", "world", "how", "are", "you", "fine", "thanks", "good",
            "morning", "afternoon", "evening", "goodbye", "see", "you", "later",
            "please", "thank", "you", "yes", "no", "maybe", "understand",
            "love", "hate", "like", "help", "need", "want", "think", "know",
            "tell", "give", "take", "come", "go", "stay", "leave", "wait",
            "work", "play", "eat", "drink", "sleep", "wake", "run", "walk",
            "talk", "listen", "read", "write", "watch", "look", "see", "hear",
            "feel", "touch", "laugh", "cry", "smile", "frown", "happy", "sad",
            "angry", "scared", "tired", "excited", "ready", "able", "open",
            "close", "start", "stop", "continue", "break", "rest", "peace",
            "quiet", "loud", "fast", "slow", "big", "small", "hot", "cold",
            "easy", "hard", "light", "dark", "bright", "clear", "beautiful",
            "ugly", "right", "wrong", "correct", "incorrect", "true", "false",
            "real", "fake", "new", "old", "young", "aged", "fresh", "stale",
            "clean", "dirty", "wet", "dry", "soft", "hard", "smooth", "rough",
            "safe", "dangerous", "strong", "weak", "deep", "shallow", "wide",
            "narrow", "long", "short", "tall", "short", "thick", "thin", "full",
            "empty", "rich", "poor", "expensive", "cheap", "free", "busy", "idle",
            "alone", "together", "inside", "outside", "above", "below", "before",
            "after", "early", "late", "always", "never", "sometimes", "often",
            "rarely", "forever", "temporary", "permanent", "possible", "impossible",
            "likely", "unlikely", "certain", "uncertain", "confident", "doubtful"
        ]
        # Pad to 500 classes
        while len(vocab) < 500:
            vocab.append(f"word_{len(vocab)}")
        return vocab[:500]

    def load_weights(self, model_path: str):
        """Load pre-trained weights."""
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
        except Exception as e:
            print(f"Warning: Could not load weights from {model_path}: {e}")
            print("Using random initialization instead.")

    def predict(self, frames: np.ndarray) -> Tuple[str, float]:
        """
        Predict text from mouth regions.
        Input: frames shape (seq_len, 96, 96, 3)
        Output: (predicted_text, confidence)
        """
        if len(frames) == 0:
            return "", 0.0

        # Ensure correct shape
        if len(frames.shape) == 3:  # Single frame
            frames = np.expand_dims(frames, 0)

        # Convert to tensor
        frames_tensor = torch.from_numpy(frames).permute(0, 3, 1, 2).unsqueeze(0)
        frames_tensor = frames_tensor.to(self.device).float()

        with torch.no_grad():
            outputs = self.model(frames_tensor)
            # outputs shape: (1, seq_len, 500)
            predictions = torch.argmax(outputs, dim=2)
            confidences = torch.nn.functional.softmax(outputs, dim=2)

        # Get most confident prediction
        pred_idx = predictions[0, -1].item()
        confidence = confidences[0, -1, pred_idx].item()

        predicted_text = self.vocabulary[pred_idx] if pred_idx < len(self.vocabulary) else "unknown"

        return predicted_text, float(confidence)

    def predict_sequence(self, frames: np.ndarray) -> Tuple[str, float]:
        """
        Predict complete sequence of text from frames.
        """
        if len(frames) < 5:
            return "", 0.0

        frames_tensor = torch.from_numpy(frames).permute(0, 3, 1, 2).unsqueeze(0)
        frames_tensor = frames_tensor.to(self.device).float()

        with torch.no_grad():
            outputs = self.model(frames_tensor)
            predictions = torch.argmax(outputs, dim=2)
            confidences = torch.nn.functional.softmax(outputs, dim=2)

        # Decode sequence
        text_sequence = []
        confidence_scores = []

        for i in range(predictions.shape[1]):
            pred_idx = predictions[0, i].item()
            conf = confidences[0, i, pred_idx].item()
            if conf > 0.3:  # Only add high-confidence predictions
                text = self.vocabulary[pred_idx] if pred_idx < len(self.vocabulary) else "unknown"
                text_sequence.append(text)
                confidence_scores.append(conf)

        predicted_text = " ".join(text_sequence) if text_sequence else "unclear"
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.0

        return predicted_text, float(avg_confidence)
