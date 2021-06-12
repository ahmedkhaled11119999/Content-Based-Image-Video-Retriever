import cv2
import numpy as np
from matplotlib import pyplot as plt


def normalize(input_array, size):
    output_array = np.zeros((256,), dtype=np.float64)
    total = 0
    for i, item in enumerate(input_array):
        output_array[i] = item / size
        total += item / size
    return output_array


def calc_hist_hsv(image):
    """
    :param image:
    :return:
    """
    hsv_base = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    channels = [0, 1]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    hist = cv2.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    return hist.tolist()


def hist_comp_hsv(hist1, hist2):
    """

    :param hist1:
    :param hist2:
    :return:
    """
    hist1 = np.array(hist1, dtype=np.float32)
    hist2 = np.array(hist2, dtype=np.float32)
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


def calculate_histogram(image):
    """
    take an opencv image and calculate its histogram and the normalize it
    :param image: opencv image (image = cv.imread())
    :return: histogram in this format
    histogram = [
        [[0.2], [0.4]] ...  # B channel
        [[0.2], [0.48]] ...  # G channel
        [[0.2], [0.48]] ...  # R channel
    ]
    """
    output = np.zeros(256, dtype=np.float64)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()
    cv_normalize = cv2.normalize(hist, hist).flatten()

    return cv_normalize


def histogram_compare(histogram1, histogram2):
    """
        return how well two histograms are similar, hist1 is 40% similar to hist2
        :param histogram1:
        :param histogram2:
        :return:
        """
    result = cv2.compareHist(histogram1, histogram2, cv2.HISTCMP_CORREL)
    return result


if __name__ == '__main__':
    image = cv2.imread("DB/storage/07.png")
    image2 = cv2.imread("DB/storage/06.png")

    # histogram1 = calculate_histogram(image)
    #
    #
    #
    #
    # histogram2 = calculate_histogram(image2)
    # #
    # # # print(histogram1.shape)
    # # # print(histogram2.shape)
    # #
    # # # calculate_histogram(image)
    # #
    # print(histogram_compare(histogram1, histogram2))

    hist1 = calc_hist_hsv(image)
    hist2 = calc_hist_hsv(image2)


    s = hist_comp_hsv(hist1, hist2)

    print(s)

    hist1 = calculate_histogram(image)
    hist2 = calculate_histogram(image2)

    s = histogram_compare(hist1, hist2)

    print(s)
