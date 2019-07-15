import numpy as np
import time
import cv2
import os
from sklearn.cluster import KMeans
from collections import Counter
from statistics import stdev
import warnings

'''
OKAY SO THE COLOR THING ISNT REALLY A GOOD IDEA.

WHAT YOU NEED TO DO IS BUILD A SIMPLE CLASSIFYER  

TO SAY YEST OR NO TO THE NEW ITEM 

'''


def crop_blob(img,blob_coordinates, box_length=5):
    '''

    :param img: image used to find blob
    :param blob_coordinates: blob coordinates
    :param box_length: lenth of 1 side of sqaure to be created around blob coordinates
    :return:
    '''

    x = int(blob_coordinates[0])

    y = int(blob_coordinates[1])

    xmin = x - int(box_length / 2)

    xmax = x + (box_length - int(box_length/2))

    ymin = y - int(box_length / 2)

    ymax = y + (box_length - int(box_length / 2))

    return img[ymin:ymax, xmin:xmax]


def localize_object_dominant_color(frame): ##IMG : String of file path
    ##crop values!
    y1 = 0
    y2 = 470
    x1 = 143
    x2 = 530

    frame = frame[y1:y2, x1:x2] ##crop that bitch

    ##KEEP ORIGINAL COLOR COPY
    original = frame.copy()
    original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)  ##WE WANT TO FIND HSV DOMINANT COLOR

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ##BACKGROUND IMAGES REQURED################
    BgmImg1 = cv2.imread('BACKGROUND/EmptyTable_6.jpg', 0)
    BgmImg1 = BgmImg1[y1:y2, x1:x2]
    BgmImg2 = cv2.imread('BACKGROUND/EmptyTable_7.jpg', 0)
    BgmImg2 = BgmImg2[y1:y2, x1:x2]
    BgmImg3 = cv2.imread('BACKGROUND/EmptyTable_8.jpg', 0)
    BgmImg3 = BgmImg3[y1:y2, x1:x2]
    ###########################################

    BgmImg = np.mean(np.array([BgmImg1, BgmImg2, BgmImg3]), axis=0)

    #~~~~~~~~~trial code

    BgmImg = cv2.GaussianBlur(BgmImg, (21, 21), 0)

    ##~~~~~~~~~~~~`end

    highlight = np.abs(frame.astype(np.int) - BgmImg.astype(np.int))

    ##threshold
    highlight[highlight > 20] = 255
    highlight[highlight < 20] = 0

    ##compatable with cv2 type
    highlight = highlight.astype(np.uint8)

    ##invert colors
    highlight = cv2.bitwise_not(highlight)

    ###BLOB DETECTOR
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 50

    # Filter by Circularity
    params.filterByCircularity = False

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')

    if int(ver[0]) < 3:

        detector = cv2.SimpleBlobDetector(params)
    else:

        detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(highlight)

    im_with_keypoints = cv2.drawKeypoints(original, keypoints, np.array([]), (0, 0, 255))

    keypoint = keypoints[0].pt

    '''
    #commented code here useful for debugging blob misstakes
    #Draw detected blobs as red circles.
    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    cv2.imshow("t",im_with_keypoints )
    cv2.waitKey(0)
    time.sleep(30)
    '''

    frame = crop_blob(original,keypoint,10) ##original already converted to HSV

    cv2.imwrite("im_with_keypoints.jpg",frame)


    d = get_dominant_color_in_HSV(frame)

    return d


def get_dominant_color_in_HSV(image, k=4, image_processing_size=None, background_color = [30, 5, 159]):
    """
    THIS FUNCTION FINDS DOMINANT COLOR IN GIVEN IMAGE FORMAT
    PLEASE ALWAYS USE HSV VALUES WHEN USING THIS FUNCTION
    (OPENCV DOEANT HAVE A QUCIK WAY TO CHECK IF HSV OR BGR, ETC.)


    takes an image as input
    returns the dominant color of the image as a list

    dominant color is found by running k means on the
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image;
    this resizing can be done with the image_processing_size param
    which takes a tuple of image dims as input

    get_dominant_color(my_image, k=4, image_processing_size = (28, 28))
    [56.2423442, 34.0834233, 70.1234123]
    """
    # resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size,
                           interpolation=cv2.INTER_AREA)

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster and assign labels to the pixels
    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(image)

    # count labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color = list(clt.cluster_centers_[label_counts.most_common(4)[0][0]])

    return dominant_color


def average(lst):
    return sum(lst) / len(lst)


def find_dominantHSV_4new_label(list_of_image_files):
    '''
    REMEMBER THE REQUIRMENT: ONLY FEED IMAGES WITH 1 TYPE OBJECT
    :param list_of_image_files: A LIST OF 3 IMAGE PATHS (OF SAME LABEL) TO FIND DOMINANT COLOR OF
    :return: DOMINANT COLOR AVERAGE
    '''
    if len(list_of_image_files)!=3:

        raise Exception("fuck you, give me three images")

    hue = []
    sat = []
    val = []

    for i in list_of_image_files:

        im = cv2.imread(i)

        d = localize_object_dominant_color(im)

        hue.append(d[0])
        sat.append(d[1])
        val.append(d[2])

    if stdev(hue) > 20 or stdev(sat) > 20 or stdev(val) > 20:

        warnings.warn("Warning: standard deviation of dominant is higher than usual")

    return [average(hue), average(sat), average(val)]


if __name__ == '__main__':

    ##below we test finding the dominat of color apples
    i1 = "/Users/juanhuerta/Desktop/trackcolor/single_objects/apple_143.jpg"
    i2 = "/Users/juanhuerta/Desktop/trackcolor/single_objects/apple_12.jpg"
    i3 = "/Users/juanhuerta/Desktop/trackcolor/single_objects/apple_128.jpg"

    IMAGES = [i1, i2, i3]

    d_color = find_dominantHSV_4new_label(IMAGES)

    print(d_color)

