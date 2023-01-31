# https://github.com/dataprofessor/code/blob/master/python/iris/iris-classification-random-forest.ipynb

# Import Library
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# load data

# set data
X = data
Y = target

# Split data into training and testing set (80-20)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# Build Model (Random Forest Classifier)
# Remember to adjust the model parameters
clf = RandomForestClassifier()
clf.fit(X_train, Y_train)


# Model Performance 
print(clf.score(X_test, Y_test))

# Adjust model until it is satisfactory

# Use to predict new data
new_data = []
print(clf.predict(new_data))

# To save and load a model see, https://stackabuse.com/scikit-learn-save-and-restore-models/