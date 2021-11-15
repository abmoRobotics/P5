
from os import environ
import cv2
from PIL import Image
import numpy as np
from skimage.morphology import medial_axis, skeletonize
from skimage import data, measure
import matplotlib.pyplot as plt
from skimage.util import invert
import time
import networkx as nx
from sklearn.neighbors import NearestNeighbors

#from ..path_planning import frame

def closing(img):
    kernel = np.ones((13,13),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

def skeletonization(img):
    skeleton = skeletonize(img)
    return skeleton

def find_length_of_skeletonization(img):
    pass

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

def find_branches(image, preds):
    kernel = np.array( [[1, 1, 1],
                    [1, 10, 1],
                    [1, 1, 1]])
    image = (image).astype(np.uint8)
	# grab the spatial dimensions of the image, along with
	# the spatial dimensions of the kernel
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]
	# allocate memory for the output image, taking care to
	# "pad" the borders of the input image so the spatial
	# size (i.e., width and height) are not reduced
    pad = (kW - 1) // 2
    output = image.copy()
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
        cv2.BORDER_REPLICATE)

    
    for point in preds:
        x = point[0]+pad
        y = point[1]+pad
        roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
        k = (roi * kernel).sum()
        if k > 12:
                output[y - pad, x - pad] = 0
        else: 
            output[y - pad, x - pad] = 1 

    return output
            
def sort_branch(regions):
    crack_cords = []
    for region in regions:
        points = region
        clf = NearestNeighbors(n_neighbors=2,algorithm='auto').fit(points)
        G = clf.kneighbors_graph()

    

        T = nx.from_scipy_sparse_matrix(G)

        order = list(nx.dfs_preorder_nodes(T, 0))
        #print(region)
        sorted_crack = [list(region[i]) for i in order]
        #region = region[order]
        crack_cords.append(sorted_crack)

    return crack_cords

# Input must be binary
def process_image(img):
    # Get skeleton
    skeleton = skeletonize(img) # 12 ms

    # Extract array with pixels from skeleton
    skeleton_points = np.where(skeleton[:]==1) # 1 ms

    # Convert to (x, y)
    skeleton_points = list(zip(skeleton_points[1], skeleton_points[0])) # 0 ms

    # Find branches
    skeleton_branches = find_branches(skeleton, skeleton_points) # 5 ms

    # Find regions
    regions = region_array(skeleton_branches) # 3 ms 

    # Sort regions WAITING FOR JESPER
    sorted_cracks = sort_branch(regions) # 9 ms

    return sorted_cracks

if __name__ == "__main__":    
    img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L') 
    #img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160222_081102_1921_1.png").convert('L') 
    img = np.array(img)
    (thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    binary_image = closing(blackAndWhiteImage)
    t1 = time.time()
    sorted_cracks = process_image(binary_image)
    print(time.time()-t1)
    print(sorted_cracks[0])
    # # Get skeleton
    # skeleton = skeletonization_with_threshold(img)

    # # Extract array with pixels from skeleton
    # skeleton_points = np.where(skeleton[:]==1)

    # # Convert to (x, y)
    # skeleton_points = list(zip(skeleton_points[1], skeleton_points[0]))

    # # Find branches
    # skeleton_branches = find_branches(skeleton, skeleton_points)

    # # Find regions
    # regions = region_array(skeleton_branches)

    # # Sort regions WAITING FOR JESPER
    # sorted_cracks = sort_branch(regions)


    # fig, axs = plt.subplots(1,2)
    # fig.suptitle('Vertically stacked subplots')
    # axs[0].imshow(skeleton)
    # axs[1].imshow(skeleton_branches)
    # # plt.imshow(skeleton)
    # # plt.imshow(skeleton2)
    # plt.axis('off')
    # plt.show()
