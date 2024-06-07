#
# CSCI3290 Computational Imaging and Vision *
# --- Declaration --- *
# I declare that the assignment here submitted is original except for source
# material explicitly acknowledged. I also acknowledge that I am aware of
# University policy and regulations on honesty in academic work, and of the
# disciplinary guidelines and procedures applicable to breaches of such policy
# and regulations, as contained in the website
# http://www.cuhk.edu.hk/policy/academichonesty/ *
# Assignment 1
# Name : Wong Wai Chun
# Student ID : 1155173231@link.cuhk.edu.hk
# Email Addr : 1155173231@link.cuhk.edu.hk
#

import cv2
import numpy as np
import argparse


def extract_and_match_feature(img_1, img_2, ratio_test=0.7):
    """
    1/  extract SIFT feature from image 1 and image 2,
    2/  use a bruteforce search to find pairs of matched features:
        for each feature point in img_1, find its best matched feature point in img_2
    3/ apply ratio test to select the set of robust matched points

    :param img_1: input image 1
    :param img_2: input image 2
    :param ratio_test: ratio for the robustness test
    :return list_pairs_matched_keypoints: a list of pairs of matched points: [[[p1x,p1y],[p2x,p2y]]]
    """
    list_pairs_matched_keypoints = []

    # to be completed ....
    sift = cv2.SIFT_create()

    keypoints1, descriptors1 = sift.detectAndCompute(img_1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img_2, None)
    print(f"Keypoints in Image 1: {len(keypoints1)}, Image 2: {len(keypoints2)}")
    
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    
    good_matches = [m for m, n in matches if m.distance < ratio_test * n.distance]
    print(f"Good matches found: {len(good_matches)}")
    
    list_pairs_matched_keypoints = [[[keypoints1[m.queryIdx].pt[0], keypoints1[m.queryIdx].pt[1]], 
                                     [keypoints2[m.trainIdx].pt[0], keypoints2[m.trainIdx].pt[1]]] 
                                    for m in good_matches]
    
    return list_pairs_matched_keypoints


def find_homography_ransac(list_pairs_matched_keypoints,
                           threshold_ratio_inliers=0.85,
                           threshold_reprojection_error=3,
                           max_num_trial=1000):
    """
    Apply RANSAC algorithm to find a homography transformation matrix that align 2 sets of feature points,
    transform the second set of feature point to the first (e.g. warp image 2 to image 1)

    :param list_pairs_matched_keypoints: a list of pairs of matched points: [[[p1x,p1y],[p2x,p2y]],...]
    :param threshold_ratio_inliers: threshold on the ratio of inliers over the total number of samples,
                                    accept the estimated homography if ratio is higher than the threshold
    :param threshold_reprojection_error: threshold of reprojection error (measured as euclidean distance, in pixels)
                                            to determine whether a sample is inlier or outlier
    :param max_num_trial: the maximum number of trials to take sample and do testing to find the best homography matrix
    :return best_H: the best found homography matrix
    """
    best_H = None

    # to be completed ...
    src_pts = np.float32([pair[0] for pair in list_pairs_matched_keypoints]).reshape(-1, 1, 2)
    dst_pts = np.float32([pair[1] for pair in list_pairs_matched_keypoints]).reshape(-1, 1, 2)
    # Use OpenCV's findHomography function with RANSAC
    best_H, mask = cv2.findHomography(dst_pts,src_pts, cv2.RANSAC, threshold_reprojection_error, maxIters=max_num_trial, confidence=threshold_ratio_inliers)



    return best_H




def warp_blend_image(img_1, H, img_2):
    """
    1/  warp image img_2 using the homography H to align it with image img_1
        (using inverse warping and bilinear resampling)
    2/  stitch image img_2 to image img_1 and apply average blending to blend the 2 images into a single img_panorama image

    :param img_1:  the original first image
    :param H: estimated homography
    :param img_2:the original second image
    :return img_panorama: resulting img_panorama image
    """
    img_panorama = None

    # to be completed ...
    h1, w1 = img_1.shape[:2]
    h2, w2 = img_2.shape[:2]

    corners1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
    corners2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
    warped_corners2 = cv2.perspectiveTransform(corners2, H)

    corners = np.concatenate((corners1, warped_corners2), axis=0)
    [xmin, ymin] = np.int32(corners.min(axis=0).ravel() - 0.5)
    [xmax, ymax] = np.int32(corners.max(axis=0).ravel() + 0.5)

    t = [-xmin, -ymin]
    Ht = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])

    warped_img2 = cv2.warpPerspective(img_2, Ht @ H, (xmax - xmin, ymax - ymin))
    
    

    warped_img2[t[1]:h1 + t[1], t[0]:w1 + t[0]] = img_1  
    

    img_panorama = warped_img2


    return img_panorama
    






def stitch_images(img_1, img_2):
    """
    :param img_1: input image 1 is the reference image. We will not warp this image
    :param img_2: We warp this image to align and stich it to the image 1
    :return img_panorama: the resulting stiched image
    """
    print('==================================================================================')
    print('===== stitch two images to generate one img_panorama image =====')
    print('==================================================================================')

    # ===== extract and match features from image 1 and image 2
    list_pairs_matched_keypoints = extract_and_match_feature(img_1=img_1, img_2=img_2, ratio_test=0.7)

    # ===== use RANSAC algorithm to find homography to warp image 2 to align it to image 1
    H = find_homography_ransac(list_pairs_matched_keypoints, threshold_ratio_inliers=0.85,
                               threshold_reprojection_error=3, max_num_trial=1000)

    # ===== warp image 2, blend it with image 1 using average blending to produce the resulting img_panorama image
    img_panorama = warp_blend_image(img_1=img_1, H=H, img_2=img_2)

    return img_panorama


if __name__ == "__main__":
    print('==================================================================================')
    print('CSCI3290, Spring 2024, Assignment 1: Image Stitching')
    print('==================================================================================')

    parser = argparse.ArgumentParser(description='Image Stitching')
    parser.add_argument('--im1', type=str, default='test_images/Rainier1.png',
                        help='path of the first input image')
    parser.add_argument('--im2', type=str, default='test_images/Rainier2.png',
                        help='path of the second input image')
    parser.add_argument('--output', type=str, default='Rainier.png',
                        help='the path of the output image')
    args = parser.parse_args()

    # ===== read 2 input images
    img_1 = cv2.imread(args.im1)
    img_2 = cv2.imread(args.im2)

    # ===== create a img_panorama image
    img_panorama = stitch_images(img_1=img_1, img_2=img_2)

    # ===== save img_panorama image
    cv2.imwrite(filename=args.output, img=img_panorama.clip(0.0, 255.0).astype(np.uint8))
