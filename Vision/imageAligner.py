import cv2
import numpy as np

def imageAligner(img1, img2):

    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    #sift = cv2.xfeatures2d.sift_create()
    MAX_FEATURES = 100
    sift = cv2.ORB_create(MAX_FEATURES)

    # find the key points and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    #FLANN_INDEX_KDTREE = 0
    #index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    #search_params = dict(checks = 50)
    #match = cv2.FlannBasedMatcher(index_params, search_params)
    match = cv2.BFMatcher()
    matches = match.knnMatch(des1,des2,k=2)


    good = []
    for m,n in matches:
        if m.distance < 0.03*n.distance:
            good.append(m)


    # draw_params = dict(matchColor = (0,255,0), # draw matches in green color
    #                 singlePointColor = None,
    #                 flags = 2)

    #img3 = cv2.drawMatches(img_,kp1,img,kp2,good,None,**draw_params)

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, M)
        #img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
        traveled = abs(np.int32(dst[0][0][1]))
        overlapHeight = h - traveled
        #print("Traveled " , traveled, " pixels with ", overlapHeight, " overlap.")
        return traveled, overlapHeight
    else:
        print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))
        return 0,0