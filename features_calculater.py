import json

from db import DB
from average_fun import calc_average, calc_dominant, average_compare, dominant_compare
from test_key_extraction import extract_key_frames
from object_detection import extract_objects
from compare_histogram import calculate_histogram, histogram_compare

import numpy as np
import cv2 as cv
import os

db = DB()


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
    if avg_color1 > avg_color2:
        similarity = avg_color2 / avg_color1
    else:
        similarity = avg_color1 / avg_color2
    return similarity


def calculate_image_features(image):
    image_features = {
        'shape': (image.shape[0], image.shape[1]),
        'avg_color': calc_average(image).tolist(),
        'dominate_color': calc_dominant(image).tolist(),
        'histogram': calculate_histogram(image),
        'objects': extract_objects(image)
    }
    image_features['dominant_color'] = image_features['avg_color']
    return image_features


def get_image_features(path):
    image = cv.imread(path)
    features = calculate_image_features(image)
    return features


def get_video_features(path):
    frames = extract_key_frames(path)
    frames_features = []
    for frame in frames:
        features = calculate_image_features(frame)
        features['parent_video_path'] = path
        frames_features.append(features)
    return frames_features


def compare_two_images(image1_features, image2_features):
    """
    return
    :param image1_features:
    :param image2_features:
    :return:
    """
    average_color = color_compare(image1_features.get('avg_color'),
                                  image2_features.get('avg_color'))

    xx = image2_features.get('dominant_color')
    dominant_color = color_compare(image1_features.get('dominant_color'),
                                   xx)

    histogram = histogram_compare(image1_features.get('histogram'),
                                  image2_features.get('histogram'))
    common_objects = set(image2_features.get('objects')).intersection(image1_features.get('objects'))

    return {
        'average_color': average_color,
        'dominant_color': dominant_color,
        'histogram': histogram,
        'common_objects': list(common_objects)
    }


def search_by_image(path):
    """
    Take an image and calculate the image features, and compare the precalculated images features in the db and return
    list of each image similarity
    :param path:
    :return:
    """
    similarity = []
    query_image_feature = get_image_features(path)
    # images_features = db.get_all({'$not': {'path': None}})
    images_features = db.get_all({})
    for image_features in images_features:
        im = cv.imread(image_features.get('path'))
        image_features['histogram'] = calculate_histogram(im)
        similar_image = compare_two_images(query_image_feature, image_features)
        similar_image['path'] = image_features['path']

        similarity.append(similar_image)

    return similarity


def sort_by(similarity, feature):
    similarity.sort(key=lambda image: image.get(feature), reverse=True)
    return similarity


def add_dataset(dir_path):
    for entry in os.scandir(dir_path):
        if entry.is_dir():
            continue
        features = calculate_image_features(cv.imread(entry.path))
        features['path'] = entry.path
        print(f'finished: {entry.name}')

        # print(features)
        features['histogram'] = []
        db.insert_image(features)


if __name__ == '__main__':
    path = "D:/Media/Gallery/GOT/Game Of Thrones"
    # add_dataset(path)

    similarity = search_by_image("C:/Users/Legion/Desktop/01.jpg")

    similarity = sort_by(similarity, 'average_color')

    for i, image in enumerate(similarity):
        cv.imshow(f'{i}, {image.get("average_color")}, {image.get("path")}', cv.imread(image.get("path")))

        cv.waitKey(0)
