from unittest import TestCase

from object_detection.obj_detection_img_text_out import *
# from object_detection.obj_detection_img_box_out import *


class ObjectDetectionTesting(TestCase):

    def test_one_object_text(self):
        """ Ensuring that YOLO detects the correct object"""
        img = "test_files/test_one_obj.jpg"
        detection = img_object_detection_txt(img)
        self.assertEqual(detection, ["dog"])

    def test_no_object_text(self):
        """ Ensuring that YOLO doesn't detect any object"""
        img = "test_files/test_no_obj.jpg"
        detection = img_object_detection_txt(img)
        self.assertEqual(detection, None)

    def test_multi_objects_text(self):
        """ Ensuring that YOLO detects the correct number of object """
        img = "test_files/test_multi_obj.jpg"
        detection = img_object_detection_txt(img)
        self.assertEqual(detection, ["dog", "car", "car", "motorbike"])

