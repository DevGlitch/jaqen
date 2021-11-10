from object_detection_func import *
import keyboard


def main():

    ####################################################################
    # ################## START - USER DEFINED FILES ################## #

    # Custom YOLOV4-Tiny Trained on Playing Cards Dataset
    config_path = "../object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "yolo/weights/blackbeard_yolov4-tiny-obj_170000.weights"
    labels_path = "../object_detection/yolo/obj_names/blackbeard.names"

    # RTSP Stream URL
    rtsp_url = "rtsp://RASPBERRY_PI_CAMERA_IP:8554/unicast"

    # ################### END - USER DEFINED FILES ################### #
    ####################################################################

    ####################################################################
    # ###################### START - BLACKBEARD ###################### #

    # INFO START
    print("[INFO] Starting Blackbeard...")

    # Load Object Detection
    print("[INFO] Loading Object Detection...")
    net = load_yolo(config_path, weights_path)
    obj_names, obj_labels = load_labels(labels_path)
    sleep(1)
    print("[INFO] Object Detection Loaded.")

    # Capture video stream from RTSP URL
    print("[INFO] Stream Capture Starting...")
    stream_video = cv2.VideoCapture(rtsp_url)
    sleep(1)
    print("[INFO] Stream Capture Started.")

    # INFO READY
    print("[INFO] Blackbeard is running...")

    while stream_video.isOpened():

        # Reading image from stream
        _, image = stream_video.read()

        ########################################################
        # ######### START OBJECT DETECTION PIPELINE #########  #

        # Get detected objects from stream
        for detected_objects in object_detection(net, obj_labels, image):

            print("[INFO] Card Detected:", detected_objects)  # for debug
            print("---------------------------------------------")  # for debug

        # ########## END OBJECT DETECTION PIPELINE ##########  #
        ########################################################

        ########################################################
        # ############## START GESTURE PIPELINE #############  #

        # Insert code here

        # ############### END GESTURE PIPELINE ##############  #
        ########################################################

        ########################################################
        # ######## START BLACKJACK STRATEGY PIPELINE ########  #

        # Insert code here

        # ######### END BLACKJACK STRATEGY PIPELINE #########  #
        ########################################################

        # Command to stop Blackbeard
        if keyboard.is_pressed("q"):
            print("[INFO] Closing Blackbeard...")
            break

    sleep(1)

    # Tearing down object detection
    teardown_obj_detection(obj_names)

    # Releasing stream
    stream_video.release()
    sleep(1)
    print("[INFO] Video stream released.")

    # ####################### END - BLACKBEARD ####################### #
    ####################################################################

    print("[INFO] Blackbeard closed.")
    print("---------------------------------------------")
    print("[INFO] Thank you for using Blackbeard!")
    print("[INFO] Developed by codejacktsu & DevGlitch.")
