import joblib
import cv2 
import numpy as np 
from skimage.feature        import graycomatrix
from scipy.stats            import kurtosis
import pywt
from GUI.settings import settings

class SVM_LINER:
    def __init__(self , path : str = None):
        self.Diseas     = ['glioma_tumor' , 'meningioma' , 'pituitary']
        self.classes    = {0:"normal" , 1:"upnormal"}
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-liner/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-liner/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-liner/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-liner/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-liner/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-liner/psvc.h5"),
        }
        self.path = path
        
    def reprocess_image(self):
        image = cv2.imread(self.path)
        image = cv2.resize(image , (256 , 256))
        image = image.reshape(1, -1)
        image = image/255
        
        return image 
    
    def calculate_texture_features(self ,glcm):
        homogeneity = np.sum(glcm * glcm)
        energy = np.sum(glcm**2)
        contrast = 0
        for i in range(glcm.shape[0]):
            for j in range(glcm.shape[1]):
                contrast += (i - j)**2 * glcm[i, j]

        idm = np.sum(glcm / (1 + (np.arange(glcm.shape[0]) - np.arange(glcm.shape[1]))**2))
        rms = np.sqrt(np.sum(glcm**2))
        smoothness = 1 - 1 / (1 + rms)
        variance = np.sum((np.arange(glcm.shape[0]) - idm)**2 * glcm.sum(axis=(0, 1)))

        return homogeneity, energy, contrast, idm, rms, smoothness, variance 
    
    
    
    def predict_image( self, image , pca , model = None , title = "testing"):
        image = self.reprocess_image()
        image_pca = pca.transform(image)
        prediction = model.predict(image_pca)
        score   = model.predict_proba(image_pca)
        predicted_class = self.classes[prediction[0]]
        self.outCome = {
            "title"          :title,
            "predicted_class":predicted_class,
            "loss"           :str(score[0][0]*100)[:5],
            "Accuracy"       :str(score[0][1]*100)[:5],
        }
        
        test_image_pca  = image_pca
        glcm            = graycomatrix(test_image_pca.astype(np.uint8), [1], [0], symmetric=True, normed=True)
        
        
        # Calculate texture features
        homogeneity, energy, contrast, idm, rms, smoothness, variance = self.calculate_texture_features(glcm)

        # Additional features
        mean_intensity = np.mean(test_image_pca)
        kurtosis_value = kurtosis(test_image_pca.flatten())
        entroppy = -np.sum(glcm * np.log(glcm + 1e-10))
        correlation = 0
        correlation_numerator = 0
        correlation_denominator = 0
        mean_values = np.arange(glcm.shape[0]).mean()

        # Calculate the correlation
        for i in range(glcm.shape[0]):
            for j in range(glcm.shape[1]):
                correlation_numerator += (i - mean_values) * (j - mean_values) * glcm[i, j]
                correlation_denominator += glcm[i, j] * np.std(np.arange(glcm.shape[0]))**2 * np.std(np.arange(glcm.shape[0]))**2
        correlation = correlation_numerator / correlation_denominator
        standard_deviation = np.std(glcm)

        self.result = {
            "prediction" : self.outCome ,
            "Correlation": correlation , 
            "Mean Intensity": mean_intensity,
            "Homogeneity": homogeneity,
            "Energy": energy,
            "Contrast": contrast,
            "Kurtosis" : kurtosis_value,
            "Variance": variance,
            "Smoothness":smoothness,
            "IDM":idm,
            "RMS": rms,
            "Entropy": entroppy,
            "Standard Deviation": standard_deviation
        }
    
        
        return self.result
    
    
    def run(self):
        
        allresult = []
        
        for D in self.Diseas:
            r = self.predict_image(image= self.path , pca=self.pca[D] , model=self.models[D] , title=D)
            allresult.append(r)
        
        return(allresult)


#                      # 
#           DWT        # 
#                      # 


