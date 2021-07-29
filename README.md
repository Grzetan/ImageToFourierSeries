# ImageToFourierSeries
Draw images as Fourier series

# How it works

Application first extracts edges from image. For this step it uses `Canny edge detector` 
implemented from scratch. Then it transforms image with extracted edges to the list of points to 
sort these points, so they create a path. Path is then passed to `discrete_fourier_transform` function
to transform this path to the set of epicycles. Then all it has to do is draw epicycles and track position
of the last epicycle. For visualizing this process I use `pygame` and `pygameZoom` (It gives ability to zoom into
pygame figures without quality loss and has a feature to track any point on canvas with specified zoom).

Useful links so you can better understand this algorithm:

`Canny edge detector`:
 - https://en.wikipedia.org/wiki/Canny_edge_detector
 - https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123

`Discrete fourier transform`:
 - https://www.youtube.com/watch?v=7_vKzcgpfvU
 - https://en.wikipedia.org/wiki/Discrete_Fourier_transform

# Usage

Install requirements:
```commandline
pip3 install -r requirements.txt
```

Run main.py 

```commandline
python3 main.py img_path=path/to/image
```

# Modify output with flags

 - Use `--static_path` if you want path to not lose color over time


 - Use `--reset_path` if you want path to reset every cycle.


 - Use `--image_visibility=VISIBLE` if you want to see image as the background.


 - Use `image_visibility=NOT_VISIBLE` (default) if you don't want image to be visible in the background