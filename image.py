import json
import cv2 as cv
import numpy as np

import averagefun


class Image:
    def __init__(self, path, dominant_color=None, average_color=None, objects=None, histogram=None):
        self.path = path
        self.dominant_color = dominant_color
        self.average_color = average_color
        self.objects = objects
        self.histogram = histogram

    def calc_average(self):
        return averagefun.calc_average(self.path)

    def calc_dominant(self):
        return averagefun.calc_average(self.path)