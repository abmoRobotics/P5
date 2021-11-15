
from os import environ
import cv2
from PIL import Image
import numpy as np
from skimage.morphology import medial_axis, skeletonize
from skimage import data, measure
import matplotlib.pyplot as plt
from skimage.util import invert
import time
from fil_finder import FilFinder2D
from astropy.io import fits
import astropy.units as u
import pandas as pd
from IPython.display import display


def closing(img):
    kernel = np.ones((13,13),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

def skeletonization(img):
    skeleton = skeletonize(img)
    return skeleton

def find_length_of_skeletonization(img):
    #mask = img.data > 1
    fil = FilFinder2D(img)
    return fil
# Function for calculating the avergage width of a crack
def crack_width(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # create an empty black image
    drawing = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    # draw contours and hull points
    for i in range(len(contours)):
        print(cv2.contourArea(contours[i]))
        
        color_contours = (255,255,255) # green - color for contours
        # draw ith contour
        cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)

    return contours

# # Billede vi loader for at teste
def test_skeletonize():
    img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L') 
    img = np.array(img)
    (thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)


    contours = closing(blackAndWhiteImage)


    s1 = skeletonize(contours)


    fig, axes = plt.subplots(1,2, figsize=(8, 8), sharex=True, sharey=True)
    ax = axes.ravel()



    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_title('original')
    ax[0].axis('off')

    ax[1].imshow(s1, cmap=plt.cm.gray)
    ax[1].set_title('skeleton')
    ax[1].axis('off')

    fig.tight_layout()
    plt.show()


    # print(s1.shape)
    # binary = (s1*255).astype(np.uint8)
    # while 1:
    #     cv2.imshow("asdf",binary)
    #     cv2.waitKey(20)

def skeletonization_with_threshold(img):
    (thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)

    contours = closing(blackAndWhiteImage)
    skeleton = skeletonize(contours)



    return skeleton

def region_array(img):
    labels, num = measure.label(img,connectivity=2,return_num=True)

    region_arr =[]
    for i in range(0,num):
        region = np.where((labels[:]==i+1))
        if len(region[0]) > 1:
            region = list(zip(region[1], region[0]))
            region_arr.append(region)
    return region_arr

def convolve(image, kernel):
	image = (image).astype(np.uint8)
	# grab the spatial dimensions of the image, along with
	# the spatial dimensions of the kernel
	(iH, iW) = image.shape[:2]
	(kH, kW) = kernel.shape[:2]
	# allocate memory for the output image, taking care to
	# "pad" the borders of the input image so the spatial
	# size (i.e., width and height) are not reduced
	pad = (kW - 1) // 2
	image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
		cv2.BORDER_REPLICATE)
	output = np.zeros((iH, iW), dtype="float32")
    
    	# loop over the input image, "sliding" the kernel across
	# each (x, y)-coordinate from left-to-right and top to
	# bottom
	for y in np.arange(pad, iH + pad):
		for x in np.arange(pad, iW + pad):
			# extract the ROI of the image by extracting the
			# *center* region of the current (x, y)-coordinates
			# dimensions
			roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
			# perform the actual convolution by taking the
			# element-wise multiplicate between the ROI and
			# the kernel, then summing the matrix
			k = (roi * kernel).sum()
			# store the convolved value in the output (x,y)-
			# coordinate of the output image
			if k > 12:
			    output[y - pad, x - pad] = k

	return output
            

def find_branch(img):
    print(img.shape[0])
    print(img.shape[1])
    
    kernel = np.array( [[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])
    for y in range(1, img.shape[0]):
        sum = 0
        for x in range(1, img.shape[1]):
            pass
    
    return img

img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L') 
#img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160222_081102_1921_1.png").convert('L') 
kernel = np.array( [[1, 1, 1],
                    [1, 10, 1],
                    [1, 1, 1]])
img = np.array(img)
img = closing(img)
skeleton = skeletonization_with_threshold(img)
skeleton2 = convolve(skeleton, kernel)
#preds = (img2*255).astype(np.uint8)

preds = region_array(skeleton)




# if (i+2.x < i.x) and (i+1.x == i.x)
# 	arr.append(i+1)
# else
# 	arr.append(i)
        #print(pred[1]) 
# preds = (img2*255).astype(np.uint8)
#contours, hierarchy = cv2.findContours(preds,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#area = cv2.contourArea(contours)
#cv2.drawContours(preds,[contours[0]],0,(255,0,0),5)
# yx_cords= np.column_stack(np.where(preds > 0))

# a = measure.label(preds,connectivity=2)
# white=np.where((a[:]==1))



# print(white)
# r,l=cv2.connectedComponents(preds)
# # white=np.where((preds[:]==255))
# print(l)
# for k in yx_cords:
#     print(k)
#print(yx_cords[0][1][1])
# for k in preds:
#     print(k)
#print(preds[350,1])
# for point in contours[0]:
#     print(point)
#for idx, cnt in enumerate(contours):
#    cv2.drawContours(preds,[cnt],0,(255,0,0),5)
fig, axs = plt.subplots(1,2)
fig.suptitle('Vertically stacked subplots')
axs[0].imshow(skeleton)
axs[1].imshow(skeleton2)
# plt.imshow(skeleton)
# plt.imshow(skeleton2)
plt.axis('off')
plt.show()
