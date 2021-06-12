from db import DB
from average_fun import calc_average, calc_dominant, color_compare
from test_key_extraction import extract_key_frames
from object_detection import extract_objects
from compare_histogram import calc_hist_hsv, hist_comp_hsv

import shutil
import cv2 as cv
import os

db = DB()

images_base_path = 'DB/storage/images'
videos_base_path = 'DB/storage/videos'


def calculate_image_features(image, ignore_dominant=False):
    """
    calculate the image features using the helper functions
    :param ignore_dominant: dominant color takes long time to be calculated and it is not required for video, set this
    to true if you want to ignore it when analyzing videos
    :param image:
    :return:
    """
    image_features = {
        'shape': (image.shape[0], image.shape[1]),
        'avg_color': calc_average(image).tolist(),
        'histogram': calc_hist_hsv(image),
        'objects': extract_objects(image)
    }
    if ignore_dominant:
        image_features['dominant_color'] = image_features['avg_color']
    else:
        image_features['dominant_color'] = calc_dominant(image).tolist()
    return image_features


def get_image_features(path):
    """
    open the image then calculate its features
    :param path:
    :return:
    """
    image = cv.imread(path)
    features = calculate_image_features(image)
    return features


def get_video_features(path):
    """
    extract the key frames from the video then calculate each frame features
    :param path:
    :return:
    """
    frames = extract_key_frames(path)
    frames_features = []
    for frame in frames:
        features = calculate_image_features(frame, ignore_dominant=True)
        features['parent_video_path'] = path
        frames_features.append(features)
    return frames_features


def compare_two_images(image1_features, image2_features):
    """
    compares two images features and return dict with similarity of each feature
    :param image1_features:
    :param image2_features:
    :return:
    """
    average_color = color_compare(image1_features.get('avg_color'),
                                  image2_features.get('avg_color'))

    dominant_color = color_compare(image1_features.get('dominant_color'),
                                   image2_features.get('dominant_color'))

    histogram = hist_comp_hsv(image1_features.get('histogram'),
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
    open the image then search search_by_image_binary
    :param path:
    :return:
    """
    return search_by_image_binary(cv.imread(path))


def search_by_image_binary(image):
    """
    Take an image and calculate the image features, and compare with the precalculated images features in the db and return
    list of each image similarity
    :param image:
    :return:
    """
    similarity = []
    query_image_feature = calculate_image_features(image)
    images_features = db.get_all_images({})
    for image_features in images_features:
        similar_image = compare_two_images(query_image_feature, image_features)
        similar_image['name'] = image_features['name']
        similar_image['_id'] = image_features['_id']
        _, ext = os.path.splitext(image_features.get('name'))
        path = os.path.join(images_base_path, f'{image_features.get("_id")}.{ext}')
        similar_image['path'] = path
        similarity.append(similar_image)
    return similarity


def sort_by(similarity, feature):
    """
    sort by the feature required
    :param similarity:
    :param feature:
    :return:
    """
    if feature == 'common_objects':
        similarity.sort(key=lambda image: len(image.get(feature)), reverse=True)
    else:
        similarity.sort(key=lambda image: image.get(feature), reverse=True)
    return similarity


def add_images_dataset(dir_path):
    """
    this can add entire directory to the images database
    :param dir_path:
    :return:
    """
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
        frame_features = calculate_image_features(key_frame, ignore_dominant=True)
        frames_features.append(frame_features)
    video_features = {
        'frames': frames_features
    }
    return video_features


def add_videos_dataset(dir_path):
    """
    this can add entire directory to the videos database
    :param dir_path:
    :return:
    """
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


def compare_two_videos(video1_features, video2_features, feature='histogram'):
    """
    compare video1 key frames with video 2 key frames and get the average similarity, this is based on naive compare
    algorithm in which we compare first video key frames with the corresponding second video key frmaes
    :param feature:
    :param video1_features:
    :param video2_features:
    :return:
    """
    if feature == 'common_objects':
        similarity = []
    else:
        similarity = 0
    for video1_frame, video2_frame in zip(video1_features['frames'], video2_features['frames']):
        similarity += compare_two_images(video1_frame, video2_frame)[feature]
    if feature == 'common_objects':
        return list(set(similarity))
    else:
        return similarity / len(video1_features['frames'])


def search_by_video(path, feature='histogram'):
    """
    1. calculate video features
    2. get saved videos features from the db
    3. search video by the required feature
    :param path:
    :param feature:
    :return:
    """
    query_video_features = calculate_video_features(path)
    db_videos_features = get_saved_videos_features()
    return search_by_video_features(query_video_features, db_videos_features, feature)


def get_saved_videos_features():
    """
    get saved videos features from the db
    :return:
    """
    return db.get_all_videos()


def search_by_video_features(query_video_features, db_videos_features, feature='histogram'):
    """
    take a video query features to be search in the db videos
    :param query_video_features:
    :param db_videos_features:
    :param feature:
    :return:
    """
    similar_videos = []
    for video_features in db_videos_features:
        similarity = compare_two_videos(query_video_features, video_features, feature)
        similar_video = {'similarity': similarity, 'name': video_features['name'], '_id': video_features['_id']}

        _, ext = os.path.splitext(video_features['name'])
        path = os.path.join(videos_base_path, f'{video_features.get("_id")}.{ext}')
        similar_video['path'] = path
        similar_videos.append(similar_video)
    if feature == 'common_objects':
        similar_videos.sort(key=lambda video: len(video.get('similarity')), reverse=True)
    else:
        similar_videos.sort(key=lambda video: video.get('similarity'), reverse=True)

    return similar_videos


if __name__ == '__main__':

    # images_dataset_path = "C:/Users/Legion/Desktop/images"
    # add_images_dataset(images_dataset_path)

    query_image_path = "C:/Users/Legion/PycharmProjects/Content-Based-Image-Video-Retriever/DB/storage/images/60c40f1df6d82ab4651128b5..jpg"

    similarity = search_by_image(
        query_image_path)

    similarity = sort_by(similarity, 'histogram')

    for i, image in enumerate(similarity):
        _, ext = os.path.splitext(image.get('name'))
        name = f'{image.get("_id")}.{ext}'
        # path = os.path.join(images_base_path, name)
        path = image.get("path")
        img = cv.imread(path)
        cv.imshow(f'{i}, {image.get("histogram")}, {name}', img)
        cv.waitKey(0)

    # videos_dataset_path = "C:/Users/Legion/Desktop/vids"
    # add_videos_dataset(videos_dataset_path)

    # query_video_path = "D:/Education/University/4thCSE/2nd/MultiMedia/Project/dataset/videos/Blue Whales 101 _ Nat Geo Wild.mp4"
    #
    # # query_video_features = calculate_video_features(query_video_path)
    # db_videos_features = get_saved_videos_features()
    # query_video_features = db_videos_features[0]
    #
    # videos = search_by_video2(query_video_features, db_videos_features)
    #
    # print(videos)
