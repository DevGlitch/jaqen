from object_detection.object_detection_func import *
import keyboard
import mediapipe as mp
import tensorflow as tf
from gesture.gesture_init import gesture_preprocess, gesture_inference, load_model


def main():

    ####################################################################
    # ################## START - USER DEFINED FILES ################## #

    # Custom YOLOV4-Tiny Trained on Playing Cards Dataset
    config_path = "../blackbeard/object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "../blackbeard/object_detection/yolo/weights/blackbeard_yolov4-tiny-obj_170000.weights"
    labels_path = "../blackbeard/object_detection/yolo/obj_names/blackbeard.names"

    # RTSP Stream URL
    rtsp_url = "rtsp://192.168.1.98:8554/unicast"

    # ################### END - USER DEFINED FILES ################### #
    ####################################################################

    ####################################################################
    # ###################### START - BLACKBEARD ###################### #

    # INFO START
    print("[INFO] Starting Blackbeard...")
    debug = True  # debug view

    # Load Object Detection
    print("[INFO] Loading Object Detection...")
    net = load_yolo(config_path, weights_path)
    obj_names, obj_labels = load_labels(labels_path)
    sleep(1)
    print("[INFO] Object Detection Loaded.")

    # Load Gesture Detection
    print("[INFO] Loading Gesture Detection...")
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    interpreter, input_details,output_details = load_model()
    inf_class = {0: 'Hit', 1: 'Stand', 2: 'Split', 3: 'Reset', 4: 'None'}
    inf_class_idx = 4
    sleep(1)
    print("[INFO] Gesture Detection Loaded.")

    # Capture video stream from RTSP URL
    print("[INFO] Stream Capture Starting...")
    stream_video = cv2.VideoCapture(rtsp_url)
    sleep(1)
    print("[INFO] Stream Capture Started.")

    # INFO READY
    print("[INFO] Blackbeard is running...")

    with mp_hands.Hands(
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while stream_video.isOpened():

            # Reading image from stream
            _, image = stream_video.read()

            ########################################################
            # ######### START OBJECT DETECTION PIPELINE #########  #

            # Get detected objects from stream
            for detected_objects in object_detection(net, obj_labels, image, cuda=1):

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

            # debug view
            if debug:
                cv2.putText(image, f"{inf_class[inf_class_idx]}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                cv2.imshow('Debug View', image)

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
