import cv2
import numpy as np
from PIL import Image


def calc_average(image):
    img = cv2.imread(image)
    height, width, _ = np.shape(img)

    # calculate the average color of each row of our image
    avg_color_per_row = np.average(img, axis=0)

    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)
    # so, convert that array to integers
    int_averages = np.array(avg_colors, dtype=np.uint8)
    # avg_color is a tuple in BGR order of the average colors
    # but as float values
    print(f'avg_colors: {int_averages}')
    return int_averages

def calc_dominant(image):
    img = cv2.imread(image)
    height, width, _ = np.shape(img)
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]

    int_dominant = np.array(dominant, dtype=np.uint8)
    print(f'int_dominant: {int_dominant}')
    return int_dominant


def average_compare(image1 , image2 ):
    RGB1 = calc_average(image1)
    RGB2 = calc_average(image2)

    # if (int(RGB1[0]) > int(RGB2[0])):
    #     R_diff = int(RGB1[0]) - int(RGB2[0])
    #     R_diff = R_diff / 2.55
    #     print(R_diff)
    # else:
    #     R_diff = int(RGB2[0]) - int(RGB1[0])
    #     R_diff = R_diff / 2.55
    #     print(R_diff)
    #
    # if (int(RGB1[1]) > int(RGB2[1])):
    #     G_diff = int(RGB1[1]) - int(RGB2[1])
    #     G_diff = G_diff /2.55
    #     print(G_diff)
    # else:
    #     G_diff = int(RGB2[1]) - int(RGB1[1])
    #     G_diff = G_diff / 2.55
    #     print(G_diff)
    #
    # if (int(RGB1[2]) > int(RGB2[2])):
    #     B_diff = int(RGB1[2]) - int(RGB2[2])
    #     B_diff = B_diff / 2.55
    #     print(B_diff)
    # else:
    #     B_diff = int(RGB2[2]) - int(RGB1[2])
    #     B_diff = B_diff / 2.55
    #     print(B_diff)
    # similarity = 300 -G_diff - B_diff - R_diff
    # similarity = similarity /3
    # print(similarity)
    average1 = int(RGB1[0]) + int(RGB1[1]) + int(RGB1[2])
    average1 = average1/3
    average2 = int(RGB2[0]) + int(RGB2[1]) + int(RGB2[2])
    average2 = average2 / 3
    if (average1 > average2):
        similarity = average2 / average1
    else :
        similarity = average1 / average2


    return similarity *100

def dominant_compare(image1 , image2 ):
    RGB1 = calc_dominant(image1)
    RGB2 = calc_dominant(image2)
    dominant1 = int(RGB1[0]) + int(RGB1[1]) + int(RGB1[2])
    dominant1 = dominant1/3
    dominant2 = int(RGB2[0]) + int(RGB2[1]) + int(RGB2[2])
    dominant2 = dominant2 / 3
    if (dominant1 > dominant2):
        similarity = dominant2 / dominant1
    else :
        similarity = dominant1 / dominant2


    return similarity * 100








#####################################test #########################################
# original_image =  cv2.imread('1.jpg')
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

result = average_compare('colorpic.jpg','HP_train.jpg')
print(result)