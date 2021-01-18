import os
import io
import argparse
import imutils
from google.cloud import vision
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import cv2
from matplotlib import pyplot as plt
from matplotlib import patches as pch

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'config/config_ocr.json'


class VisionOCR:
    def __init__(self, image):
        self.image = image

    def vision_environment(self):
        client = vision.ImageAnnotatorClient()
        file_name = os.path.abspath(self.image)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels: ')
        for label in labels:
            print(label.description)

    def document_spilt_text(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as file:
            content = file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        lst = []
        for i in texts:
            text = str(i.description).split()
            lst.append(text)
        print(lst)
        ocr = ''.join(lst[0])
        return ocr

    def document_google(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        txt = ''
        for text in texts:
            txt += text.description
        return txt

    def document_google_plot(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        x_axis = []
        y_axis = []
        txt = ''
        a = plt.imread(self.image)
        fig, ax = plt.subplots(1)
        ax.imshow(a)

        for text in texts:
            txt += text.description
            for vertex in text.bounding_poly.vertices:
                x_axis.append(vertex.x)
                y_axis.append(vertex.y)
            vertices = ([(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])
            X = vertices[0]
            X1 = vertices[1]
            Y = vertices[2]
            rect = pch.Rectangle(X, (X1[0] - X[0]),
                                 (Y[1] - X[1]), linewidth=1,
                                 edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.show()
        return txt

    def document_pandas(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        feature = vision.Image(content=content)
        response = client.text_detection(image=feature)
        texts = response.text_annotations
        df = pd.DataFrame(columns=['locale', 'description', 'vertextX', 'vertextY'])
        for text in texts:
            vertices = ([(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])
            print(vertices[0], vertices[2])
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description,
                    vertextX=vertices[0],
                    vertextY=vertices[2]
                ),
                ignore_index=True
            )
        return df

    def document_uri(self):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = self.image
        response = client.text_detection(image=image)
        texts = response.text_annotations

        df = pd.DataFrame(columns=['locale', 'description'])
        for text in texts:
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description
                ),
                ignore_index=True
            )
            return df

    def document_tesseract(self):
        text_classifier = pytesseract.image_to_string(Image.open(self.image), lang='tha')
        image = cv2.imread(self.image)
        scale = 0.5
        img_convert = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        img = cv2.threshold(img_convert, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow('img', img)
        cv2.waitKey(3)
        return text_classifier


def edu_resize(image):
    img = cv2.imread(image)
    img_resize = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    img_cropped = img[0:200, 200:500]
    cv2.imshow('Original', img)
    cv2.imshow('Resize', img_resize)
    cv2.imshow('Cropped', img_cropped)
    cv2.waitKey(0)


def edu_gray(image):
    img = cv2.imread(image)
    kernel = np.ones((5, 5), np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
    img_threshold = cv2.Canny(img, 100, 100)
    img_dialation = cv2.dilate(img_threshold, kernel=kernel, iterations=1)
    img_ercoded = cv2.erode(img_dialation, kernel=kernel, iterations=1)
    cv2.imshow('Gray Image', img_gray)
    cv2.imshow('Blur Image', img_blur)
    cv2.imshow('Threshole', img_threshold)
    cv2.imshow('dialation', img_dialation)
    cv2.imshow('ercoded', img_ercoded)
    cv2.waitKey(0)


def edu_numpy():
    square = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    square[0][1] = 4
    square[1][0:] = np.arange(3)
    a = np.zeros((3, 4), dtype='int')
    b = np.ones((3, 4), dtype='float')
    c = np.identity(3, dtype='int')
    d = np.eye(3, 5)

def dimention_img():
    img = np.zeros((512, 512, 3), np.uint8) # height, width
    cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), 3) # width height
    cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
    cv2.circle(img, (400, 50), 30, (255, 0, 0), 3)
    cv2.imshow('image', img)
    cv2.waitKey(0)
