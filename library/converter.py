import cv2 as cv
import numpy as np
import classes.image as image
import library.helper as h

from copy import deepcopy

def rgb2rgba(img):
    """Converts the Provided Image from RGB to RGBA, Adding Alpha Values to Every Pixel.
    
    Parameters
    ----------
    img : ndarray, required
        The Loaded Image to Convert
    
    Returns
    -------
    The Converted Image, as an ndarray
    """
    
    if(type(img) == np.ndarray):
        return np.insert(img, 3, 255, axis=2)
    elif(type(img) == image.image):
        return np.insert(img.color, 3, 255, axis=2)

def rgba2rgb(img, background=[255,255,255], save_transparency=True):
    """Converts Color Image to RGB by Changing Transparent Pixels to the Background Color, Then Removes Alpha Channel"""

    if(type(img) == image.image):
        if(save_transparency): img.get_transparency()

        row_iter = 0
        col_iter = 0

        while row_iter < img.row_size:
            col_iter = 0
            while col_iter < img.col_size:
                if(img.color[row_iter, col_iter][3] == 0):
                    img.color[row_iter, col_iter] = [background[0], background[1], background[2], 1]
                col_iter += 1
            row_iter += 1

        img.color = img.color[:,:,:3]
        return img.color, img.transparent_pixels
    elif(type(img) == np.ndarray):
        row_iter = 0
        col_iter = 0

        transparent_pixels = []

        while row_iter < img.shape[0]:
            col_iter = 0
            while col_iter < img.shape[1]:
                if(img[row_iter, col_iter][3] == 0):
                    if(save_transparency): transparent_pixels.append([row_iter,col_iter])
                    img[row_iter, col_iter] = [background[0], background[1], background[2], 1]
                col_iter += 1
            row_iter += 1

        img = img[:,:,:3]
        return img, transparent_pixels

def rgb2yuv(img):
    if(type(img) == image.image):
        return cv.cvtColor(img.color, cv.COLOR_RGB2YUV)
    elif(type(img) == np.ndarray):
        return cv.cvtColor(img, cv.COLOR_RGB2YUV)

def yuv2rgb(img):
    if(type(img) == image.image):
        return cv.cvtColor(img.color, cv.COLOR_YUV2RGB)
    elif(type(img) == np.ndarray):
        return cv.cvtColor(img, cv.COLOR_YUV2RGB)
    
def bgr2rgb(img):
    if(type(img) == image.image):
        return cv.cvtColor(img.color, cv.COLOR_BGR2RGB)
    elif(type(img) == np.ndarray):
        return cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
def rgba2gray(img):
    temp_img, transparent_pixels = rgba2rgb(img)
    temp_img = rgb2gray(temp_img)
    return temp_img, transparent_pixels    

def rgb2gray(img):
    if(type(img) == image.image):
        return cv.cvtColor(img.color, cv.COLOR_RGB2GRAY)
    elif(type(img) == np.ndarray):
        return cv.cvtColor(img, cv.COLOR_RGB2GRAY)

def gray2rgb(img):
    if(type(img) == image.image):
        return cv.cvtColor(img.color, cv.COLOR_GRAY2RGB)
    elif(type(img) == np.ndarray):
        return cv.cvtColor(img, cv.COLOR_GRAY2RGB)

def gray2rgba(img, transparent_pixels=[]):
    temp_img = gray2rgb(img)
    temp_img = rgb2rgba(temp_img)
    if transparent_pixels:
        h.restore_transparency(temp_img, transparent_pixels)
    return temp_img
    
def img_range(img, max=1):
    row_iter = 0
    col_iter = 0
    if(max==1):
        while row_iter < img.shape[0]:
            col_iter = 0
            while col_iter < img.shape[1]:
                pixel = img[row_iter,col_iter]
                if(len(img) == 3):
                    img[row_iter,col_iter] = [pixel[0]/255, pixel[1]/255, pixel[2]/255, pixel[3]]
                elif(len(img) == 2):
                    img[row_iter,col_iter] = pixel/255
                col_iter += 1
            row_iter += 1
        return img
    elif(max==255):
        while row_iter < img.shape[0]:
            col_iter = 0
            while col_iter < img.shape[1]:
                pixel = img[row_iter,col_iter]
                if(type(pixel) == np.float64):
                    img[row_iter,col_iter] = pixel*255
                else:
                    img[row_iter,col_iter] = [pixel[0]*255, pixel[1]*255, pixel[2]*255, pixel[3]]
                col_iter += 1
            row_iter += 1
        return img

