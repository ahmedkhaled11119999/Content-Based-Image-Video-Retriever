from db import DB
from average_fun import calc_average, calc_dominant, average_compare, dominant_compare
from test_key_extraction import extract_key_frames
from object_detection import extract_objects
from compare_histogram import calc_hist_2, hist_comp_2

import shutil
import cv2 as cv
import os

db = DB()

images_base_path = 'DB/storage/images'
videos_base_path = 'DB/storage/videos'


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
        'dominant_color': calc_dominant(image).tolist(),
        'histogram': calc_hist_2(image),
        'objects': extract_objects(image)
    }
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

    dominant_color = color_compare(image1_features.get('dominant_color'),
                                   image2_features.get('dominant_color'))

    histogram = hist_comp_2(image1_features.get('histogram'),
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
    return search_by_image_2(cv.imread(path))


def search_by_image_2(image):
    similarity = []
    query_image_feature = calculate_image_features(image)
    # images_features = db.get_all({'$not': {'name': None}})
    images_features = db.get_all_images({})
    for image_features in images_features:
        similar_image = compare_two_images(query_image_feature, image_features)
        similar_image['name'] = image_features['name']
        similar_image['_id'] = image_features['_id']
        similarity.append(similar_image)
    return similarity

def sort_by(similarity, feature):
    if feature == 'common_objects':
        similarity.sort(key=lambda image: len(image.get(feature)), reverse=True)
    else:
        similarity.sort(key=lambda image: image.get(feature), reverse=True)
    return similarity


def add_images_dataset(dir_path):
    entries = os.scandir(dir_path)
    for i, entry in enumerate(entries):
        if entry.is_dir():
            continue
        print(f'{i}, image: {entry.name}')
        features = calculate_image_features(cv.imread(entry.path))
        features['name'] = entry.name
        _, ext = os.path.splitext(entry.name)
        inserted = db.insert_image(features)
        shutil.copy(entry.path, os.path.join(images_base_path, f'{inserted.inserted_id}.{ext}'))


# def search_by_video()
def calculate_video_features(path):
    """
    video data_structure:
    {
        path: '',
        frames: [
            {
                number: 1,
                'avg_color': 13
                .
                .
            },
            {
                number: 2,
                'avg_color': 13
                .
                .
            }
        ]
    }
    :param path:
    :return:
    """
    key_frames = extract_key_frames(path)
    frames_features = []
    print(f'{len(key_frames)} key frames extracted')
    for i, key_frame in enumerate(key_frames):
        print(f'processing key frame: {i + 1} of {len(key_frames)}')
        frame_features = calculate_image_features(key_frame)
        frames_features.append(frame_features)
    video_features = {
        'frames': frames_features
    }

    return video_features


def add_videos_dataset(dir_path):
    entries = os.scandir(dir_path)
    for i, entry in enumerate(entries):
        if entry.is_dir():
            continue
        print(f'{i}, video: {entry.name}')
        features = calculate_video_features(entry.path)
        features['name'] = entry.name
        _, ext = os.path.splitext(entry.name)
        inserted = db.insert_key_frames(features)
        shutil.copy(entry.path, os.path.join(videos_base_path, f'{inserted.inserted_id}.{ext}'))


if __name__ == '__main__':
    path = "D:/Education/University/4thCSE/2nd/MultiMedia/Project/dataset/videos"
    # add_dataset(path)

    # similarity = search_by_image(
    #     "D:/Education/University/4thCSE/2nd/MultiMedia/Project/dataset/all dataset/862.jpg")
    #
    # similarity = sort_by(similarity, 'histogram')
    #
    # for i, image in enumerate(similarity):
    #     _, ext = os.path.splitext(image.get('name'))
    #     name = f'{image.get("_id")}.{ext}'
    #     path = os.path.join(base_path, name)
    #     img = cv.imread(path)
    #     cv.imshow(f'{i}, {image.get("histogram")}, {name}', img)
    #
    #     cv.waitKey(0)

    add_videos_dataset(path)
    # features = calculate_video_features(path)
    #
    # inserted = db.insert_key_frames(features)
    # print(inserted)