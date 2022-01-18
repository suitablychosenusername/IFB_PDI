import numpy as np
import cv2
import os

imageFiles = ["seagull.png", "baboon.png", "butterfly.png", "city.png", "house.png"]
inputPath = os.path.realpath(os.path.dirname(__file__))
outputPath = inputPath + "/output/02/"
inputPath += "/originals/"

kernels = [
    # h1 - laplaciano do gaussiano
    np.array([  [ 0,  0, -1,  0,  0],
                [ 0, -1, -2, -1,  0],
                [-1, -2, 16, -2, -1],
                [ 0, -1, -2, -1,  0],
                [ 0,  0, -1,  0,  0] ]),

    # h2
    np.array([  [ 1,  4,  6,  4,  1],
                [ 4, 16, 24, 16,  4],
                [ 6, 24, 36, 24,  6],
                [ 4, 16, 24, 16,  4],
                [ 1,  4,  6,  4,  1] ]) / 256,

    # h3 - sobel vertical
    np.array([  [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1] ]),

    # h4 - sobel horizontal
    np.array([  [-1, -2, -1],
                [0]*3,
                [ 1,  2,  1] ]),

    # h5 - detecção de pontos
    np.array([  [-1]*3,
                [-1,  8, -1],
                [-1]*3] ),
    
    # h6 - blur
    np.array(   [[1]*3]*3 ) / 9,

    # h7 - detecção de retas
    np.array([  [-1, -1,  2],
                [-1,  2, -1],
                [ 2, -1, -1] ]),

    # h8 - detecção de retas
    np.array([  [ 2, -1, -1],
                [-1,  2, -1],
                [-1, -1,  2] ]),
    # h9
    np.diag(    [1]*10 ) / 9,

    # h10
    np.array([  [-1]*5,
                [-1, 2, 2, 2, -1],
                [-1, 2, 8, 2, -1],
                [-1, 2, 2, 2, -1],
                [-1]*5 ]) / 8,
    
    # h11
    np.array([  [-1, -1,  0],
                [-1,  0,  1],
                [ 0,  1,  1] ]),

    # sqrt( (h3)^2 + (h4)^2 )
    np.array([  [0]*3]*3) ]

def readFiles():
    images = []
    for i in range(len(imageFiles)):
        images.append(cv2.imread(inputPath + imageFiles[i], cv2.IMREAD_GRAYSCALE))
        if images[i] is None:
            print("\nERROR: Coult not read file:", inputPath + imageFiles[i])
            exit(0)
    return images
    
class Originals:
    def __init__(self, images):
        self.images = images
    
    # def showAll(self):
    #     for i in range(len(imageFiles)):
    #         cv2.imshow(imageFiles[i], self.images[i])
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    def applyKernel(self, kernelMatrices):
        outputFiles = []
        for i in self.images:
            outputImages = []
            for j in kernelMatrices:
                outputImages.append(cv2.filter2D(src=i, ddepth=-1, kernel=j))
            outputFiles.append(outputImages)
        
        for i in range(len(outputFiles)):
            for j in range(len(kernels)):
                name, fileFormat = imageFiles[i].split(".")
                if j+1 != 12:
                    cv2.imwrite(outputPath + name + "_Kernel_" + str(j+1) + "." + fileFormat, outputFiles[i][j])
                else:
                    cv2.imwrite(outputPath + name + "_Kernels_3_with_4." + fileFormat, outputFiles[i][j])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

originals = Originals(readFiles())
# originals.showAll()
originals.applyKernel(kernels)