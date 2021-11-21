from unittest import TestCase
from blackbeard.object_detection.obj_detection_img_text_out import *

# from blackbeard.object_detection.obj_detection_img_box_out import *


# YOLOV3 & COCO for testing functions
config_path = "object_detection/yolo/cfg/yolov3.cfg"
weights_path = "object_detection/yolo/weights/yolov3.weights"  # wget https://pjreddie.com/media/files/yolov3.weights
labels_path = "object_detection/yolo/obj_names/coco.names"  # COCO Labels (https://cocodataset.org/)


class ObjectDetectionTesting(TestCase):
    def test_one_object_text(self):
        """Ensuring that YOLO detects the correct object"""
        img = "test_files/test_one_obj.jpg"
        detection = img_object_detection_txt(
            img, config_path, weights_path, labels_path
        )
        self.assertEqual(detection, ["dog"])

    def test_no_object_text(self):
        """Ensuring that YOLO doesn't detect any object"""
        img = "test_files/test_no_obj.jpg"
        detection = img_object_detection_txt(
            img, config_path, weights_path, labels_path
        )
        self.assertEqual(detection, None)

    def test_multi_objects_text(self):
        """Ensuring that YOLO detects the correct number of object"""
        img = "test_files/test_multi_obj.jpg"
        detection = img_object_detection_txt(
            img, config_path, weights_path, labels_path
        )
        self.assertEqual(detection, ["dog", "car", "car", "motorbike"])
