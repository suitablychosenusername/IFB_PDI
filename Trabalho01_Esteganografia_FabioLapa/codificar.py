#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cv2, os
from numpy import uint8

#  .----------------------------------.
# |              INDEX                 |
# |------------------------------------|
# | Parser de Argumentos ------ Ln  27 |
# | Classe Encoder ------------ Ln  41 |
# |     ∟ __init__ ------------ Ln  45 |
# |     ∟ str2bin ------------- Ln  53 |
# |     ∟ bin2str ------------- Ln  71 |
# |     ∟ inject -------------- Ln  86 |
# |     ∟ extract ------------- Ln 120 |
# |     ∟ show_channels ------- Ln 145 |
# |     ∟ save ---------------- Ln 181 |
# | Main ---------------------- Ln 186 |
# | Codificação --------------- Ln 218 |
# | Decodificação ------------- Ln 235 |
# |                                    |
# '------------------------------------'

#  .----------------------.
# |  Parser de Argumentos  |
#  '----------------------'

parser = argparse.ArgumentParser()

parser.add_argument("imagePath", metavar="IMAGEPATH.PNG", type=str, help= "Name of or path to an PNG file.")
parser.add_argument("-c", "--Encode", metavar="TEXTFILE.TXT", nargs=1, type=str, help = "Reads a TXT file and encodes the text into the target IMAGEPATH.PNG.")
parser.add_argument("-d", "--Decode", action='store_true', help = "Reads IMAGEPATH.PNG file and decodes a message from it.")
parser.add_argument("-l", "--Layer", type=int, choices=[0, 1, 2], default=0, help = "The color layer in which the message should be hidden into. /  0 = Blue [default] / 1 = Green / 2 = Red.")
parser.add_argument("-o", "--Output", metavar="OUTPUTIMAGE.PNG | OUTPUTMESSAGE.TXT", nargs=1, help = "Name of or path to the destination file. Must be a PNG if encoding and a TXT if decoding. [default = \"IMAGEPATH_Copy.PNG\" | \"IMAGEPATH_Extract.TXT\"]")

args = parser.parse_args()

#  .---------------------.
# |    Classe Encoder     |
#  '---------------------'

class Encoder:
    def __init__(self, color_layer, src_image_path="", string=""):
        self.string = string
        self.srcimage = cv2.imread(src_image_path)
        self.cpyimage = self.srcimage.copy()
        self.channel = color_layer

# ------------------------------------------------------------------------------
    # converter a string para binario
    def str2bin(self, string):
        # se string for uma string, faça:
        if type(string) == str:
            # armazene em lo uma lista de cada caractere da string, convertido em binario de 8 digitos
            lo = [ format(ord(character), '08b') for character in string ]
            # retorne a junção da lista como string, finalizado por "/\/\/\/\/\"
            for i in range(5):
                lo.append(format(ord("/"), "08b"))
                lo.append(format(ord("\\"), "08b"))
            lo = ''.join(lo)
            return lo, len(lo)

        # se string for um valor inteiro, retorne este valor em binario
        elif type(string) == uint8 or type(string) == int:
            return format(string, "08b")

# ------------------------------------------------------------------------------
    # converter uma string binaria para string
    def bin2str(self, string):
        # faça uma lista de numeros com 8 digitos
        aux = [ string[i:i+8] for i in range(0, len(string), 8) ]
        message = ''
        # para cada numero em aux, faça:
        for i in aux:
            # converta o numero para caractere e concatene em message
            message += chr(int(i, 2))
            # se achar o delimitador, quebre o loop
            if message[-10:] == '/\\/\\/\\/\\/\\':
                break
        return message

