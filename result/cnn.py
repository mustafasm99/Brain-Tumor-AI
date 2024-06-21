import cv2
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
from keras.metrics import CategoricalAccuracy
from GUI.settings import settings


"""
class to get the image result form the 
CNN model. 
"""

class CNN:
    model = load_model(settings['BASE_DIR'] / "models/CNN/brain_cancer_classifier.h5")
#     model = load_model("C:/project/guipyside/models/CNN/brain_cancer_classifier.h5")
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[CategoricalAccuracy()])
    classes = {0: "normal", 1: "glioma_tumor", 2: "meningioma", 3: "pituitary"}
    labels = [0 , 1 , 2 , 4]
    
    
    def __init__(self, image_path):
        self.path = image_path

    def preprocess_image(self):
        # Load and preprocess the image
        img = cv2.imread(self.path)
        img = cv2.resize(img, (256, 256))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        img = np.expand_dims(img, axis=-1)  # Add a channel dimension
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        
        
        return img

    def classify_image(self):
        img = self.preprocess_image()

        # Predict the class of the image
        predictions = self.model.predict(img)
        predicted_class = np.argmax(predictions)

        # Map the predicted class index to the class name
        predicted_class_name = self.classes[predicted_class]

        # Get prediction probability for the predicted class
        predicted_probability = np.max(predictions)

        return predicted_class_name, predicted_probability

    def evaluate_image(self, true_label):
        img = self.preprocess_image()
        true_labels = np.array([true_label])
        true_labels = to_categorical(true_labels, num_classes=len(self.classes))
        print(true_labels , true_label)
        # Evaluate the image to get loss and accuracy
        loss, accuracy = self.model.evaluate(img, true_labels , verbose = 2)

        return loss, accuracy

    def run(self):
        classification_result = self.classify_image()
        predicted_class_name = classification_result[0]
        predicted_class_idx = list(self.classes.keys())[list(self.classes.values()).index(predicted_class_name)]
        
        
        
        evaluation_result = self.evaluate_image(predicted_class_idx)
        result = {
            "predicted_class"       : classification_result[0],
            "predicted_probability" : classification_result[1],
            "loss"                  : evaluation_result[0],
            "accuracy"              : evaluation_result[1]
        }

        return result
