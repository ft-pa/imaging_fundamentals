# region_growing
A routine that implements a region growing algorithm based on mathematical morphology

## Concepts
Region growing is a classical technique in which, based on the properties of an initial ("seed") point, pixels from its neighborhoods are labeled as pertaining or not pertaining to a region. The processs is carried out iteratively, until there is no more any noticeable change in the classified ("binarized") image.
While the decision criterion varies from application to application, here a pixel is considered to belong to a region if its value lies fullfils the condition

![intensity criterion](etc/eq_span_interval.png)

## Howto
The code possess three input parameters that must be passed by flags
| flag          | default value | description |
|---------------|---------------|-------------|
| `-path_input` | `""`          | **absolute** path to the input image |
| `-path_output`| `""`          | **absolute** path to the output directory, where sequence frames are to be saved |
| `-num_sigma`  | `3`           | the number of sigma (standard deviation; please see explanation above) that spans the interval of analysis |
| `-sigma_noise`| `0.`          | noise standard deviation |

In order to execute this study, the user must call Python through the command line, passing the parameters via flags. An example would be
```
python3  python3 main.py -path_input <path_to_input_image> -sigma_noise 0 -path_output <path_to_output_image>
```
Notice that the order of the flags is immaterial. The script will parse them properly.
