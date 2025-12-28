
import torch
import torch.nn as nn
import os

# Define the RawNet2Like model (simplified for demonstration)
# This class needs to be compatible enough for loading weights with strict=False
# and for processing audio features.
class RawNet2Like(nn.Module):
    def __init__(self, num_classes=1, input_length=16000 * 5): # Default input_length
        super().__init__()
        # A very simplified feature extractor. Actual RawNet2 is much more complex.
        # The key is to have *some* conv layers that might align with early layers in pre-trained model.
        self.features = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1) # Output a fixed size, 1
        )
        
        # If the input to FC after AdaptiveAvgPool1d(1) is always the number of channels (128 here)
        features_size = 128
        
        self.classifier = nn.Linear(features_size, num_classes)

    def forward(self, x):
        # x is expected as (batch_size, input_length) or (batch_size, 1, input_length)
        if x.dim() == 2:
            x = x.unsqueeze(1) # Add channel dimension (batch_size, 1, input_length)
        
        x = self.features(x)
        x = torch.flatten(x, 1) # Flatten for the linear layer
        x = self.classifier(x)
        return x

class AudioDeepfakeModel:
    def __init__(self, model_path, num_classes=1, input_length=16000 * 5, model_instance=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        if model_instance is not None:
            self.model = model_instance.to(self.device)
            print("Using provided model instance for AudioDeepfakeModel.")
            # If a model instance is provided, we don't try to load external weights into it by default.
            # The user is responsible for loading weights into their custom instance if needed.
        else:
            # Initialize the RawNet2Like model
            self.model = RawNet2Like(num_classes=num_classes, input_length=input_length).to(self.device)
            
            # Load weights if model_instance was not provided
            if os.path.exists(model_path):
                print(f"Loading audio model weights from {model_path}")
                checkpoint = torch.load(model_path, map_location=self.device)
                # The actual checkpoint might contain 'model_state_dict' or just state_dict
                if 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'], strict=False)
                else:
                    self.model.load_state_dict(checkpoint, strict=False)
                print("Audio model weights loaded (strict=False).")
            else:
                print(f"Warning: Audio model weights not found at {model_path}. Using uninitialized model.")
        
        self.model.eval() # Set model to evaluation mode

    def predict(self, audio_features):
        # audio_features is expected to be a torch tensor
        with torch.no_grad():
            audio_features = audio_features.to(self.device)
            output = self.model(audio_features)
            # Assuming output is logits for binary classification
            # Convert to probability (e.g., using sigmoid for binary)
            probability = torch.sigmoid(output).item()
            return probability
