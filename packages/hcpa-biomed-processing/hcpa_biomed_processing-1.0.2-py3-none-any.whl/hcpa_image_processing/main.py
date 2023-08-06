import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from skimage import data
from skimage.color import separate_stains, combine_stains, hdx_from_rgb, rgb_from_hdx
import easygui
from os import path
import sys

threshold = int(sys.argv[1])
paths = easygui.fileopenbox(multiple=True)

save_dir = easygui.diropenbox()

# Example IHC image
for i in range(len(paths)):
    img_path = paths[i]

    img = Image.open(img_path)

    # Separate the stains from the IHC image
    img_stains = separate_stains(img, hdx_from_rgb)

    # Create an RGB image for our stain
    null_array = np.zeros_like(img_stains[:, :, 0])
    color_converted_img = combine_stains(
        np.stack((null_array, img_stains[:, :, 1], null_array), axis=-1), rgb_from_hdx
    )

    color_converted_img_uint8 = (color_converted_img * 255).astype(np.uint8)

    color_converted_img_pil = Image.fromarray(color_converted_img_uint8, "RGB")
    color_converted_img_pil

    gray = color_converted_img_pil.convert("L")
    source = color_converted_img_pil.split()

    bw = gray.point(lambda i: i < threshold and 255)
    new_path = save_dir + "\\" + path.basename(img_path)
    print(new_path)
    bw.save(new_path)

# img_arr = np.asarray(bw)
# plt.imshow(bw, cmap="gray", vmin=0, vmax=255)
# plt.show()
