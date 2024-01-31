# 2D Geometric shapes generator

## Info
A generator of 2D geometric shape data set, this data set is composed of a set of 
images stored in `png` files. Each image contains one of the following shapes : 
Square, Triangle, Circle, Star, Polygon, Heptagon, Hexagon, Octagon and Nonagon.

Each image is generated within the following parameters : 

- A fixed size (default 265x265 pixel)
- A fixed or random background colour (default black)
- A fixed or random filling colour of each shape (default white)
- A fixed or random aspect ratio of the shape W / H between 0.5 and 2 (default 1)
- A fixed or random rotation angle between -180° and 180° (default 0°)
- A fixed or random position inside of the containing image (default centered)
- A fixed or random perimeter (default 50% of image height)
- A prompt describing the image saved in prompts.csv

**All the parameters described above are generated for each sample independently 
and identically.** 

## Generating new Samples
Run the data set generation with detault arguments:
```
python shape_generator.py
```

Run the data set generation with customized arguments :
```
python shape_generator.py --size 1000 --resolution 256 --destination /YOUR_DESTINATION_PATH/ --randomize radius aspect_ratio rotation fill_color bg_color position
```

The generation command may accept the following option : 

- `--size`: The number of generated images per each shape (default 1000)
- `--resolution`: The resolution of a generated image (res x res x 3) (default 256)
- `--destination`: The path of the folder where the generated images 
will be stored.
- `--randomize`: Randomized shape options: `none` or a selection of `radius`, `rotation`, `ill_color`, `bg_color`, `position` (default is none)


Train Set :
```
python shape_generator.py --size 1000 --resolution 256 --destination ./data/train256/ --randomize radius aspect_ratio rotation position
```

Validation Set :
```
python shape_generator.py --size 5 --resolution 256 --destination ./data/val256/ --randomize radius aspect_ratio rotation position
```

Test Set :
```
python shape_generator.py --size 12 --resolution 256 --destination ./data/test256/ --randomize radius aspect_ratio rotation position
```

## Disclaimer
This repository is strongly inspired by [elkorchi/2DGeometricShapesGenerator](https://github.com/elkorchi/2DGeometricShapesGenerator). It includes main functionalities from this repository but extends them in the context of an image-text and image-label dataset, which could be used in training a conditional generative model. The images are now generated using opencv instead of turtle.