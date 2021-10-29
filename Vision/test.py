from utils.dataset import CarvanaDataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from model.model import UNET
from utils.utils import check_accuracy
import torch
import torchvision
from tqdm import tqdm
import numpy as np
import torch.nn as nn
from utils.utils import (load_model)

# hyperparameters
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_HEIGHT = 320
IMAGE_WIDTH = 480
TEST_IMG_DIR = "data/TEST_images/"
TEST_MASK_DIR = "data/TEST_masks/"


def get_testDS():
    train_transform = A.Compose(
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

    test_ds = CarvanaDataset(
        image_dir=TEST_IMG_DIR,
        mask_dir=TEST_MASK_DIR,
        transform=train_transform,
    )
    return test_ds

def main():
    test_loader = get_testDS()

    loop = tqdm(test_loader)
    model = load_model("model/model1.pth.tar")


    # def check_accuracy(loader, model, device="cuda"):
    # num_correct = 0
    # num_pixels = 0
    # dice_score = 0
    # intersection = 0
    # union = 0
    # IoU = 0
    # union1 = 0
    # model.eval()

    # with torch.no_grad():
    #     for x, y in loader:
    #         x = x.to(device)
    #         y = y.to(device).unsqueeze(1)
    #         preds = torch.sigmoid(model(x))
    #         preds = (preds > 0.5).float()
    #         num_correct += (preds == y).sum()
    #         num_pixels += torch.numel(preds)
    #         intersection += ((preds * y).sum())
    #         union1 +=(preds + y).sum()
    #         union = union1-intersection
    #         IoU = intersection / union
    #         dice_score += (2 * (preds * y).sum()) / (
    #             (preds + y).sum() + 1e-8
    #         )

    # print(
    #     f"Got {num_correct}/{num_pixels} with acc {num_correct/num_pixels*100:.2f}"
    # )
    # print(f"Dice score: {dice_score/len(loader)}")
    # print(f"IoU score: {IoU}")
    #print(type(test_loader))
    num_correct = 0
    for batch_idx, (data, masks) in enumerate(loop):
        data = data.to(device=DEVICE)
        masks = data.to(device=DEVICE)
        data = torch.unsqueeze(data,0)
        masks = torch.unsqueeze(masks,0)

        #targets2 = torch.unsqueeze(targets,0)
        output = torch.sigmoid(model(data))
        output = torch.squeeze(output)
        masks = torch.squeeze(masks)
        preds = (output > 0.5).float()
        
        if batch_idx == 2:
            print(preds.shape)
            print(masks.shape)
            num_correct += (preds == masks).sum()
            print(f"numcorrects {num_correct}")
            print(320*480)
            # print(type(data))
            torchvision.utils.save_image(preds, f"test_images/pred{batch_idx}.png")
            torchvision.utils.save_image(masks, f"test_images/{batch_idx}.png")
            a = masks.cpu().detach().numpy()
            b = preds.cpu().detach().numpy()
            print(a.shape)
            print(b.shape)
            # row, col = a.shape
            # print(row)
            # print(col)

            # for i in range (0,320):
            #     for j in range (0,480):
            #         print(a[i][j])
            #         print(b[i][j])
            # for idx in enumerate(row):
            #     for idx2 in enumerate(col):
            #         print(a[idx][idx2])
           # a[0].len()
            # for x,y in a:
            #     print(x)
            #     print(y)
            # with torch.no_grad():
            #     for x, y in data:
            #         print(x)
            #         print(y)

        
        # im = cv2.imread("testDataset.png")
        # targets = targets.float().unsqueeze(1).to(device=DEVICE)

        # with torch.cuda.amp.autocast():
        #     predictions = model(targets)
        #     loss = loss_fn(predictions, targets)

    # for idx, item in enumerate(test_loader):
    #     print(test_loader[idx][0].shape)
    #     test_loader[idx][0] = torch.unsqueeze(test_loader[idx][0],0)
        

    # for e in test_loader:
    #     print(e)
    # print(test_loader[0][0])
    
    # check_accuracy(data, model)

if __name__ == "__main__":
    main()