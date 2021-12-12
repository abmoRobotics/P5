
from utils.dataset import CrackDataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from model.model import UNET
import torch
import torchvision
from tqdm import tqdm
import numpy as np
import torch.nn as nn
from utils.utils import (load_model)
#from torchmetrics import IoU


# hyperparameters
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_HEIGHT = 360
IMAGE_WIDTH = 640
TEST_IMG_DIR = "data/test_images/"
TEST_MASK_DIR = "data/test_masks/"


def bm0(mask1, mask2):
    mask1_area = np.count_nonzero(mask1 == 1)       # I assume this is faster as mask1 == 1 is a bool array
    mask2_area = np.count_nonzero(mask2 == 1)
    intersection = np.count_nonzero( np.logical_and( mask1, mask2) )
    iou = intersection/(mask1_area+mask2_area-intersection)
    return iou

def f1_loss(y_true, y_pred, beta=1) -> np.float32:
    '''Calculate F1 score.
    
    The original implmentation is written by Michal Haltuf on Kaggle.
    
    Reference
    ---------
    - https://www.kaggle.com/rejpalcz/best-loss-function-for-f1-score-metric
    - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score
    - https://discuss.pytorch.org/t/calculating-precision-recall-and-f1-score-in-case-of-multi-label-classification/28265/6
    
    # '''
    # assert y_true.shape[1] == 1
    # assert y_pred.shape[1] == 1
        
    
    tp = (y_true * y_pred).sum()
    tn = ((1 - y_true) * (1 - y_pred)).sum()
    fp = ((1 - y_true) * y_pred).sum()
    fn = (y_true * (1 - y_pred)).sum()
    
    epsilon = 1e-7
    
    precision = tp / (tp + fp + epsilon)
    recall = tp / (tp + fn + epsilon)
    
    f1 = (1 + beta**2)* (precision*recall) / (beta**2 * precision + recall + epsilon)

    return f1 


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

    test_ds = CrackDataset(
        image_dir=TEST_IMG_DIR,
        mask_dir=TEST_MASK_DIR,
        transform=train_transform,
    )
    return test_ds

def check_accuracy(loader, model):
    loop = tqdm(loader)

    IoU = 0
    F1 = 0

    for batch_idx, (data, masks) in enumerate(loop):
        data = data.to(device=DEVICE)
        #print(data.shape)
        masks = masks.to(device=DEVICE)
        data = torch.unsqueeze(data,0)
        masks = torch.unsqueeze(masks,0)
        output = torch.sigmoid(model(data))

        output = torch.squeeze(output)
        masks = torch.squeeze(masks)
        preds = (output > 0.5).float()

        if ( 7 < batch_idx < 13):
            torchvision.utils.save_image(preds, f"tests/test_images/pred{batch_idx}.png")
            torchvision.utils.save_image(masks, f"tests/test_images/{batch_idx}.png")
            torchvision.utils.save_image(data, f"tests/test_images/original{batch_idx}.png")
        a = masks.cpu().detach().numpy()
        b = preds.cpu().detach().numpy()
        IoU += bm0(a,b)
        F1 += f1_loss(a,b)

    IoU = IoU / len(loader)
    F1 = F1 / len(loader)

    return IoU, F1


def main():
    test_loader = get_testDS()
    # loop = tqdm(test_loader)
    model = load_model("model/crack500v4.pth.tar", features=[64, 128, 256, 512])

    IoU, F1 = check_accuracy(test_loader, model)
    print(F1)
    print(IoU)


if __name__ == "__main__":
    main()