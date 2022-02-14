import matplotlib.pyplot as plt
import cv2
from skimage.filters import difference_of_gaussians
from skimage import filters
import os

inputPath = os.path.realpath(os.path.dirname(__file__))

def gaussian():
  image = cv2.imread(inputPath + "/originals/ifb1.jpeg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  filtered_image = difference_of_gaussians(image, 1.5)
  image = plt.imshow(filtered_image, cmap=plt.cm.gray)

  plt.show()

def Roberts():
  image = cv2.imread(inputPath + "/originals/ifb2.jpeg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edge_roberts = filters.roberts(image)
  image = plt.imshow(edge_roberts, cmap=plt.cm.gray)

  plt.show()

def Sobel():
  image = cv2.imread(inputPath + "/originals/brasilia1.jpeg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edge_sobel = filters.sobel(image)
  image = plt.imshow(edge_sobel, cmap=plt.cm.gray)
  
  plt.show()

def Prewitt():
  image = cv2.imread(inputPath + "/originals/brasilia2.jpeg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edge_prewitt = filters.prewitt(image)
  image = plt.imshow(edge_prewitt, cmap=plt.cm.gray)

  plt.show()

def Scharr():
  image = cv2.imread(inputPath + "/originals/brasilia3.jpeg")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edge_scharr = filters.scharr(image)
  image = plt.imshow(edge_scharr, cmap=plt.cm.gray)

  plt.show()

gaussian()
Roberts()
Sobel()
Prewitt()
Scharr()