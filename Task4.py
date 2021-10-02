from sys import stderr
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from sys import argv

def boundingBox(colorMin, colorMax, colorSpace="RGB"):
    '''Tracks an object with color in [`colorMin`, `colorMax`] in the given
    color-space (`colorSpace`). Draws a bounding box around the object and
    displays the modified video stream.

    Heavily inspired by code from the OpenCV tutorials, specifically:
    https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
    https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html

    @param colorMin: The 3-item list representing the minimum color to track
    @param colorMax: The 3-item list representing the maximum color to track
    @param colorSpace: The color space to use. Either "RGB" or "HSV" (default
    "RGB")
    '''

    # Color constant depending on color-space
    red = [0,0,255]
    if colorSpace == "HSV":
        red = cv.cvtColor(np.uint8([[red]]), cv.COLOR_BGR2HSV)[0,0].tolist()

    cap = cv.VideoCapture(0)

    while(1):
        # Take each frame
        _, frame = cap.read()

        # Convert BGR to HSV, if necessary
        if colorSpace == "HSV":
            frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Grab area within color range (will be B/W)
        mask = cv.inRange(frame, colorMin, colorMax)

        # Find contours and draw bounding boxes on original frame for each
        contours, _ = cv.findContours(mask,
                                      cv.RETR_LIST,
                                      cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv.boundingRect(cnt)
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), red)

        # Convert back to BGR, if necessary
        if colorSpace == "HSV":
            frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)

        # Display new frame
        cv.imshow("bounded", frame)

        # Stop when ESC is pressed
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    validArgs = ["RGB", "HSV"]
    if len(argv) != 2 or (argv[1].upper() not in validArgs):
        print(f"Usage: {argv[0]} [RGB|HSV].", file=stderr)
        exit(1)
    
    colorMin = np.uint8([[[200, 150, 30]]])
    colorMax = np.uint8([[[240, 170, 70]]])
    if argv[1].upper() == "RGB":
        boundingBox(colorMin, colorMax)
    elif argv[1].upper() == "HSV":
        h = cv.cvtColor(np.uint8([[[222, 161, 49]]]), cv.COLOR_BGR2HSV)[0,0,0]
        colorMin = np.uint8([h - 10, 150, 150])
        colorMax = np.uint8([h + 10, 255, 255])
        boundingBox(colorMin, colorMax, "HSV")