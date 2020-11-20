import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('images/im_6.jpg', 0)
min_l = 127
max_l = 255
ret, thresh1 = cv.threshold(img, min_l, max_l, cv.THRESH_BINARY)
ret, thresh2 = cv.threshold(img, min_l, max_l, cv.THRESH_BINARY_INV)
ret, thresh3 = cv.threshold(img, min_l, max_l, cv.THRESH_TRUNC)
ret, thresh4 = cv.threshold(img, min_l, max_l, cv.THRESH_TOZERO)
ret, thresh5 = cv.threshold(img, min_l, max_l, cv.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
	thresh = images[i]
	x_pixels, y_pixels = thresh.shape
	roi = thresh
	# roi = thresh(0.2*y_pixels,0.5*y_pixels,0,0.8*x_pixels)
	plt.subplot(2, 3, i + 1), plt.imshow(roi, 'gray')
	pixels = cv.countNonZero(roi)
	image_area = roi.shape[0] * roi.shape[1]
	area_perc = (pixels / image_area) * 100
	plt.title(f"{titles[i]}: {round(area_perc, 2)}%")
	plt.xticks([]), plt.yticks([])
plt.show()
