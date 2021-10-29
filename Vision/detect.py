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

from utils import load_model


# Måske nødvendigt
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Using device: ", device)

# Load the trained model
model = load_model("model1.pth.tar")


# Open window to visualize the segmentation
cv2.namedWindow("Real Feed")
cv2.namedWindow("Segmented Feed")
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
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_img = np.asarray(
        cv2.resize(rgb_image, (360, 480)))
    channel_first_img = np.transpose(resized_img, (2, 0, 1))
    img_added_axis = np.expand_dims(channel_first_img, axis=0)
    input_tensor = torch.from_numpy(img_added_axis).float()
    # input_tensor.to(device=device)
    input_tensor = input_tensor.cuda()
    preds = model(input_tensor)
    prediction = preds[0].cpu().detach().numpy()
    prediction = np.transpose(prediction, (1, 2, 0))

    prediction = np.uint8((prediction > 0.7) * 255)
    cv2.imshow("preview", prediction)
    cv2.imshow("normal", frame)
    key = cv2.waitKey(20)
    if key == 27:
        break
    if frame_count % 30 == 0:
        print("Frame Per second: {} fps.".format(
            (datetime.now() - start_time) / frame_count))
    frame_count = frame_count + 1

# Close window
cv2.destroyWindow("preview")
cv2.destroyWindow("normal")
