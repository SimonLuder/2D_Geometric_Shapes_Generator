# 2D Geometric shapes generator

A generator of 2D geometric shape data set, this data set is composed of a set of 
images stored in `png` files. Each image contains one of the following shapes : 
Square, Triangle, Circle, Star, Polygon, Heptagone, Hexagone, Octagone and Nonagon.

Each image is generated within the following parameters : 

- A fixed size (default 265x265 pixel)
- A fixed or random background colour (default black)
- A fixed or random filling colour of each shape (default white)
- A fixed or random rotation angle between -180° and 180° (default 0°)
- A fixed or random position inside of the containing image (default centered)
- A fixed or random perimeter (default 50% of image height)
- A prompt describing the image saved in prompts.csv

**All the parameters described above are generated for each sample independently 
and identically.** 


Run the data set generation with detault arguments:
```
python shape_generator.py
```

Run the data set generation with customized arguments :
```
python shape_generator.py --size 1000 --resolution 256 --destination ./data/YOUR_DATASET_NAME/ --randomize radius rotation fill_color bg_color position
```

The generation command may accept the following option : 

- `--size`: The number of generated images per each shape (default 1000)
- `--resolution`: The resolution of a generated image (res x res x 3) (default 256)
- `--destination`: The path of the folder where the generated images 
will be stored.
- `--randomize`: Randomized shape options: none or a selection of radius, rotation, fill_color, bg_color, position (default none)
