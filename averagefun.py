import cv2
import numpy as np


def calc_average(image):
    height, width, _ = np.shape(image)

    # calculate the average color of each row of our image
    avg_color_per_row = np.average(image, axis=0)

    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)
    # so, convert that array to integers
    int_averages = np.array(avg_colors, dtype=np.uint8)
    # avg_color is a tuple in BGR order of the average colors
    # but as float values
    print(f'avg_colors: {int_averages}')
    return int_averages


def calc_dominant(image):
    height, width, _ = np.shape(image)
    pixels = np.float32(image.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]

    int_dominant = np.array(dominant, dtype=np.uint8)
    print(f'int_dominant: {int_dominant}')
    return int_dominant


def calc_hist(image):
    hist = []
    for i in range(3):
        histr = cv2.calcHist([image], [i], None, [256], [0, 256]).tolist()
        hist.append(histr)
        cv2.normalize(histr, histr)
        print(histr.shape)
    return hist


if __name__ == '__main__':
    path = 'DB/storage/1.jpg'

    original_image = cv2.imread(path)
    average = calc_average(path)
    height, width, _ = np.shape(original_image)
    dominant = calc_dominant(path)
    print(f'average: {average}')
    print(f'dominant: {dominant}')

    average_image = np.zeros((height, width, 3), np.uint8)
    dominant_image = np.zeros((height, width, 3), np.uint8)

    average_image[:] = average
    dominant_image[:] = dominant

    cv2.imshow("original image", np.hstack([original_image]))
    cv2.imshow("Avg Color", np.hstack([average_image]))
    cv2.imshow("dominant Color", np.hstack([dominant_image]))
    cv2.waitKey(0)
