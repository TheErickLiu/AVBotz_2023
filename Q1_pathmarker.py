import cv2
import numpy as np
from typing import Tuple
import sys
import os

def pathmarker_info(image_path: str) -> Tuple[int, int, int]:

    # read in image and convert to hsv colorspace
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## removes all colors but colors in lower bound and upper bounds
    lower_bound = (2, 100, 20)
    upper_bound = (15, 255, 255)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)


    # cv2.RETR_EXTERNAL: Gives only extreme outer contours / the ones that matter
    # cv2.CHAIN_APPROX_SIMPLE: compresses horizontal, vertical, and diagonal segments and leaves only their end points
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # find the largest contour with a matching color
    largest, idx = -1, -1
    for i, c in enumerate(contours):
        if cv2.contourArea(c) > largest:
            largest, idx = cv2.contourArea(c), i

    # center, width and height helps find correct angle
    (xPixelCenter, yPixelCenter), (width, height), angle = cv2.minAreaRect(contours[idx])

    if width > height:
        angle = angle - 90

    return (int(xPixelCenter), int(yPixelCenter), int(angle))


def main():
    if len(sys.argv) <= 1:
        sys.stderr.write('Error: missing input file\n')
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        sys.stderr.write('Error: input file does not exist.\n')
        sys.exit(1)

    result = pathmarker_info(input_file)
    print(' '.join([str(v) for v in result]))


if __name__ == "__main__":
    main()

