import sys
import json
import torch
import base64
import io
from PIL import Image
import numpy as np
from retina_classifier import RetinaClassifier
from autoencoder import Autoencoder   # reconstruction
import torch.nn.functional as F
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

IMAGE_PATH = sys.argv[1]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUTOENCODER_PATH = os.path.join(BASE_DIR, "autoencoder_retina.pth")
CLASSIFIER_PATH = os.path.join(BASE_DIR, "retina_classifier.pth")
ENCODER_PATH = os.path.join(BASE_DIR, "encoder_only.pth")


CLASSES = ["No DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]

DESCRIPTIONS = {
    "No DR": "Healthy retina with no signs of diabetic retinopathy.",
    "Mild DR": "Early signs of diabetic retinopathy. Mild microaneurysms present.",
    "Moderate DR": "More visible abnormalities. Requires medical consultation.",
    "Severe DR": "Serious damage. Immediate ophthalmology care needed.",
    "Proliferative DR": "Advanced stage. New abnormal blood vessels. High risk of vision loss."
}

# ✅ Load Image
img = Image.open(IMAGE_PATH).convert("RGB")
img = img.resize((224, 224))

img_np = np.array(img).astype("float32") / 255.0
img_np = np.transpose(img_np, (2, 0, 1))
img_tensor = torch.tensor(img_np).unsqueeze(0).to(device)

# ✅ Load Autoencoder
auto = Autoencoder().to(device)
auto.load_state_dict(torch.load(AUTOENCODER_PATH, map_location=device))
auto.eval()

with torch.no_grad():
    reconstructed_tensor = auto(img_tensor)
    reconstructed_np = reconstructed_tensor.squeeze().cpu().numpy()

reconstructed_np = np.transpose(reconstructed_np, (1, 2, 0))
reconstructed_img = Image.fromarray((reconstructed_np * 255).astype("uint8"))

# ✅ Convert PIL → Base64
def to_base64(pil_img):
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    return base64.b64encode(buff.getvalue()).decode()

original_b64 = to_base64(img)
reconstructed_b64 = to_base64(reconstructed_img)

# ✅ CLASSIFICATION
model = RetinaClassifier().to(device)
model.load_state_dict(torch.load(CLASSIFIER_PATH, map_location=device))
model.eval()


with torch.no_grad():
    out = model(img_tensor)
    prob = torch.softmax(out, dim=1)[0]
    pred_class = CLASSES[int(torch.argmax(prob))]
    confidence = float(prob.max()) * 100

result = {
    "original": original_b64,
    "reconstructed": reconstructed_b64,
    "stage": pred_class,
    "description": DESCRIPTIONS[pred_class],
    "confidence": confidence
}

import json
print(json.dumps(result))

