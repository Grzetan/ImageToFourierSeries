from window_files.window import Window
import argparse
from functions.ImageVisibility import ImageVisibility

parser = argparse.ArgumentParser(description="Images to Fourier Series")
parser.add_argument("img_path", type=str, help="Path to image")
parser.add_argument("--image_visibility", type=str, default="NOT_VISIBLE", help="Specify if image should be visible while drawing fourier "
                                                     "transform or maybe it should pop up when drawing is done")
parser.add_argument("--static_path", help="Specify if path should not be less visible over time", action="store_true")
parser.add_argument("--reset_path", help="Specify if path should reset with each full cycle", action="store_true")

args = parser.parse_args()
try:
    args.image_visibility = ImageVisibility[args.image_visibility]
except:
    print("Wrong image_visibility value!!! You can only use:")
    for x in ImageVisibility:
        print(x.name)
    exit()

Window(args.img_path, args.image_visibility, args.static_path, args.reset_path)
