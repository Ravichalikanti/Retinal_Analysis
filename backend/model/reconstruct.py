import sys
import json
import torch
import base64
import io
from PIL import Image
import numpy as np
from autoencoder import Autoencoder

device = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ FIXED ABSOLUTE PATH
MODEL_PATH = r"C:/Users/DELL/Videos/major_proj/backend/model/autoencoder_retina.pth"

image_path = sys.argv[1]

model = Autoencoder().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

img = Image.open(image_path).convert("RGB")
img = img.resize((224, 224))

img_np = np.array(img).astype("float32") / 255.0
img_np = np.transpose(img_np, (2, 0, 1))
img_tensor = torch.tensor(img_np).unsqueeze(0).to(device)

with torch.no_grad():
    reconstructed = model(img_tensor).cpu().squeeze().numpy()

reconstructed = np.transpose(reconstructed, (1, 2, 0))
reconstructed_img = Image.fromarray((reconstructed * 255).astype("uint8"))

def to_base64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

print(json.dumps({
    "original": to_base64(img),
    "reconstructed": to_base64(reconstructed_img)
}))
