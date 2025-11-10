import torch

# Load the wrong checkpoint
state = torch.load("encoder_only.pth", map_location="cpu")

new_state = {}

# Remove "encoder." prefix
for k, v in state.items():
    new_key = k.replace("encoder.", "")
    new_state[new_key] = v

# Save corrected checkpoint
torch.save(new_state, "encoder_only_fixed.pth")

print("✅ Fixed encoder saved as encoder_only_fixed.pth")
