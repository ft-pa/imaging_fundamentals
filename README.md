# image_analysis_fundamentals
A few routines for those who seek to understand some of the fundamentals of image analysis

## Howto
Techniques will be divided inot three categories:
+ Segmentation
+ Enhancement (to appear)
+ Geometry (to appear)

Inside each directory there are stand-alone scripts, _i.e._, `main.py` files that combined with their associated modules allow the user to run a number of experiments.

For example, in order to try image segmentation through the usage of a region growing method, it suffices to download the content available on `segmentation/region_growing` and run the file `main.py`on a terminal, giving the code proper input parameters. Simple testing images are provided, but the user is encouraged trying and adapting codes as much he/she needs.

## Dependencies

All codes in this repository were writen using
- Python 3.9.1;
- OpenCV 4.5.0; and
- Numpy 1.20.0.

Tests were ran on a Linux terminal. If you have any troubles with file I/O, it may be possible that exist one or more paths with OS-dependent formats in the codes. While [os.path](https://docs.python.org/3.9/library/os.path.html#module-os.path) was extensively used, eventually some "Linux-driven-hard-coded" directive might have passed anyway.