# ------------------------------------------------------------------------------
    # injetar a messagem na imagem
    def inject(self):
        # teste se tamanho da imagem, em byte, é suficiente para o texto.
        if (self.srcimage.shape[0] * self.srcimage.shape[1] * 4 // 8) < len(self.string) + 10:
            print("Image is smaller than text. Please, input a bigger image or smaller text.")
            exit(0)

        # converta o texto em binario
        message, msg_size = self.str2bin(self.string)

        i = 0

        finished = False
        # percorra os pixels da imagem
        for row in self.cpyimage:
            for pixel in row:
                # se mensagem ainda não foi concluida, altere o ultimo bit do canal
                if i < msg_size:
                    # converta o valor do canal selecionado em binario
                    channel_info =  self.str2bin(pixel[self.channel])
                    # altere o valor dos 4 ultimos bits do canal selecionado no pixel
                    pixel[self.channel] = int(channel_info[:-4] + message[i] + message[i+1] +
                                                        message[i+2] + message[i+3], 2)
                    i += 4
                # senao quebre loops
                else:
                    finished = True
                    break;
            if finished:
                break;

        print("Injected!")

# ------------------------------------------------------------------------------
    # Extrair a mensagem
    def extract(self):
        message = ""
        finished = False
        # formate 0 delimitador em binario
        delimiter = format(ord("/"), '08b') + format(ord("\\"), '08b')
        delimiter += delimiter + delimiter + delimiter + delimiter
        # Percorra a imagem:
        for row in self.cpyimage:
            for pixel in row:
                # converta o valor do canal selecionado em binario
                channel_info = self.str2bin(pixel[self.channel])
                # concatene os ultimos bits do canal selecionado em uma unica string
                message += channel_info[-4:]
                # faça até encontrar o delimitador
                if message[-80:] == delimiter:
                    finished = True
                    break;
            if finished:
                break;

        # converta a string resultante para texto e retorne
        return self.bin2str(message)[:-10]

# ------------------------------------------------------------------------------
    # Mostrar canais de cores de ambas as imagens
    def show_channels(self):
        # Imagem original e seus canais
        cv2.imshow("Original Image", self.srcimage)
        red = self.srcimage.copy()
        red[:, :, 0] = 0
        red[:, :, 1] = 0
        green = self.srcimage.copy()
        green[:, :, 0] = 0
        green[:, :, 2] = 0
        blue = self.srcimage.copy()
        blue[:, :, 1] = 0
        blue[:, :, 2] = 0
        cv2.imshow("Red Channel", red)
        cv2.imshow("Green Channel", green)
        cv2.imshow("Blue Channel", blue)

        # Imagem alterada e seus canais
        cv2.imshow("Copy Image", self.cpyimage)
        redp = self.cpyimage.copy()
        redp[:, :, 0] = 0
        redp[:, :, 1] = 0
        greenp = self.cpyimage.copy()
        greenp[:, :, 0] = 0
        greenp[:, :, 2] = 0
        bluep = self.cpyimage.copy()
        bluep[:, :, 1] = 0
        bluep[:, :, 2] = 0
        cv2.imshow("Red Channel Copy", redp)
        cv2.imshow("Green Channel Copy", greenp)
        cv2.imshow("Blue Channel Copy", bluep)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ------------------------------------------------------------------------------
    # salvar a imagem alterada
    def save(self, outputname):
        cv2.imwrite(outputname, self.cpyimage)
        print("Saved to", outputname)

#  .----------------------.
# |          Main          |
#  '----------------------'
    
if __name__ == '__main__':

    if args.Encode and args.Decode:
        print("You can't encode and decode files in the same run!")
        exit(0)

    if not args.Encode and not args.Decode:
        print("You should choose either to encode [-c] or decode [-d] the message into the image file!")
        exit(0)
    # print(args.imagePath)
    if not os.path.exists(args.imagePath):
        print("Image file not found!")
        exit(0)

    if args.Output:
        outputname = args.Output[0]
    elif args.Encode:
        outputname = args.imagePath.removesuffix(".png") + "_Copy.png"
    elif args.Decode:
        outputname = args.imagePath.removesuffix(".png") + "_Extract.txt"
    
    if args.Layer:
        color_layer = args.Layer
    else:
        color_layer = 0


# ------------------------------------------------------------------------------
    # codificar a mensagem na imagem
    if args.Encode:
        # teste se arquivo existe
        if not os.path.exists(args.Encode[0]):
            print("Text file not found!")
            exit(0)
        # abra arquivo em modo leitura e extraia todas as linhas
        with open(args.Encode[0], 'r', encoding='utf-8') as f:
            msg = "".join(f.readlines())

        # crie o objeto Encoder e realize as operações inject, show_channels e save.
        en = Encoder(string=msg, src_image_path=args.imagePath, color_layer=color_layer)
        en.inject()
        en.show_channels()
        en.save(outputname)

# ------------------------------------------------------------------------------
    # descodificar a mensagem na imagem
    elif args.Decode:
        # crie o objeto Encoder e realize a operação extract, salvando o destino no arquivo
        en = Encoder(src_image_path=args.imagePath, color_layer=color_layer)
        with open(outputname, 'w', encoding='utf-8') as t:
            t.write(en.extract())