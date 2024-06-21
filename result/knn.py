import cv2 as cv 
import numpy as np 
import joblib
from GUI.settings import settings 
import pywt


class KNN:
     model_path = settings['BASE_DIR']/"models/KNN/knn_model.joblib"
     model = joblib.load(model_path)
     
     def __init__(self , image_path:str=None):
          self.path = image_path
     
     def preprocess_image(self):
          img = cv.imread(self.path)
          img = cv.resize(img, (256, 256))
          img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
          img = np.array(img).flatten()
          return img
     
     def run(self):
          img = self.preprocess_image()
          prediction = self.model.predict([img])
          result = {
               "prediction class" : prediction[0]
          }
          return result


class KNN_DWT:
     model_path = settings['BASE_DIR']/"models/KNN/knn_model_DWT.joblib"
     model = joblib.load(model_path)
     
     def __init__(self, image_path):
          self.path = image_path
     
     def n_level_dwt(self , image , wavelet , levels = 3):
          coeffs = image
          for i in range(levels):
               coeffs = pywt.dwt2(coeffs, wavelet)
               coeffs = coeffs[0]
          image = cv.normalize(coeffs , None , alpha=0 , beta=255 , norm_type=cv.NORM_MINMAX)
          image = np.uint8(image)
          return image
     
     def preprocess_image(self):
          img = cv.imread(self.path)
          img = cv.resize(img, (256, 256))
          img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
          img = self.n_level_dwt(img ,"haar" , 3)
          img = np.array(img).flatten()
          return img

     def run(self):
          img = self.preprocess_image()
          prediction = self.model.predict([img])
          result = {
               "prediction class" : prediction[0]
          }
          return result
     