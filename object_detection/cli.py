from obj_detection_img_text_out import *
from obj_detection_img_box_out import *
# from obj_detection_video_box_out import *
from obj_detection_video_text_out import *


def main():

    # Custom YOLOV4-Tiny Trained on Cards Dataset
    config_path = "../object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "../object_detection/yolo/weights/yolov4-tiny-obj_170000.weights"
    labels_path = "../object_detection/yolo/obj_names/blackbeard.names"

    # YOLOV3 & COCO for testing function
    # config_path = "../object_detection/yolo/cfg/yolov3.cfg"
    # weights_path = "../object_detection/yolo/weights/yolov3.weights"  # wget https://pjreddie.com/media/files/yolov3.weights
    # labels_path = "../object_detection/yolo/obj_names/coco.names"  # COCO Labels (https://cocodataset.org/)

    # img = "z_valet_obj.jpg"
    #
    # # Get text out with detected objects as a list
    # img_object_detection_txt(img, config_path, weights_path, labels_path)
    #
    # # Get image out with detected objects in bounding boxes
    # img_object_detection_box(img, config_path, weights_path, labels_path)

    # vid = "busy_intersection.mp4"
    vid = "live_blackjack_short_2.mp4"

    # Get video out with detected objects in bounding boxes
    # vid_object_detection_box(vid, config_path, weights_path, labels_path)

    # Get text out with detected objects as a list
    for detected_objects in vid_object_detection_txt(vid, config_path, weights_path, labels_path):

        print(detected_objects)  # for debug
        print("----------------------------------------")  # for debug

    # Close all open windows
    # cv2.destroyAllWindows()