class SVM_LINER_DWT:
    def __init__(self , path : str = None):
        
        self.Diseas     = ['glioma_tumor' , 'meningioma' , 'pituitary']
        self.classes    = {0:"normal" , 1:"upnormal"}
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-liner-dwt/psvc.h5"),
        }
        self.path = path
    
    # applay the dwt
    def n_level_dwt(self , image, wavelet, levels):
        coeffs = image
        for i in range(levels):
            coeffs = pywt.dwt2(coeffs, wavelet)
            coeffs = coeffs[0]
        image = cv2.normalize(coeffs , None , alpha=0 , beta=255 , norm_type=cv2.NORM_MINMAX)
        image = np.uint8(image)
        return image  
    
    
    def reprocess_image(self):
        image = cv2.imread(self.path)
        image = cv2.resize(image , (256 , 256))
        image = self.n_level_dwt(image , 'haar' , 3)
       
        image = image.reshape(1, -1)
        image = image/255
       
        return image 
    
    def calculate_texture_features(self ,glcm):
        
        homogeneity = np.sum(glcm * glcm)
        energy = np.sum(glcm**2)
        contrast = 0
        for i in range(glcm.shape[0]):
            for j in range(glcm.shape[1]):
                contrast += (i - j)**2 * glcm[i, j]

        idm = np.sum(glcm / (1 + (np.arange(glcm.shape[0]) - np.arange(glcm.shape[1]))**2))
        rms = np.sqrt(np.sum(glcm**2))
        smoothness = 1 - 1 / (1 + rms)
        variance = np.sum((np.arange(glcm.shape[0]) - idm)**2 * glcm.sum(axis=(0, 1)))

        
        return homogeneity, energy, contrast, idm, rms, smoothness, variance 
    
    
    
    def predict_image( self, image , pca , model = None , title = "testing"):
        
        image = self.reprocess_image()
        image_pca = pca.transform(image)
        prediction = model.predict(image_pca)
        score   = model.predict_proba(image_pca)
        predicted_class = self.classes[prediction[0]]
        self.outCome = {
            "title"          :title,
            "predicted_class":predicted_class,
            "loss"           :str(score[0][0]*100)[:5],
            "Accuracy"       :str(score[0][1]*100)[:5],
        }
        
        test_image_pca  = image_pca
        glcm            = graycomatrix(test_image_pca.astype(np.uint8), [1], [0], symmetric=True, normed=True)
        
        
        # Calculate texture features
        homogeneity, energy, contrast, idm, rms, smoothness, variance = self.calculate_texture_features(glcm)

        # Additional features
        mean_intensity = np.mean(test_image_pca)
        kurtosis_value = kurtosis(test_image_pca.flatten())
        entroppy = -np.sum(glcm * np.log(glcm + 1e-10))
        correlation = 0
        correlation_numerator = 0
        correlation_denominator = 0
        mean_values = np.arange(glcm.shape[0]).mean()

        # Calculate the correlation
        for i in range(glcm.shape[0]):
            for j in range(glcm.shape[1]):
                correlation_numerator += (i - mean_values) * (j - mean_values) * glcm[i, j]
                correlation_denominator += glcm[i, j] * np.std(np.arange(glcm.shape[0]))**2 * np.std(np.arange(glcm.shape[0]))**2
        correlation = correlation_numerator / correlation_denominator
        standard_deviation = np.std(glcm)

        self.result = {
            "prediction" : self.outCome ,
            "Correlation": correlation , 
            "Mean Intensity": mean_intensity,
            "Homogeneity": homogeneity,
            "Energy": energy,
            "Contrast": contrast,
            "Kurtosis" : kurtosis_value,
            "Variance": variance,
            "Smoothness":smoothness,
            "IDM":idm,
            "RMS": rms,
            "Entropy": entroppy,
            "Standard Deviation": standard_deviation
        }
    
        
        return self.result
    
    
    def run(self):
        
        allresult = []
        
        for D in self.Diseas:
            r = self.predict_image(image= self.path , pca=self.pca[D] , model=self.models[D] , title=D)
            allresult.append(r)
        
        return(allresult)
 
    
# 
#   RPF     
# 


class RPF(SVM_LINER):
    def __init__(self , path = None):
        super().__init__(path = path)
        
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-rpf/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-rpf/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-rpf/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-rpf/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-rpf/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-rpf/psvc.h5"),
        }


class RPF_DWT(SVM_LINER_DWT):
    def __init__(self , path = None):
        super().__init__(path = path)
        
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-rpf-dwt/psvc.h5"),
        }  

# 
#   POLY
#    

class POLY(SVM_LINER):
    def __init__(self , path = None):
        super().__init__(path = path)
        
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-poly/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-poly/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-poly/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-poly/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-poly/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-poly/psvc.h5"),
        }

class POLY_DWT(SVM_LINER_DWT):
    def __init__(self , path = None):
        super().__init__(path = path)
        
        self.pca        = {
                "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/gpca.h5"),
                "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/mpca.h5"),
                "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/ppca.h5"),
        }
        
        
        self.models     = {
            "glioma_tumor":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/gsvc.h5"),
            "meningioma":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/msvc.h5"),
            "pituitary":joblib.load(settings['BASE_DIR']/"models/svm-poly-dwt/psvc.h5"),
        }