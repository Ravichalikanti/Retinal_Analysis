import torch
import torch.nn as nn

# ✅ Encoder matches training structure
class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, 4, 2, 1),
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.ReLU(),
            nn.Conv2d(128, 256, 4, 2, 1),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.encoder(x)

# ✅ CLASSIFIER (EXACT TRAINED STRUCTURE)
class RetinaClassifier(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()

        # nested encoder — matches keys encoder.encoder.xxx
        self.encoder = Encoder()

        # ✅ THIS EXACT MATCHES classifier.4.weight & classifier.4.bias
        self.classifier = nn.Sequential(
            nn.Flatten(),                                      # 0
            nn.Linear(256 * 28 * 28, 512),                     # 1
            nn.ReLU(),                                         # 2
            nn.Dropout(0.3),                                   # 3
            nn.Linear(512, num_classes)                        # 4  ✅ matches saved file
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.classifier(x)
        return x
