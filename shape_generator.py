import os
import argparse
from time import time
from shapes import GeometricShapes
from pathlib import Path



if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=10, help="Number of generated images per each shape")
    parser.add_argument('--resolution', type=int, default=256, help="Image resolution (res x res x 3")
    parser.add_argument('--destination', type=str, default=f"./data/{time():.0f}/", help="Storage path")
    parser.add_argument('--randomize', type=str, nargs='+', default="none", 
                        help='Randomized options: none or a selection of radius, rotation, fill_color, bg_color, position')

    args = parser.parse_args()

    # create destination dir if doesn't exist
    Path(args.destination).mkdir(parents=True, exist_ok=True)
    
    # randomized parameters
    if args.randomize == "none":
        args.randomize = []

    # start generating
    shapes_generator = GeometricShapes(destination=args.destination, 
                                       class_size=args.size, 
                                       img_res=args.resolution,
                                       randomize=args.randomize
    )
    shapes_generator.generate()