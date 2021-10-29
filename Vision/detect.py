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

from utils.utils import load_model


# hyperparameters
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_HEIGHT = 320
IMAGE_WIDTH = 480

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
model = load_model("model/model1.pth.tar")

cap = cv2.VideoCapture(0)

# try to get first frame
if cap.isOpened():
    rval, frame = cap.read()
else: 
    rval = False

start_time = datetime.now()
frame_count = 1

while rval:
    rval, frame = cap.read()
    augmentented = detect_transform(image=frame)
    data = augmentented["image"].to(device=DEVICE)
    data = torch.unsqueeze(data,0)
    output = torch.sigmoid(model(data))
    output = torch.squeeze(output)
    preds = (output > 0.5).float()
   
    cv2.imshow("preview", preds.cpu().numpy())
    key = cv2.waitKey(20)
    

# Close window
cv2.destroyWindow("frame")

