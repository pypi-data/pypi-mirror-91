# Colorblind

Colorblind is a computer vision library that converts images into a
colorblind friendly version depending on the type of colorblindness.
The three supported types of colorblindness/color weakness are:

* Deuteranopia: green weakness
* Protanopia: red weakness
* Tritanopia: blue weakness (extremely rare)

So far we provide three algorithms to correct the images:

* Daltonization: Original method for generating colorblind-friendly images
* HSV Hue Shift: Shifts Hue based on green ratio or blue ratio (depending on colorblindness type)
* LAB Shift: Previous studies for this had to tune hyperparameters to get good results


## Installation

```
pip install colorblind
```

## Usage
```
# imports
import numpy as np
import cv2
from colorblind import colorblind
import matplotlib.pyplot as plt

# load image
img = cv2.imread('../images/seven.jpg')
img = img[..., ::-1]

# simulate protanopia
simulated_img = colorblind.simulate_colorblindness(img, colorblind_type='protanopia')

# correct using daltonization
daltonized_img = colorblind.daltonize_correct(img, colorblind_type='protanopia')

# correct using hsv correction
hsv_img = colorblind.hsv_color_correct(img, colorblind_type='protanopia')
```

## Results

### Deuteranopia
| Type | Original | Daltonization | HSV Corrected |
|----------|------------|---------------|---------------|
| Full Color |![](images/seven.jpg) | ![](images/duteranopia_daltonized_img.jpg) | ![](images/protanopia_hsv_img.jpg) |
| Simulated | ![](images/duteranopia_img.jpg) | ![](images/duteranopia_daltonized_view_img.jpg) | ![](images/duteranopia_hsv_view_img.jpg) |

### Protanopia
| Type | Original | Daltonization | HSV Corrected |
|----------|------------|---------------|---------------|
| Full Color |![](images/seven.jpg) | ![](images/protanopia_daltonized_img.jpg) | ![](images/protanopia_hsv_img.jpg) |
| Simulated | ![](images/protanopia_img.jpg) | ![](images/protanopia_daltonized_view_img.jpg) | ![](images/protanopia_hsv_view_img.jpg) |

### Tritanopia
| Type | Original | Daltonization | HSV Corrected |
|----------|------------|---------------|---------------|
| Full Color |![](images/seven.jpg) | ![](images/tritanopia_daltonized_img.jpg) | ![](images/tritanopia_hsv_img.jpg) |
| Simulated | ![](images/tritanopia_img.jpg) | ![](images/tritanopia_daltonized_view_img.jpg) | ![](images/tritanopia_hsv_view_img.jpg) |

## Credits

Mostly inspired by a summary paper of algorithms applicable to making images color-blind friendly.
Example: https://www.researchgate.net/publication/326626897_Smartphone_Based_Image_Color_Correction_for_Color_Blindness

Daltonization values came from https://github.com/joergdietrich/daltonize

Further information on color blindness is available at:
* https://ixora.io/projects/colorblindness/color-blindness-simulation-research/
* http://www.daltonize.org/
