import os
import cv2
import numpy as np

seed_coordinates    = None
visited_coordinates = None

"""
    |---------------|
    |   plant_seed  |
    |---------------|

    Allows used to select a coordinate by clicking on it and then draws a
    circle on that point
"""
def plant_seed(event,
               x,
               y,
               flags,
               param):
        img = param[0]

        global seed_coordinates

        if event==cv2.EVENT_LBUTTONDBLCLK:
            str_aux = ">> Point coordinates [in px]: ({:d}, {:d})".format(y, x)

            print(str_aux)

            seed_coordinates = (y, x)

            cv2.circle(img,
                       center=(x,y),
                       radius=5,
                       color=1.,
                       lineType=cv2.LINE_4)

"""
    |-----------------------------------|
    |   generate_initial_seed_image     |
    |-----------------------------------|

    Returns a binary image where the only non-null pixel is the one whose
    coordinates coincide with the one given by user
"""
def generate_initial_seed_image(input_image, coordinates):
    output_image = np.zeros_like(input_image)

    output_image[coordinates[0], coordinates[1]] = 1.

    return output_image

"""
    |-------------------|
    |   grow_region     |
    |-------------------|
"""
def grow_region(input_image,
                seed_image,
                num_sigma=3,
                path_output_sequence="./"):

    num_rows, num_cols = input_image.shape[0 : 2]

    # structuring element
    struct_el = np.ones((3, 3), dtype=np.uint8)

    output_image  = seed_image.copy()
    output_image  = output_image.astype(np.uint8)

    k = 0

    seq_img_out = np.zeros((num_rows, num_cols, 3), dtype=np.float32)

    for i in range(0, 3):
        seq_img_out[:, :, i] = input_image

    while 1:
        former_output = output_image.copy()

        aux = former_output.copy()

        if aux.max()!=0:
            aux = aux/aux.max()

        seq_img_out[:, :, 2] = np.maximum(aux,
                                          input_image)

        seq_frame = seq_img_out.copy()
        seq_frame = cv2.normalize(src=seq_img_out,
                                  dst=seq_frame.astype(np.uint8),
                                  alpha=255,
                                  beta=0,
                                  norm_type=cv2.NORM_MINMAX)

        file_name = "frame_{:04d}.png".format(k)
        path_file = os.path.join(path_output_sequence, file_name)

        cv2.imwrite(filename=path_file, img=seq_frame)

        output_image = cv2.dilate(src=output_image,
                                  dst=output_image,
                                  kernel=struct_el,
                                  anchor=(-1,-1))

        bool_nonzero = output_image != 0.

        mu = input_image[bool_nonzero].mean()
        si = input_image[bool_nonzero].std()

        mask = np.abs(input_image-mu)<=num_sigma*si
        mask = mask.astype(np.float32)

        output_image = output_image.astype(np.float32)
        output_image = output_image/output_image.max()

        output_image = output_image*mask

        if np.all(former_output==output_image):
            break

        k += 1

    return output_image.astype(np.float32)