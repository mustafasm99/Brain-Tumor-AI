# Brain Cancer Detection with Python 

This application uses Python, TensorFlow, scikit-learn, and PySide6 to create a comprehensive Windows application capable of analyzing brain images and identifying different types of brain tumors.

## Models Used

### SVM Model
The SVM (Support Vector Machine) model is a linear algorithm used for binary classification tasks. In this application, the SVM model has been trained three times to ensure increased accuracy and reliable output.

Each model is trained for one of the following diseases:
1. Glioma tumor
2. Pituitary tumor
3. Meningioma tumor

This model achieves an accuracy of approximately 97%.

### KNN Model
The KNN (K-Nearest Neighbors) algorithm is a non-parametric method used for classification and regression. It is particularly effective for classification tasks where the decision boundary is irregular. Here's more detailed information about using KNN as a classifier in this application:

#### How KNN Works:
1. **Training Phase**: KNN does not have a traditional training phase. Instead, it memorizes the training dataset.
2. **Prediction Phase**: When a new data point is given, the algorithm:
   - Calculates the distance between the new data point and all the points in the training dataset. Common distance metrics include Euclidean, Manhattan, and Minkowski.
   - Selects the 'k' nearest data points (neighbors) to the new data point.
   - Determines the most common class among these neighbors. The new data point is classified into this class.

#### Advantages of KNN:
- **Simplicity**: KNN is easy to understand and implement.
- **No Training Time**: Since KNN is a lazy learner (it doesn't learn a discriminative function from the training data), it has a negligible training phase.
- **Versatility**: KNN can be used for both classification and regression tasks.

#### Disadvantages of KNN:
- **Computational Cost**: Calculating the distance between the data points can be computationally expensive, especially with large datasets.
- **Memory Intensive**: KNN stores all the training data, which can be a limitation in terms of memory usage.
- **Curse of Dimensionality**: The performance of KNN can degrade with high-dimensional data, as the distance between points becomes less meaningful.

#### Application in Brain Cancer Detection:
In this application, KNN is used to classify brain tumor images into different categories based on their features. The steps involved are:
- **Feature Extraction**: Extracting relevant features from the brain images.
- **Data Normalization**: Normalizing the features to ensure equal weightage.
- **Distance Calculation**: Calculating the distance between the new image's features and those of the training images.
- **Classification**: Classifying the new image based on the majority class of the 'k' nearest neighbors.

This model achieves an accuracy of approximately 90%.

### CNN Model
The CNN (Convolutional Neural Network) model uses multiple layers to preprocess the data and classify it. CNNs are particularly effective for image recognition tasks due to their ability to capture spatial hierarchies in images.

The architecture of the CNN model used in this application is as follows:

```python
Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 1))
MaxPooling2D(pool_size=(2, 2))
Conv2D(64, (3, 3), activation='relu')
MaxPooling2D(pool_size=(2, 2))
Conv2D(128, (3, 3), activation='relu')
MaxPooling2D(pool_size=(2, 2))
Flatten()
Dense(128, activation='relu')
Dropout(0.5)
Dense(4, activation='softmax')  # 4 classes

```

[image](https://github.com/mustafasm99/guipyside/blob/main/usedImages/Figure_1.png?raw=true)
