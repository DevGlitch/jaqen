from obj_detection_img_text_out import *
from obj_detection_img_box_out import *
from obj_detection_video_box_out import *
import cv2


def main():

    # Custom YOLOV4-Tiny Trained on Cards Dataset
    config_path = "../object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "../object_detection/yolo/weights/yolov4-tiny-obj_170000.weights"
    labels_path = "../object_detection/yolo/obj_names/blackbeard.names"

    img = "z_valet_obj.jpg"

    # Get text out with detected objects as a list
    img_object_detection_txt(img, config_path, weights_path, labels_path)

    # Get image out with detected objects in bounding boxes
    # img_object_detection_box(img, config_path, weights_path, labels_path)

    # vid = "busy_intersection.mp4"
    # vid = "live_blackjack_short_2.mp4"

    # Get video out with detected objects in bounding boxes
    # vid_object_detection_box(vid, config_path, weights_path, labels_path)

    # Close all open windows
    # cv2.destroyAllWindows()
