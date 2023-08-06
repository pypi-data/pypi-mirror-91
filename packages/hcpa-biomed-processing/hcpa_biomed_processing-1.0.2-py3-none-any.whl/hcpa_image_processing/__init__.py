import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from skimage import data
from skimage.color import separate_stains, combine_stains, hdx_from_rgb, rgb_from_hdx
import easygui
from os import path
import sys


def execute():
    threshold = int(sys.argv[1])
    paths = easygui.fileopenbox(multiple=True, title="Select the images")

    save_dir = easygui.diropenbox(title="Select the destination folder")

    for i in range(len(paths)):
        img_path = paths[i]

        img = Image.open(img_path)

        # Separate the stains from the IHC image
        img_stains = separate_stains(img, hdx_from_rgb)

        # Create an RGB image for our stain
        null_array = np.zeros_like(img_stains[:, :, 0])
        color_converted_img = combine_stains(
            np.stack((null_array, img_stains[:, :, 1], null_array), axis=-1),
            rgb_from_hdx,
        )

        color_converted_img_uint8 = (color_converted_img * 255).astype(np.uint8)

        color_converted_img_pil = Image.fromarray(color_converted_img_uint8, "RGB")

        # Converting image to Grayscale
        gray = color_converted_img_pil.convert("L")
        source = color_converted_img_pil.split()

        # Applying threshold
        bw = gray.point(lambda i: i < threshold and 255)

        img_dir = path.dirname(img_path)
        new_path = new_path = save_dir + "\\" + path.basename(img_path)
        if img_dir == save_dir:
            split_path = path.splitext(img_path)
            new_path = split_path[0] + "_processed" + split_path[1]

        print(new_path)
        bw.save(new_path)


execute()