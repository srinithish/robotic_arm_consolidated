import numpy as np
import time
import cv2
import os



class Img(object):
    def __init__(self, name, objects):
        self.name = name
        self.objects = objects

    def __repr__(self):
        return '{}: {}'.format(self.name, self.objects)


class Item(object):
    def __init__(self, label, xmin, xmax, ymin, ymax):
        self.label = label
        self.xmax = xmax
        self.xmin = xmin
        self.ymin = ymin
        self.ymax = ymax

    def __repr__(self):
        return '{}: xmin: {}, xmax: {}, ymin: {}, ymax: {}'.format(self.label, self.xmin,self.xmax, self.ymin,
                                                                   self.ymax)



def area(points):
    return (points[1] - points[0]) * (points[3] - points[2])


def parallel_to_img(points):

    point1x = points[0][0]
    point1y = points[0][1]

    point2x = points[1][0]
    point2y = points[1][1]

    point3x = points[2][0]
    point3y = points[2][1]

    point4x = points[3][0]
    point4y = points[3][1]

    min_x = min(point1x, point2x, point3x, point4x)
    max_x = max(point1x, point2x, point3x, point4x)

    min_y = min(point1y, point2y, point3y, point4y)
    max_y = max(point1y, point2y, point3y, point4y)

    newrect = np.array([[max_x, max_y], [min_x, max_y], [min_x, min_y], [max_x, min_y]])

    return newrect


def return_ordered(points):

    point1x = points[0][0]
    point1y = points[0][1]

    point2x = points[1][0]
    point2y = points[1][1]

    point3x = points[2][0]
    point3y = points[2][1]

    point4x = points[3][0]
    point4y = points[3][1]

    min_x = min(point1x, point2x, point3x, point4x)
    max_x = max(point1x, point2x, point3x, point4x)

    min_y = min(point1y, point2y, point3y, point4y)
    max_y = max(point1y, point2y, point3y, point4y)

    newrect = [min_x, max_x, min_y, max_y]

    return newrect


def transf(points, y1, x1):

    point1x = points[0][0] + x1
    point1y = points[0][1] + y1

    point2x = points[1][0] + x1
    point2y = points[1][1] + y1

    point3x = points[2][0] + x1
    point3y = points[2][1] + y1

    point4x = points[3][0] + x1
    point4y = points[3][1] + y1

    newrect = np.array([[point1x, point1y], [point2x, point2y], [point3x, point3y], [point4x, point4y]])

    return newrect


def intercept_area(a, b):
    ##this function looks for intersect bigger than 80% on either rectagle

    dx = min(a[1], b[1]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[2], b[2])

    if (dx >= 0) and (dy >= 0):

        i_area = dx * dy

        if i_area > area(a) * 0.7 or i_area > area(b) * 0.7:

            return True

        else:

            return False
    else:

        return False


def replace_intercept_rects(rectangles, rect):

    cnt = 0  ##intercet coutner: how to many times has the tested rectagle intersect

    o_rec = return_ordered(rect)

    for i in range(len(rectangles)):

        o_rectagle = return_ordered(rectangles[i])

        if intercept_area(o_rec, o_rectagle):
            ##rectangle has been found to intercept

            cnt += 1

            if area(o_rectagle) < area(o_rec):

                rectangles[i] = rect

    # if cnt==0 then there was no intercect
    if cnt == 0:

        rectangles.append(rect)

    return rectangles


def localize(frame): ##IMG : String of file path
    ##crop values!
#    y1 = 0
#    y2 = 470
#    x1 = 143
#    x2 = 530

    y1 = 100
    y2 = 400
    x1 = 150
    x2 = 530

    rectangles = []
    objects = []

    ##black color detection range
    blackLower = np.array([0, 0, 0], dtype="uint8")
    blackUpper = np.array([10, 10, 10], dtype="uint8")
	#########
    

    ##process image to grey and crop
    frame = frame[y1:y2, x1:x2] ##crop that bitch

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

        ( cnts, _) = cv2.findContours(blue.copy(), cv2.
                                        RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) > 0:

            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

            rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))

            cv2.drawContours(frame, [rect], -1, (255, 255, 255), 2)  ##WEIRD DONT REMOVE THIS

            p_rect = parallel_to_img(rect)

            if area(return_ordered(p_rect)) > 200:

                if len(rectangles) == 0:

                    rectangles.append(p_rect)

                else:

                    rectangles = replace_intercept_rects(rectangles, p_rect)
                    
    t_rectangles = []

    for r in rectangles:
        
        t_rectangles.append(transf(r,y1,x1))

        t_r = return_ordered(transf(r,y1,x1))  ##objects have global goordinates (no cropping coordinates)

        item = Item('unknown', xmin=t_r[0], xmax=t_r[1], ymin=t_r[2], ymax=t_r[3])

        objects.append(item)

    return objects, t_rectangles


if __name__ == '__main__':
###these are the cropped vals that work for our current set up
# ...lazy way..but we can built a table area detectorlater
    y1 = 0
    y2 = 470
    x1 = 143
    x2 = 530
    
    ##REPLACE IMAGE FOLDER
    IMG_FOLDER = "TEST"
    
    ##this below is a demostration

    for filename in os.listdir(IMG_FOLDER):

        if filename != ".DS_Store":  ##mac problem

            print(filename)

            f = cv2.imread(IMG_FOLDER + "/" + filename) ##AJUST ACCORDINGLY

            (o, rectangles) = localize(f) ##o are the objects you need Natish

            frame = cv2.imread(IMG_FOLDER + "/" + filename)

            for r in rectangles:

                cv2.drawContours(frame, [r], -1, (0, 255, 0), 2)

            cv2.imshow("Tracking", frame)

            if cv2.waitKey(1) and 0xFF == ord("q"):
                break

            time.sleep(3)

    cv2.destroyAllWindows()




