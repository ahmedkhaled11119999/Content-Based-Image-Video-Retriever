
import cv2 as cv
import os
import numpy as np

def extract_key_frames(video_path):
    """
    open the video and extract the key frames as opencv images
    :param video_path:
    :return: return list of opencv images
    """
    key_frames = []
    frame_thresh = 2700000  # adjustable
    capture = cv.VideoCapture(video_path)
    frames_per_second = int(capture.get(cv.CAP_PROP_FPS))
    if (frames_per_second == 0):
        print("Not available")

    # Read the first frame.
    success, prev_frame = capture.read()

    while success:
        success, curr_frame = capture.read()
        if success:

            #using absolute_difference

            diff = cv.absdiff(curr_frame, prev_frame)
            non_zero_count = np.count_nonzero(diff)
            if non_zero_count > frame_thresh:
                key_frames.append(curr_frame)


            prev_frame = curr_frame

    return key_frames

#################"Test extract_key_frames"##########################

def Test_extract_key_frames(video_path):
    key_frames = extract_key_frames(video_path)
    print(len(key_frames))
    #print(key_frames)

    for i in range(len(key_frames)):
        cv.imshow('key frame ' + str(i), key_frames[i])
        cv.waitKey(500)
video_path='Video.mp4' #path of video uploaded from DB\storage
Test_extract_key_frames(video_path)
