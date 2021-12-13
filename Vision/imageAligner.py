import cv2
import numpy as np

from cv2 import cuda, threshold





def imageAlignerGPU(imgRef, imgOverlap):   
    MAX_FEATURES = 115000
    
    img1GPU = imgRef.copy()
    img2GPU = imgOverlap.copy()
    cuMat1 = cv2.cuda_GpuMat()
    cuMat2 = cv2.cuda_GpuMat()

    cuMat1.upload(img1GPU)
    cuMat2.upload(img2GPU)

    imgRef = cv2.cuda.cvtColor(cuMat1,cv2.COLOR_BGR2GRAY)
    imgOverlap = cv2.cuda.cvtColor(cuMat2,cv2.COLOR_BGR2GRAY)
    #img_ = imgOverlap.download()
    #img_1 = imgRef.download()
    #print(img_.shape)
    
    orb = cuda.ORB_create(MAX_FEATURES,edgeThreshold=31)
    orb.setBlurForDescriptor(True)
    print(orb.getBlurForDescriptor())

    # find the key points and descriptors with ORB
    kp1, des1 = orb.detectAndComputeAsync(imgRef,None)
    kp2, des2 = orb.detectAndComputeAsync(imgOverlap,None)

    match = cuda.DescriptorMatcher_createBFMatcher(cv2.NORM_HAMMING)
    matches_gpu = match.knnMatchAsync(des1,des2,k=2)


    good = []
    matches_cpu = []
    matches_cpu = match.knnMatchConvert(matches_gpu)

    for m,n in matches_cpu:
        if m.distance < 0.5*n.distance:
            good.append(m)

  
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    flags = 2)

    img3 = cv2.drawMatches(img1GPU, orb.convert(kp1), img2GPU,orb.convert(kp2),good,None,**draw_params)
   # cv2.imshow("original_image_drawMatches.jpg", img3)
    cv2.imwrite("GPU_original_image_drawMatches.jpg",img3)

    MIN_MATCH_COUNT = 5
    if len(good) > MIN_MATCH_COUNT:
        
        kp1_cpu = orb.convert(kp1)
        kp2_cpu = orb.convert(kp2)

        src_pts = np.float32([ kp1_cpu[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2_cpu[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
        
        
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        imgOverlap_cpu = imgOverlap.download()

        imgRef_cpu = imgRef.download()

        h,w = imgOverlap_cpu.shape

        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        dst = cv2.perspectiveTransform(pts, M)

        imgRef = cv2.polylines(imgRef_cpu,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        traveled = abs(np.int32(dst[0][0][1]))

        OverlapHeight = h - traveled

        return traveled, OverlapHeight
    else:
        print("Insufficient matches")
        return 0,0

def imageAlignerCPU(img1, img2):
    h,w = img1.shape

    #sift = cv2.xfeatures2d.sift_create()
    MAX_FEATURES = 5000
    sift = cv2.ORB_create(MAX_FEATURES)

    # find the key points and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # print("nu")
    # print(img1.dtype)
    # print(img2.dtype)
    match = cv2.BFMatcher()
    # print(des1)
    # print(kp1)
    # print(des2)
    # print(kp2)
    
    # print("---")
  
    #print(matches)
    good = []
    try:
        matches = match.knnMatch(des1,des2,k=2)

        for m,n in matches:
            if m.distance < 0.5 * n.distance:
                good.append(m)
    except:
        print("ERROR DESCRIPTORS NOT AVAILABLE")
        return h,0
            
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    #cv2.imshow("original_image_drawMatches.jpg", img3)
    cv2.imwrite("original_image_drawMatches.jpg",img3)
            
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, M)
        traveled = abs(np.int32(dst[0][0][1]))
        overlapHeight = h - traveled
        #print("Height image: ", h, " Traveled ", traveled, "Overlap height: ", overlapHeight)
        return traveled, overlapHeight
    else:
        print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))
        return h,0
if __name__ == "__main__":
    import time


    im1 = cv2.imread("test_data/image_aligner/p1.png")
    im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
   # im1 = cv2.resize(im1, (480,320),interpolation=cv2.INTER_AREA)
    #print(im1.dtype)
    im2 = cv2.imread("test_data/image_aligner/p2.png")

    im2 = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
  #  im2 = cv2.resize(im2, (480,320),interpolation=cv2.INTER_AREA)
    imageAlignerCPU(im1,im2)
    print(im2.shape)
    # for i in range(10):
    #     t1 = time.time()
        
    #     print(imageAlignerGPU(im1,im2))

    #     # for i in range (0,100):
    #     #     imageAlignerCPU(im1,im2)
    #     print((time.time()-t1))
