from sys import stderr
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
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

def dominantColor():
    '''Uses K-means to find the dominant color of the middle 200x200 pixel
    square of the webcam. Fills the square on the video with the dominant color.

    Inspired heavily by https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097.
    '''

    cap = cv.VideoCapture(0)

    while(1):
        _, frame = cap.read()

        # Slice out the middle 200x200 pixel square
        halfSide = 100
        midH = frame.shape[0]//2
        midW = frame.shape[1]//2
        topL = (midW-halfSide, midH-halfSide)
        botR = (midW+halfSide, midH+halfSide)
        square = frame[midH-halfSide:midH+halfSide,midW-halfSide:midW+halfSide,:]

        # Reshape image to more easily cluster
        reshaped = square.reshape((square.shape[0] * square.shape[1], 3))
        km = KMeans(n_clusters=3)
        km.fit(reshaped)

        # Generate histogram for clusters
        hist, _ = np.histogram(km.labels_, bins=3)
        hist = hist.astype("float")
        hist /= hist.sum()

        # Get the dominant color according to the histogram
        domColor = max(zip(hist, km.cluster_centers_), key=lambda x: x[0])[1]

        # Put the filled rectangle on the frame and show the frame
        cv.rectangle(frame, topL, botR, domColor, -1)
        cv.imshow("dominant color", frame)

        # Stop when ESC is pressed
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    validArgs = ["RGB", "HSV", "DOM"]
    if len(argv) != 2 or (argv[1].upper() not in validArgs):
        print(f"Usage: {argv[0]} [RGB|HSV|DOM].", file=stderr)
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
    elif argv[1].upper() == "DOM":
        dominantColor()