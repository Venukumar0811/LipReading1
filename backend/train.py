from model import LipReadingModel
import torch
import numpy as np


def save_model_checkpoint():
    """Save a pretrained model checkpoint."""
    model = LipReadingModel(device="cpu")
    model.model.eval()
    
    # Save model state
    checkpoint_path = "lip_reading_model.pt"
    torch.save(model.model.state_dict(), checkpoint_path)
    print(f"Model saved to {checkpoint_path}")


def load_and_test_model():
    """Test loading and inference with the model."""
    model = LipReadingModel(
        model_path="lip_reading_model.pt",
        device="cpu"
    )
    
    # Create dummy input
    dummy_frame = np.random.randn(96, 96, 3).astype(np.float32)
    dummy_frames = np.repeat(np.expand_dims(dummy_frame, 0), 10, axis=0)
    
    # Test prediction
    text, confidence = model.predict_sequence(dummy_frames)
    print(f"Predicted text: {text}")
    print(f"Confidence: {confidence:.4f}")


if __name__ == "__main__":
    print("Saving model checkpoint...")
    save_model_checkpoint()
    print("\nTesting model inference...")
    load_and_test_model()
