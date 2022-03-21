#Computer vision library
import cv2 as cv

#Matrix math library
import numpy as np

#Read images from image name
haystack_img = cv.imread('haystack.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('needle.jpg', cv.IMREAD_UNCHANGED)

#Finds matches
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
print(result)
print()


#checks for matches
threshold = 0.4
locations = np.where(result >= threshold)
print(locations)
#Ignore
locations = list(zip(*locations[::-1]))

#Print out matches
print(locations)

#Finds height and width of needle image
needle_w = needle_img.shape[1]
needle_h = needle_img.shape[0]

#Make list for match rectangles
rectangles = []
for loc in locations:
    #      x value       y value      width     height
    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
    rectangles.append(rect)
    rectangles.append(rect)

print(rectangles)

rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

#if 0
#if 1:

if len(rectangles):
    print("Found needle")

    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    for (x, y, w, h) in rectangles:
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        center_x = x + int(w/2)
        center_y = y + int(h/2)
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        cv.drawMarker(haystack_img, (center_x, center_y), (255, 0, 255), cv.MARKER_STAR)
    cv.imshow('Matches', haystack_img)
    cv.waitKey()

#Show heat map of results
cv.imshow('Result', result)
cv.waitKey()
