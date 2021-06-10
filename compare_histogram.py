import cv2
import numpy as np
from matplotlib import pyplot as plt


def normalize(input_array, size):
    output_array = np.zeros((256,), dtype=np.float64)
    # print(output_array.shape)
    total = 0
    for i, item in enumerate(input_array):
        output_array[i] = item / size
        total += item / size
    # print(total)
    return output_array


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
    our_normalize = normalize(hist, image.shape[0] * image.shape[1])

    cv_normalize = cv2.normalize(hist, hist).flatten()
    # plt.plot(our_normalize)
    # np.concatenate((output, our_normalize), axis=None)
    # # output += our_normalize
    #
    # hist = cv2.calcHist([image], [1], None, [256], [0, 256]).flatten()
    # our_normalize = normalize(hist, image.shape[0] * image.shape[1])
    # # hist = cv2.normalize(hist, hist).flatten()
    # plt.plot(our_normalize)
    # np.concatenate((output, our_normalize), axis=None)
    #
    # hist = cv2.calcHist([image], [2], None, [256], [0, 256]).flatten()
    # our_normalize = normalize(hist, image.shape[0] * image.shape[1])
    # cv_normalize = cv2.normalize(hist, hist)
    # print(cv_normalize)
    # np.concatenate((output, our_normalize), axis=None)
    #
    # plt.plot(our_normalize)
    # # plt.plot(cv_normalize)
    # plt.show()


    print(cv_normalize.shape)
    # return our_normalize
    return cv_normalize


def histogram_compare(histogram1, histogram2):
    """
        return how well two histograms are similar, hist1 is 40% similar to hist2
        :param histogram1:
        :param histogram2:
        :return:
        """
    print(histogram1.shape)
    print(histogram2.shape)
    # result = cv2.compareHist(histogram1, histogram2, cv2.HISTCMP_INTERSECT)
    result = cv2.compareHist(histogram1, histogram2, cv2.HISTCMP_CORREL)
    print(result)
    return result
    # return (result / 50388) * 100


if __name__ == '__main__':
    image = cv2.imread("DB/storage/05.jpg")
    image2 = cv2.imread("DB/storage/1.1.jpg")


    histogram1 = calculate_histogram(image)




    histogram2 = calculate_histogram(image2)
    #
    # # print(histogram1.shape)
    # # print(histogram2.shape)
    #
    # # calculate_histogram(image)
    #
    print(histogram_compare(histogram1, histogram2))
