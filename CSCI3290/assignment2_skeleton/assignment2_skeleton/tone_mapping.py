#
# CSCI3290 Computational Imaging and Vision *
# --- Declaration --- *
# I declare that the assignment here submitted is original except for source
# material explicitly acknowledged. I also acknowledge that I am aware of
# University policy and regulations on honesty in academic work, and of the
# disciplinary guidelines and procedures applicable to breaches of such policy
# and regulations, as contained in the website
# http://www.cuhk.edu.hk/policy/academichonesty/ *
# Assignment 2
# Name : Wong Wai Chun 
# Student ID : 1155173231
# Email Addr : 1155173231@link.cuhk.edu.hk
#

import math
import cv2
import numpy as np
import os
import sys
import argparse


class ArgParser(argparse.ArgumentParser):
    """ ArgumentParser with better error message

    """

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def hdr_read(filename: str) -> np.ndarray:
    """ Load a hdr image from a given path

    :param filename: path to hdr image
    :return: data: hdr image, ndarray type
    """
    data = cv2.imread(filename, cv2.IMREAD_ANYDEPTH)
    assert data is not None, "File {0} not exist".format(filename)
    assert len(data.shape) == 3 and data.shape[2] == 3, "Input should be a 3-channel color hdr image"
    return data


def ldr_write(filename: str, data: np.ndarray) -> None:
    """ Store a ldr image to the given path

    :param filename: target path
    :param data: ldr image, ndarray type
    :return: status: if True, success; else, fail
    """
    return cv2.imwrite(filename, data)


def compute_luminance(input: np.ndarray) -> np.ndarray:
    """ compute the luminance of a color image

    :param input: color image
    :return: luminance: luminance intensity
    """
    luminance = 0.2126 * input[:, :, 0] + 0.7152 * input[:, :, 1] + 0.0722 * input[:, :, 2]
    return luminance


def map_luminance(input: np.ndarray, luminance: np.ndarray, new_luminance: np.ndarray) -> np.ndarray:
    """ use contrast reduced luminace to recompose color image

    :param input: hdr image
    :param luminance: original luminance
    :param new_luminance: contrast reduced luminance
    :return: output: ldr image
    """
    # write you code here
    # to be completed
    
    # write you code here
    result = np.zeros([input.shape[0], input.shape[1], input.shape[2]])

    for i in range(input.shape[0]):
        for j in range(input.shape[1]):
            result[i][j][0] = input[i][j][0] * new_luminance[i][j]/ luminance[i][j]
            result[i][j][1] = input[i][j][1] * new_luminance[i][j]/ luminance[i][j]
            result[i][j][2] = input[i][j][2] * new_luminance[i][j]/ luminance[i][j]

    output = np.array(result)
    # write you code here
    return output


def he_tonemap(input: np.ndarray) -> np.ndarray:
    """ global tone mapping with histogram equalization operator

    :param input: hdr image
    :return: output: ldr image, value range [0, 1]
    """
    # write you code here
     
    # Compute luminance from the HDR image
    luminance = compute_luminance(input)

    # Compute histogram of the luminance image using a fixed
    #  number of bins
    histogram, bin_edges = np.histogram(luminance, bins=2048, range=(0, np.max(luminance)))

    # Compute cumulative histogram (normalized)
    cumulative = np.cumsum(histogram)
    cumulative_normalized = cumulative / cumulative[-1]

    # Map the luminance image through the normalized cumulative histogram
    ldr_image = np.interp(luminance.flatten(), bin_edges[:-1], cumulative_normalized)

    # # Reshape the LDR image back to the original shape (excluding the color channels)
    ldr_image_m = ldr_image.reshape(luminance.shape)

    # Normalize the LDR image to be in range [0, 1] if necessary
    ldr_image /= ldr_image.max()
    ldr_image = map_luminance(input,luminance, ldr_image_m )

    return ldr_image



