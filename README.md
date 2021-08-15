# ImageToFourierSeries
Draw images as Fourier series

# How it works

Application first extracts edges from image. For this step it uses `Canny edge detector` 
implemented from scratch. Then it transforms image with extracted edges to the list of points to 
sort these points, so they create a path. Path is then passed to `discrete_fourier_transform` function
to transform this path to the set of epicycles. Then all it has to do is draw epicycles and track position
of the last epicycle. For visualizing this process I use `pygame` and `pygameZoom` (It gives ability to zoom into
pygame figures without quality loss and has a feature to track any point on canvas with specified zoom).
All algorithms are written in `Cython` which is much faster then 
pure python.

Useful links so you can better understand this algorithm:

`Canny edge detector`:
 - https://en.wikipedia.org/wiki/Canny_edge_detector
 - https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123

`Discrete fourier transform`:
 - https://www.youtube.com/watch?v=7_vKzcgpfvU
 - https://en.wikipedia.org/wiki/Discrete_Fourier_transform

# Example

If you feed this image to program,

![Face](https://github.com/Grzetan/ImageToFourierSeries/blob/master/src/face.jpeg)

You will get this:

![Video](https://github.com/Grzetan/ImageToFourierSeries/blob/master/src/face.mp4)

# Usage

Install requirements:
```commandline
pip3 install -r requirements.txt
```

Setup cython functions:

```commandline
python3 setup.py build_ext --inplace
```

Run main.py 

```commandline
python3 main.py img_path=path/to/image
```

# Modify output with flags

 - Use `--static_path` if you want path to not lose color over time


 - Use `--reset_path` if you want path to reset every cycle.


 - Use `--image_visibility=VISIBLE` if you want to see image as the background.


 - Use `--image_visibility=NOT_VISIBLE` (default) if you don't want image to be visible in the background

# Video options

 - Use `--save_as_video` if you want to save result to MP4 file. It will save in current directory with name
`ImageToFourierSeries-1629031103830.mp4`. This long number represents current timestamp.


 - Use `--custom_recording` if you want to decide when the video ends by simply closing window. By default, it will end 
when one full cycle is completed.

    
 - Use `--cycle_duration=duration` where `duration` is a number to specify duration of one cycle (in seconds). It 
can be useful when you want to slow down animation (visible only on video). Default is 30 seconds, so anything greater than 30 will slow down animation
and anything lower will speed it up.