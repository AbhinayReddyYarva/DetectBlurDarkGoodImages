# USAGE
# python detect_blur_dark.py --images images

# importing the necessary packages
from imutils import paths
import argparse
import cv2

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def gray_scale_mean(image):
	# compute the gray scale image mean and then return the mean value
	return cv2.mean(gray)[0]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-bt", "--blurthreshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-dt", "--darkthreshold", type=float, default=60.0,
	help="average pixel intesity fall below this value will be considered 'dark'")
args = vars(ap.parse_args())

# loop over the input images
for imagePath in paths.list_images(args["images"]):
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian and Gray scale mean
	print(imagePath)# method
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	print("{}: Variance of the Laplacian {:.2f}".format(imagePath, fm))
	dk = gray_scale_mean(gray)
	print("{}: Gray scale mean {:.2f}".format(imagePath, dk))
	text = "Good"

	# if the focus and dark measure is less than the supplied threshold,
	# then the image should be considered "blurry and dark" or "dark" or "blurry"
	if fm < args["blurthreshold"] and dk < args["darkthreshold"]:
		text = "Blurry and Dark"
	elif dk < args["darkthreshold"]:
		text = "Dark"
	elif fm < args["blurthreshold"]:
		text = "Blurry"

	# show the image
	cv2.putText(image, "{}:Focus-{:.2f} Mean-{:.2f}".format(text, fm, dk), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	key = cv2.waitKey(0)