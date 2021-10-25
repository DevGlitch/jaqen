from obj_detection_img_text_out import *
from obj_detection_img_box_out import *
from obj_detection_video_box_out import *
import cv2


def main():

    # img = "z_valet_obj.jpg"
    #
    # # Get text out with detected objects as a list
    # img_object_detection_txt(img)
    #
    # # Get image out with detected objects in bounding boxes
    # img_object_detection_box(img)

    # vid = "busy_intersection.mp4"
    vid = "live_blackjack_short_2.mp4"

    # Get video out with detected objects in bounding boxes
    vid_object_detection_box(vid)

    # Close all open windows
    # cv2.destroyAllWindows()
