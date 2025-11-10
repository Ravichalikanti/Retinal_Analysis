import torch
from autoencoder import Autoencoder

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the full autoencoder
model = Autoencoder().to(device)
model.load_state_dict(torch.load("autoencoder_retina.pth", map_location=device))

# Extract only encoder weights
encoder_state = model.encoder.state_dict()

# Save encoder weights
torch.save(encoder_state, "encoder_only.pth")

print("✅ encoder_only.pth created successfully!")