def bilateral_filter(input: np.ndarray, size: int, sigma_space: float, sigma_range: float) -> np.ndarray:
    """ local tone mapping with durand's operator (bilateral filtering)

    :param input: input image/map
    :param size: windows size for spatial filtering
    :param sigma_space: filter sigma for spatial kernel
    :param sigma_range: filter sigma for range kernel
    :return: output: filtered output
    """
    # write you code here
    # to be completed

    # write you code here

    r = size//2
    h, w = input.shape
    test = np.copy(input)
    test = np.pad(test, ((r,r),(r,r)), 'reflect').astype(np.float64)

    temp = np.zeros_like(input)
    #spatial gaussian function (2D gaussian kernel)
    kernel_space = np.zeros(shape=[size, size], dtype=float)
    kernel_max = size//2+1
    kernel_min = 0-kernel_max+1
    x,y = np.mgrid[kernel_min:kernel_max , kernel_min:kernel_max]

    kernel_space = np.exp(-(x*x+y*y)/(2*sigma_space*sigma_space))
    kernel_space = kernel_space / kernel_space.sum() #normalized
    
    for y in range(r,r+h):
        for x in range(r,r+w):
            target = test[y-r:y+r+1,x-r:x+r+1]  #target kernel center at [y,x] (I(xi))

            #range kernel (1D gaussian kernel)
            intensityDiff = (target-test[y,x])   #(I(xi)-I(x))
            #take gaussian
            product = (intensityDiff*intensityDiff)/(2*sigma_range*sigma_range)
            LUT = np.exp(-product)  #Look Up Table
            kernel_range = LUT/LUT.sum() #normalized

            divide = kernel_range * kernel_space  #k(x)
            combine = divide * target
            temp[y-r][x-r]= (np.sum(combine)) / np.sum(divide)
    
    output = np.array(temp)
    # write you code here
    return output

def test():
    input_image = np.random.rand(100, 100, 3)  # A random image with values [0, 1]

    # Assume these are the calculated parameters for your image.
    size = 5
    sigma_space = 15
    sigma_range = 0.1

    # Apply custom bilateral filter
    custom_filtered_image = bilateral_filter(input_image, size, sigma_space, sigma_range)

    # Apply OpenCV bilateral filter
    opencv_filtered_image = cv2.bilateralFilter(input_image.astype(np.float32), size, sigmaColor=sigma_range*255, sigmaSpace=sigma_space)

    # Calculate the difference between the two outputs
    difference = cv2.norm(custom_filtered_image.astype(np.float32) - opencv_filtered_image, cv2.NORM_L2)

    print(f"Difference between custom and OpenCV implementation: {difference}")


def durand_tonemap(input: np.ndarray) -> np.ndarray:
    """ local tone mapping with durand's operator (bilateral filtering)

    :param input: hdr image
    :return: output: ldr image, value range [0, 1]
    """
    # write you code here
    # to be completed

    # write you code here
    luminace = compute_luminance(input)
    logIntensity = np.log10(luminace)
    #print(logIntensity)

    sigma_space = 0.02 * min(input.shape[0], input.shape[1])
    sigma_range = 0.4
    kernel_size = 2 * max(round(1.5*sigma_space),1) + 1

    #filter with bilaterial filter
    baseLayer = bilateral_filter(logIntensity, size = kernel_size,sigma_space = sigma_space, sigma_range = sigma_range)

    detail = logIntensity - baseLayer
    contrast = 50 #user-controllable parameter
    delta = np.amax(baseLayer) - np.amin(baseLayer)

    gamma = math.log10(contrast) / delta
    #print(gamma)

    reconstruct = np.power(10, gamma * baseLayer + detail)
    divideBy = np.power(10, np.amax(gamma*baseLayer))
    displayLum = reconstruct / divideBy

    result = map_luminance(input, luminace, displayLum)
    output = np.array(result)

    return output


# operator dictionary
op_dict = {
    "durand": durand_tonemap,
    "he": he_tonemap
}

# if __name__ == "__main__":
#     test()


#py tone_mapping.py .\test_images\doll.hdr --op all

if __name__ == "__main__":
    # read arguments
    parser = ArgParser(description='Tone Mapping')
    parser.add_argument("filename", metavar="HDRImage", type=str, help="path to the hdr image")
    parser.add_argument("--op", type=str, default="all", choices=["durand", "he", "all"],
                        help="tone mapping operators")
    args = parser.parse_args()
    # print banner
    banner = "CSCI3290, Spring 2024, Assignment 2: tone mapping"
    bar = "=" * len(banner)
    print("\n".join([bar, banner, bar]))
    # read hdr image
    image = hdr_read(args.filename)


    # define the whole process for tone mapping
    def process(op: str) -> None:
        """ perform tone mapping with the given operator

        :param op: the name of specific operator
        :return: None
        """
        operator = op_dict[op]
        # tone mapping
        result = operator(image)
        # gamma correction
        result = np.power(result, 1.0 / 2.2)
        # convert each channel to 8bit unsigned integer
        result_8bit = np.clip(result * 255, 0, 255).astype('uint8')
        # store the result
        target = "output/{filename}.{op}.png".format(filename=os.path.basename(args.filename), op=op)
        msg_success = lambda: print("Converted '{filename}' to '{target}' with {op} operator.".format(
            filename=args.filename, target=target, op=op
        ))
        msg_fail = lambda: print("Failed to write {0}".format(target))
        msg_success() if ldr_write(target, result_8bit) else msg_fail()


    if args.op == "all":
        [process(op) for op in op_dict.keys()]
    else:
        process(args.op)
