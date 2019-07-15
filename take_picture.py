import numpy as np
import time
import cv2
import os
import localize


def take_picture(image2test):

    global image2test_old

    y1 = 0
    y2 = 470
    x1 = 143
    x2 = 530

    (l_o, l_r) = localize.localize(image2test)

    if image2test_old.size != 0: ##check if unmoved

        (l_o2, l_r2) = localize.localize(image2test_old) ##should only have one object

        if len(l_o) > 1:

            return False

        else:

            for o in l_o:

                if np.abs(o.xmin - l_o2[0].xmin) < 5 or np.abs(o.xmax - l_o2[0].xmax) < 5 or np.abs(o.ymin - l_o2[0].ymin) < 5 or np.abs(o.ymax - l_o2[0].ymax) < 5:
                    ##if we entered here then onject has not moved more than 5 pixels from previous picture snap

                    return False

                else:
                    ##objct has moved so
                    break

    ##image is either moved from prevous possition or first run

    if len(l_o) > 1:

        return False

    else:

        for o in l_o:

            if o.xmin  < x1 or o.xmax  > x2 or o.ymin  < y1 or o.ymax  > y2:

                ##hand is probaby in the frame

                return False

            else:

                ##ready to take a picture

                image2test_old = image2test

                return True

image2test_old = np.array([])

##run a demo with images on TEST folder
if __name__ == '__main__':

    ##REPLACE IMAGE FOLDER
    IMG_FOLDER = "TEST"
    
    ##this below is a demostration

    for filename in os.listdir(IMG_FOLDER):

        if filename != ".DS_Store":  ##mac problem

            print(filename)

            f = cv2.imread(IMG_FOLDER + "/" + filename) ##AJUST ACCORDINGLY

            (o, rectangles) = localize.localize(f) ##o are the objects you need Natish

            frame = cv2.imread(IMG_FOLDER + "/" + filename)

            for r in rectangles:

                cv2.drawContours(frame, [r], -1, (0, 255, 0), 2)

            print(take_picture(frame))

            cv2.imshow("Tracking", frame)

            if cv2.waitKey(1) and 0xFF == ord("q"):
                break

            time.sleep(5)

    cv2.destroyAllWindows()




