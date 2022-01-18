import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


# CAMINHOS PARA AS IMAGENS DA LENA E LENA_MODIFICADA

inputPathLena = "lena.jpg"
inputPathLenaMod = "lena_modificada.jpg"

# função para mostrar todos os histogramas em uma só janela (praticamente copiada e colada)
def show_hist(image):
    ncols = 3
    nrows = 2
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))

    label = ["Original", "Add", "Sub", "Mul", "Div"]
    counter = 0
    x = 0
    for i in range(nrows):
        for j in range(ncols):

            ax = axes[i][j]

            # Plot when we have data
            if counter < len(image):

                ax.hist(image[j].ravel(), 256, [0,256])
                leg = ax.legend(loc='upper left')
                ax.set_title(label[x])
                x += 1
                leg.draw_frame(False)

            # Remove axis when we no longer have data
            else:
                ax.set_axis_off()

            counter += 1

    fig.suptitle("Histograms")
    plt.show()

# -------------------------------------------------------

# calcula ME
def calc_ME(image):
    print("\n# ----- Erro Maximo ----- #")
    shape = image[0].shape
    label = ["Original", "Add", "Sub", "Mul", "Div"]
    for i in range(1, len(image)):
        max_error = []
        for row in range(0, shape[0]):
            for col in range(0, shape[1]):
                max_error.append(abs(image[0].item(row, col) - image[i].item(row, col)))
    
        print("Erro Máximo: ", label[i], max(max_error))
    print()

# -------------------------------------------------------

# Calcula MAE
def calc_MAE(image):
    print("\n# ----- Erro Maximo Absoluto ----- #")
    shape = image[0].shape
    label = ["Original", "Add", "Sub", "Mul", "Div"]
    for i in range(1, len(image)):
        max_error = 0
        for row in range(0, shape[0]):
            for col in range(0, shape[1]):
                max_error += abs(image[0].item(row, col) - image[i].item(row, col))
    
        max_err = max_error/image[0].size
        print("Erro Máximo Absoluto: {0} {1:0.2f}".format(label[i], max_err))
    print()

# -------------------------------------------------------

#  calcula MSE
def calc_MSE(image, show_results=1):
    print("\n# ----- Erro Medio Quadratico ----- #")
    shape = image[0].shape
    hell = []
    label = ["Original", "Add", "Sub", "Mul", "Div"]
    for i in range(1, len(image)):
        max_error = 0
        for row in range(0, shape[0]):
            for col in range(0, shape[1]):
                max_error += (image[0].item(row, col) - image[i].item(row, col))**2
    
        max_error = max_error/image[0].size
        hell.append(max_error)
        if(show_results):
            print("Erro Medio Quadratico: {0} {1:.2f}".format(label[i], max_error))
    print()
    return hell

# -------------------------------------------------------

# calcula PSNR
def calc_PSNR(image):
    hell = calc_MSE(image, 0)
    label = ["Add", "Sub", "Mul", "Div"]
    print("\n# ----- Relacao Sinal-Ruido de Pico -----")
    for i in range(0, 4):
        max_error = 10 * np.log10((image[0].size * 255*255)/(hell[i]))
        print("Relacao Sinal-Ruido de Pico: {0} {1:.2f}".format(
            label[i], max_error))

# -------------------------------------------------------

# aplica ruido gaussiano na imagem
def ruidoG(imagem, m = 0, v = 0.01):
    imagem = np.array(imagem/255, dtype = float)

    ruido = np.random.normal(m, v ** 0.5, imagem.shape)
    gaussiano = imagem + ruido

    if gaussiano.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.

    gaussiano = np.clip(gaussiano, low_clip, 1.0)
    gaussiano = np.uint8(gaussiano*255)
    
    cv.imshow("Gaussiano", gaussiano)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return gaussiano

# -------------------------------------------------------

# calcula entropia
def entropia(image):

    entr = []
    hist = cv.calcHist([image], [0], None, [256], [0, 255])

    for ni in hist:
        p = ni / image.size
        if p == 0:
            en = 0
        else:
            en = -1 * p * (np.log(p) / np.log(2))
        entr.append(en)

    print("Entropia: ", sum(entr))

# -------------------------------------------------------

# converte para imagem binaria com bias de intensidade = 10
def imbin(image):
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image.item(row,col) > 10:
                image.itemset((row,col), 255)
            else:
                image.itemset((row,col), 0)
    return image

# -------------------------------------------------------

if __name__ == "__main__":
    # Questão 01
    image = []
    image.append(cv.imread(inputPathLena, cv.IMREAD_GRAYSCALE))

    # Questão 02
    # Soma
    image.append(cv.add(image[0], 30))

    # Subtração
    image.append(cv.subtract(image[0], 70))

    # Multiplicação
    image.append(cv.multiply(image[0], 1.2))
    
    # Divisão
    image.append(cv.divide(image[0], 4))

    # Mostrar o resultado das operações sobre a imagem original
    cv.imshow("Original", image[0])
    cv.imshow("Add", image[1])
    cv.imshow("Sub", image[2])
    cv.imshow("Mul", image[3])
    cv.imshow("Div", image[4])
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Questões 03 e 04
    # Mostrar o histograma
    show_hist(image)

    # Questão 05
    # Calculo de Erros
    calc_ME(image)
    calc_MAE(image)
    calc_MSE(image)
    calc_PSNR(image)

    # Questão 06
    # Constroi a piramide e mostra os resultados a cada nivel
    img2 = image[0].copy()
    for i in range(4):
        img2 = cv.pyrDown(img2)
        cv.imshow("meh", img2)
        cv.waitKey(0)
        cv.destroyAllWindows()


    # Questão 07
    # Aplicar ruido gaussinao
    comruido = ruidoG(image[0])

    # Questão 08
    # Calcular entropia
    print("# ----- Lena Original -----")
    entropia(image[0])
    print("# ----- Lena com Ruido -----")
    entropia(comruido)

    # Questão 09
    # Carrega a lena_modificada
    lenaMod = cv.imread(inputPathLenaMod, 0)
    lenaOri = image[0].copy()
    # Calcula a diferenca entre a modificada e a original e a converte em bin
    dif = imbin(cv.subtract(lenaOri,lenaMod))
    # Mostra o resultado
    cv.imshow("Ori - Mod", dif)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    # Questão 10
    # Calcula componentes vizinhanca-4
    fourway = cv.connectedComponents(dif, connectivity=4)
    # Calcula componentes vizinhanca-8
    eightway = cv.connectedComponents(dif, connectivity=8)
    print("Numero componentes Vizinhanca-4:", fourway[0])
    print("Numero componentes Vizinhanca-8:", eightway[0])

