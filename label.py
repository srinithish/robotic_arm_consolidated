import numpy as np
import cv2
import localize
import os

def label_imgs(IMG_NAME_LIST, label):

    results = []

    for filename in IMG_NAME_LIST:

        print(filename)

        f = cv2.imread(filename)

        o = localize_label(f,label)
        
        
        baseName = os.path.basename(filename)
        
        
        i = localize.Img(baseName, o)

        results.append(i)

    print("Done!")

    return results


def localize_label(frame, label): ##IMG : String of file path
    ##crop values!
#    y1 = 0
#    y2 = 470
#    x1 = 143
#    x2 = 530
    y1 = 0
    y2 = 400
    x1 = 143
    x2 = 530
    rectangles = []
    objects = []

    ##black color detection range
    blackLower = np.array([0, 0, 0], dtype="uint8")
    blackUpper = np.array([10, 10, 10], dtype="uint8")
	#########


    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.imread(IMG, 0)

    frame = frame[y1:y2, x1:x2] ##crop that bitch

    ##BACKGROUND IMAGES REQURED################
    BgmImg1 = cv2.imread('BACKGROUND/EmptyTable_6.jpg', 0)
    BgmImg1 = BgmImg1[y1:y2, x1:x2]
    BgmImg2 = cv2.imread('BACKGROUND/EmptyTable_7.jpg', 0)
    BgmImg2 = BgmImg2[y1:y2, x1:x2]
    BgmImg3 = cv2.imread('BACKGROUND/EmptyTable_8.jpg', 0)
    BgmImg3 = BgmImg3[y1:y2, x1:x2]
    ###########################################

    BgmImg = np.mean(np.array([BgmImg1, BgmImg2, BgmImg3]), axis=0)

    ##trial code

    BgmImg = cv2.GaussianBlur(BgmImg, (21, 21), 0)
    ##end

    highlight = np.abs(frame.astype(np.int) - BgmImg.astype(np.int))

    ##threshold
    highlight[highlight > 20] = 255
    highlight[highlight < 20] = 0

    ##compatable with cv2 type
    highlight = highlight.astype(np.uint8)

    ##invert colors
    highlight = cv2.bitwise_not(highlight)

    ##back to RGB
    frame = cv2.cvtColor(highlight, cv2.COLOR_GRAY2RGB)

    cv2.imwrite("testing.jpg",frame)

    #plt.imsave('test.jpg',frame)

    for i in range(100):

        blue = cv2.inRange(frame, blackLower, blackUpper)

        # blue = cv2.GaussianBlur(blue, (3, 3), 0)

        (cnts, _) = cv2.findContours(blue.copy(), cv2.
                                        RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) > 0:

            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

            rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))

            cv2.drawContours(frame, [rect], -1, (255, 255, 255), 2)  ##WEIRD DONT REMOVE THIS

            p_rect = localize.parallel_to_img(rect)

            if localize.area(localize.return_ordered(p_rect)) > 200:

                if len(rectangles) == 0:

                    rectangles.append(p_rect)

                else:

                    rectangles = localize.replace_intercept_rects(rectangles, p_rect)

    t_rectangles = []

    for r in rectangles:

        t_rectangles.append(localize.transf(r,y1,x1))

        t_r = localize.return_ordered(localize.transf(r,y1,x1))  ##objects have global goordinates (no cropping coordinates)

        item = localize.Item(label, xmin=t_r[0], xmax=t_r[1], ymin=t_r[2], ymax=t_r[3])

        objects.append(item)

    return objects




if __name__ == '__main__':

    IMG_NAME_LIST = ['TEST/TestImgsAll_5.jpg','TEST/TestImgsAll_6.jpg','TEST/TestImgsAll_7.jpg']

    print(label_imgs(IMG_NAME_LIST, "apple"))

