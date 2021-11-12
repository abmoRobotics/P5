from model.model import UNET
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
import numpy as np
import cv2
import torchvision
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2
from datetime import date, datetime
from utils.features import (closing, skeletonization)
import time

from utils.utils import load_model


# hyperparameters
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 384

#Transforms
detect_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )

# Load the trained model
model = load_model("model/crack500BrightnessAugmentation.pth.tar")

cap = cv2.VideoCapture(1)

# try to get first frame
if cap.isOpened():
    rval, frame = cap.read()
else: 
    rval = False

start_time = datetime.now()
frame_count = 1

while rval:
    start_time = time.time()
    rval, frame = cap.read()
    augmentented = detect_transform(image=frame)
    data = augmentented["image"].to(device=DEVICE)
    data = torch.unsqueeze(data,0)
    output = torch.sigmoid(model(data))
    output = torch.squeeze(output)
    preds = (output > 0.5).float()
    preds = closing(preds.cpu().numpy())
    s1 = time.time()
    preds = skeletonization(preds)
    s2 = time.time()
    print(s2-s1)
    preds = (preds*255).astype(np.uint8)
    s3 = time.time()
    print(s3-s2)
    cv2.imshow("preview", preds)
    cv2.imshow("normal", frame)
    key = cv2.waitKey(1)
    print("FPS: ", 1.0 / (time.time() - start_time))

# Close window
cv2.destroyWindow("frame")
# cv2.destroyWindow("preview")
cv2.destroyWindow("normal")
