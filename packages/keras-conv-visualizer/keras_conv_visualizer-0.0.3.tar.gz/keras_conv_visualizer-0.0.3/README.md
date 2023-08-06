# Keras Conv Visualizer
> Package allows visualize convolutional layers from keras models.

## Table of contents
* [General info](#general-info)
* [Libraries](#libraries)
* [Setup](#setup)
* [Documentation](#documentation)
* [PyPi](#pypi)
* [TODO](#todo)
* [Development](#development)
* [Status](#status)
* [Contact](#contact)

## General info
This package is a set of tools for visualizing convolutional layers from keras models. At this moment includes:
* [Filters visualization](#filters-visualization)
* [Grad-CAM activation visualization](#grad-cam)
* [Intermediate activations visualization](#intermediate-activations-visualization)

## Libraries
- Keras - version 2.4.3
- Matplotlib - version 3.3.3
- NumPy - version 1.19.4
- OpenCV - version 4.4.0.46
- TensorFlow - version 2.4.0rc1

## Setup
* Install from PyPi: `pip install keras-conv-visualizer`

## Documentation
#### Status: _in progress_
### Filters visualization
```python
import matplotlib.pyplot as plt
from tensorflow.keras.applications import VGG16
from keras_conv_visualizer.filters import FilterVisualization

# Model has to have standarized input (std=0, var=1)!
model = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
layer_name = "block5_conv3"

# First parameter - trained keras model, second - input_size
fv = FilterVisualization(model)
# First parameter - layer feature index (ex. block1_conv1 has (224, 224, 64) index is from 0 to 63)
# Second parameter - layer name
loss, img = fv.visualize_filter(0, layer_name)
plt.imshow(img)
```
Result:

[![filters.png](https://i.postimg.cc/YCxdK1nP/filters.png)](https://postimg.cc/Mnv71j80)

<h3 id="grad-cam">Grad-CAM activation visualization</h3>

```python
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import VGG16, imagenet_utils
import matplotlib.pyplot as plt
from keras_conv_visualizer.gradcam import GradCAM

img_path = 'elephant.jpg'

# load the input image from disk (in Keras/TensorFlow format) and preprocess it
image = load_img(img_path, target_size=(224, 224))
image = img_to_array(image)
image = imagenet_utils.preprocess_input(image)

model = VGG16(weights="imagenet", input_shape=(224, 224, 3))

cam = GradCAM(model)
# First parameter - image tensor, second - image path, third - alpha value for heatmap (transparency)
heatmap, output = cam.make_superimposed_img(image, img_path, alpha=0.6)

plt.imshow(heatmap)
plt.imshow(output)
```
Results:

| <img src = "https://i.postimg.cc/nrtpXsL5/elephant.png" width=350> | <img src = "https://i.postimg.cc/G3Vzdr9W/heatmap.png" width=500> | <img src = "https://i.postimg.cc/28WG5JZV/superimposed.png" width=500> |
|:--:| :--: | :--: |
| *Input image* | *Heatmap* | *Superimposed image* |


### Intermediate activations visualization
```python
from keras.models import load_model
from keras.preprocessing import image
from keras_conv_visualization.intermediate_activations import IntermediateActivations

# load the input image from disk (in Keras/TensorFlow format) and preprocess it
img = image.load_img('some_image.png', target_size=(96, 96), color_mode='grayscale')
img_tensor = image.img_to_array(img)
img_tensor /= 255

model = load_model('some_model.h5')

int_activations = IntermediateActivations(model)
int_activations.plot_intermediate_activations(img_tensor)
```

Input image:

[![input-image.png](https://i.postimg.cc/1tBsV71h/input-image.png)](https://postimg.cc/47Yrr53B)

Results:
<p align="center">
  <img src = "https://i.postimg.cc/5NS4htRN/r1.png" width=350 height=350>
  <img src = "https://i.postimg.cc/wjxqgdC5/r2.png" width=350 height=350>
  <img src = "https://i.postimg.cc/66R5hcVZ/r3.png" width=350 height=350>
  <img src = "https://i.postimg.cc/jdbq3fvF/r4.png" width=350 height=350>
</p>

## PyPi
[keras-conv-visualizer](https://pypi.org/project/keras-conv-visualizer/)

## TODO
- Add shap values
- Automatically recognition input size for FilterVisualization

## Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

* Fork the repo
* Create a new branch (`git checkout -b improve-feature`)
* Make the appropriate changes in the files
* **Verify if they are correct**
* Add changes to reflect the changes made
* Commit changes
* Push to the branch (`git push origin improve-feature`)
* Create a Pull Request

## Status
Library is: _in progress_

## Contact
albert.lis.1996@gmail.com - feel free to contact me!
