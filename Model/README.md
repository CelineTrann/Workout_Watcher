## Data
The data needs to be a numerical 2D array as seen below.

```
data: [
    [features...],
    [features...],
    [features...],
    ...
]
```

There also needs to exists values associated with this data to indicate what theses data points represent. The values should be in numerical format, that map to a label.

Overall, the data should look like,
``` python
{'data': array([[5.1, 3.5, 1.4, 0.2],
                [4.9, 3. , 1.4, 0.2],
                [4.7, 3.2, 1.3, 0.2],
                [4.6, 3.1, 1.5, 0.2],...
'target': array([0, 0, 0, ... 1, 1, 1, ... 2, 2, 2, ...
'target_names': array(['setosa', 'versicolor', 'virginica'], dtype='<U10'), 
...}
```

Here the int in the `target` array correspond with the label at the index of `target_names`.


## Using the data
The data will be considered the "x-axis" of the data. Then the target array will be consider the "y-axis" when looking at the code.

## Acquiring the Data
There are 4 categories we need to consider
1. Left Foot
2. Right Foot
3. Left Hand
4. Rigth hand

Therefore, the following data points can be used to identify it
* height to width ratio of bounding box
* segment side that has more pressure (left or right foot arc)
* side with the lowest convexity [convexity defects](https://theailearner.com/2020/11/09/convexity-defects-opencv/) (left or right hand)

Note: This is subject to change

## Model to Use
Based on [this article](https://towardsdatascience.com/machine-learning-classifiers-comparison-with-python-33149aecdbca), given that we are trying to classify our data with less then 100k samples, we should use Linear SVC. If that model is not working we can use KNeighbours, SVC, or Ensemble Classifiers (Random Forest, AdaBoost).