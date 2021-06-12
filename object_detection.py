import cv2

thres = 0.5  # Threshold to detect object


def extract_objects(image):
    """
    take an opencv image and extract the objects in it
    :param image: opencv image (image = cv.imread())
    :return: list of strings with the objects names
    """
    extracted_objectsIds = []
    extracted_objects = []
    classNames = []
    classFile = 'object_detection/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'object_detection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'object_detection/frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    classIds, confs, bbox = net.detect(image, confThreshold=thres)

    # for id, conf in zip(classIds, confs):
    #     print(f'name: {id}, conf: {conf}')

    try:
        extracted_objectsIds = classIds.flatten()
    except Exception as e:
        print(f'no objects can be detected')
    for i in extracted_objectsIds:
        extracted_objects.append(classNames[i - 1])
    # print(extracted_objects)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(image, box, color=(0, 255, 0), thickness=2)
            cv2.putText(image, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return extracted_objects


if __name__ == '__main__':
    img = cv2.imread("object_detection/20210115062121_New_EVs_coming_in_2021.jpg")
    extracted = extract_objects(img)

    print(extracted)
