import numpy as np
import scipy.ndimage
import imageio
import cv2

img = "Linkedin.JPG"

def rgb2gray(rgb):
    return np.dot(rgb[..., :3],[0.2122,0.7152,0.0740])

def dodge(front,back):
    final_sketch = front*255/(255-back)
    final_sketch[final_sketch>255] = 255
    final_sketch[back==255] = 255
    return final_sketch.astype('uint8')
    

ss = imageio.imread(img)
gray = rgb2gray(ss)

i = 240-gray 

blur  = scipy.ndimage.filters.gaussian_filter(i,sigma = 15)
r = dodge(blur,gray)

cv2.imwrite('Linkedin-sketch.jpg',r)