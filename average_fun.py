import cv2
import numpy as np
from PIL import Image


def calc_average(image):
    """
    It calculates the average color of all the pixels in one image. In depth, this we load a pixel and unpack its
    individual color channels. Then we sum of the channel values into an accumulator then divide these sums by the
    number of all pixels.
    :param image:
    :return:
    """
    height, width, _ = np.shape(image)

    # calculate the average color of each row of our image
    avg_color_per_row = np.average(image, axis=0)

    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)
    # so, convert that array to integers
    int_averages = np.array(avg_colors, dtype=np.uint8)
    # avg_color is a tuple in BGR order of the average colors
    # but as float values
    # print(f'avg_colors: {int_averages}')
    return int_averages


def calc_dominant(image):
    """
    The dominant color is a descriptor that extract the color the most used in the image. In other words, the color of
    the pixels that have the maximum number in one image will represent the dominant color.
    :param image:
    :return:
    """
    height, width, _ = np.shape(image)
    pixels = np.float32(image.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]

    int_dominant = np.array(dominant, dtype=np.uint8)
    # print(f'int_dominant: {int_dominant}')
    return int_dominant


def color_compare(color1, color2):
    """
    return how well two colors are similar, color is 80% similar to color2
    :param color1:
    :param color2:
    :return:
    """
    avg_color1 = int(color1[0]) + int(color1[1]) + int(color1[2])
    avg_color1 = avg_color1 / 3
    avg_color2 = int(color2[0]) + int(color2[1]) + int(color2[2])
    avg_color2 = avg_color2 / 3

    if avg_color1 == avg_color2:
        similarity = 1
    elif avg_color1 > avg_color2:
        similarity = avg_color2 / avg_color1
    else:
        similarity = avg_color1 / avg_color2

    return similarity


if __name__ == '__main__':

    #####################################test #########################################
    original_image =  cv2.imread('1.jpg')
    # average = calc_average('1.jpg')
    # height, width, _ = np.shape(original_image)
    # dominant = calc_dominant('1.jpg')
    #
    # average_image = np.zeros((height, width, 3), np.uint8)
    # dominant_image = np.zeros((height, width, 3), np.uint8)
    #
    # average_image[:] = average
    # dominant_image[:] = dominant
    #
    #
    #
    # cv2.imshow("original image", np.hstack([original_image]))
    # cv2.imshow("Avg Color", np.hstack([average_image]))
    # cv2.imshow("dominant Color", np.hstack([dominant_image]))
    # cv2.waitKey(0)
