from window_files.window import Window
import argparse

parser = argparse.ArgumentParser(description="Images to Fourier Series")
parser.add_argument("img_path", type=str, help="Path to image")
parser.add_argument("--image_visible", help="Specify if image should be visible while drawing fourier transform", action="store_true")
parser.add_argument("--path_disappears", help="Specify if path should be less visible over time", action="store_true")

args = parser.parse_args()

Window(args.img_path, args.image_visible, args.path_disappears)
