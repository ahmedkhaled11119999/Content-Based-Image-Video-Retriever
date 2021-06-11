from pymongo import MongoClient


class DB:
    def __init__(self):
        # client = MongoClient(
        #     "mongodb+srv://admin_belal:qwertyzxcvbnm@clusterformultimediapro.5bugi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        client = MongoClient(
            "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
        self.__db = client.get_database('CBIVR')
        self.__images_data = self.__db['Images_data']

    def insert_image(self, image_features):
        return self.__images_data.insert_one(image_features)

    def insert_key_frames(self, key_frames_features):
        return self.__images_data.insert_many(key_frames_features)

    def get_all(self, filters=None):
        if filters is None:
            filters = {}
        return self.__images_data.find(filters)


if __name__ == '__main__':

    avg_color = [20, 45, 54]
    dominant_color = [20, 45, 54]
    histogram = [
        [[20], [48]],  # B channel
        [[20], [48]],  # G channel
        [[20], [48]]  # R channel
    ]

    standalone_image_features = {
        'path': 'image_path',
        'shape': (100, 50),
        'avg_color': avg_color,
        'dominant_color': dominant_color,
        'histogram': histogram,
        'objects': ['brush', 'boy', 'girl']
    }

    video_frames_features = [
        {
            'parent_video_path': 'video_path',
            'shape': (100, 50),
            'avg_color': avg_color,
            'dominant_color': dominant_color,
            'histogram': histogram,
            'objects': ['brush', 'boy', 'girl']
        },
        {
            'parent_video_path': 'video_path',
            'shape': (100, 50),
            'avg_color': avg_color,
            'dominant_color': dominant_color,
            'histogram': histogram,
            'objects': ['brush', 'boy', 'girl']
        }
    ]

    db = DB()
    # result = db.insert_image(standalone_image_features)
    # result = db.insert_key_frames(video_frames_features)
    # print(f'db.insert_key_frames(video_frames_features): \n{result}')
    # result = db.get_all({'$not': {'path': None}})
    result = db.get_all({})
    for x in result:
        print(x.get('path'))
        if x.get('parent_video_path'):
            print(f'video: \n{x}')
        elif x.get('path'):
            print(f'image: \n{x}')
        else:
            print('!!!!!!!!!!')
