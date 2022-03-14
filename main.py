import os
import sys
import cv2
import numpy as np
import region_growing as rg

"""
################################################################################
#####################     PARSING USER ARGUMENTS       #########################
################################################################################
"""

path_input_image     = ""
path_output_sequence = ""
num_sigma            = 3
sigma_noise          = 0.

while len(sys.argv)>1:
    flag = sys.argv[1]

    del sys.argv[1]

    if flag.lower()=="-path_input":
        path_input_image = sys.argv[1]

        del sys.argv[1]
    elif flag.lower()=="-num_sigma":
        num_sigma = int(sys.argv[1])

        del sys.argv[1]
    elif flag.lower()=="-sigma_noise":
        sigma_noise = float(sys.argv[1])

        del sys.argv[1]
    elif flag.lower()=="-path_output":
        path_output_sequence = sys.argv[1]

        del sys.argv[1]

"""
################################################################################
#####################     MAIN AND AUX FUNCTIONS       #########################
################################################################################
"""
"""
    |-----------------------------------|
    |   check_if_there_is_sequence_dir  |
    |-----------------------------------|

    Checks if there is a valid directory where sequence frames are to be saved.
    If there is not such directory, a new one will be created. If there is
    already a directory named '/sequence', then a new one is created, with a
    random number appended to its name
"""
def check_if_there_is_sequence_dir(path_output=path_output_sequence):
    if os.path.isdir(path_output)==False:
        aux_str = ">> Directory to save sequence frames not found. Creating one"

        print(aux_str)

        path_output = os.path.join(os.path.curdir, "sequence")

        try:
            os.mkdir(path=path_output)
        except FileExistsError:
            print("ayiu")
            random_indice = np.random.randint(low=0,
                                              high=1000000)

            path_output += "_{:6d}".format(random_indice)

            aux_str = ">> The informed directory already exists. Files will be"
            aux_str = " saved in the {:s} folder".format(path_output)

            print(aux_str)

            os.mkdir(path=path_output)

"""
    |----------------------------------|
    |   check_if_there_is_input_image  |
    |----------------------------------|

    Checks if there is a valid file to be used as input image. If this is not
    the case, an exception is raised and applications breaks.
"""
def check_if_there_is_input_image(path_input):
    if os.path.isfile(path_input):
        aux_str = ">> Image file detected. Moving on"

        print(aux_str)
    else:
        aux_str = ">> File not found. Exiting application"

        raise FileNotFoundError(aux_str)

"""
    |-----------------------------|
    |   corrupt_image_with_noise  |
    |-----------------------------|

    Corrupts the input image with random Gaussian noise centered at zero with
    standar deviation given by sigma_noise
"""

def corrupt_image_with_noise(input_image,
                             sigma=sigma_noise):

    noise = np.random.normal(loc=0.,
                             scale=sigma,
                             size=input_image.shape)

    output_image = input_image + noise

    return output_image

"""
    |-----------|
    |   main    |
    |-----------|
"""

def main():
    check_if_there_is_input_image(path_input=path_input_image)

    check_if_there_is_sequence_dir(path_output=path_output_sequence)

    aux_str = ">> Reading image as grayscale and normalizing it"

    print(aux_str)

    img_in = cv2.imread(filename=path_input_image, flags=0)
    img_in = img_in.astype(np.float32)
    img_in = img_in/img_in.max()

    aux_str = ">> Done"

    print(aux_str)

    if sigma_noise>0.:
        aux_str = ">> Degrading image with noise"

        print(aux_str)

        img_in = corrupt_image_with_noise(input_image=img_in,
                                          sigma=sigma_noise)

        aux_str = ">> Done"

        print(aux_str)

    # auxiliary image to receive seed annotation
    ann_img = img_in.copy()

    cv2.namedWindow("Input image", flags=cv2.WINDOW_AUTOSIZE)

    aux_str = ">> Double click with mouse left button over a single point of"
    aux_str += " the input image selects the seed point. After picking this"
    aux_str += " coordinate close the visualization pressing ESC key"

    print(aux_str)

    cv2.setMouseCallback(window_name="Input image",
                         on_mouse=rg.plant_seed,
                         param=(ann_img,))
    while(1):
        cv2.imshow("Input image", ann_img)

        if (cv2.waitKey(10) & 0xFF)==27:
            break

    cv2.destroyWindow(winname="Input image")

    seed_img = rg.generate_initial_seed_image(input_image=img_in,
                                              coordinates=rg.seed_coordinates)

    cv2.namedWindow("Seed image", flags=cv2.WINDOW_AUTOSIZE)

    cv2.imshow("Seed image", seed_img)

    img_out = rg.grow_region(input_image=img_in,
                             seed_image=seed_img,
                             num_sigma=num_sigma,
                             path_output_sequence=path_output_sequence)

    cv2.namedWindow("Final image", flags=cv2.WINDOW_AUTOSIZE)

    cv2.imshow("Final image", img_out)

    if (cv2.waitKey(0) & 0xFF)==27:
        cv2.destroyAllWindows()

    aux_str = ">> End"

    print(aux_str)

"""
    ****************************************************************************
    ***********************         MAIN        ********************************
    ****************************************************************************
"""

if __name__=="__main__":
    main()