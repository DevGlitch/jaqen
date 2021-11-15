from object_detection.object_detection_func import *
from remote_gpio.gpio_func import *
from mqtt.mqtt_func import *
import keyboard


def main():

    ####################################################################
    # ################## START - USER DEFINED FILES ################## #

    # Custom YOLOV4-Tiny Trained on Playing Cards Dataset
    config_path = "../blackbeard/object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "../blackbeard/object_detection/yolo/weights/blackbeard_yolov4-tiny-obj_170000.weights"
    labels_path = "../blackbeard/object_detection/yolo/obj_names/blackbeard.names"

    # Raspberry Pi IP Address
    pi_ip = "ADD PI ADDRESS HERE"

    # RTSP Stream URL
    rtsp_url = "rtsp://" + pi_ip + ":8554/unicast"

    # MQTT channel
    pi_channel = "blackbeard"

    # ################### END - USER DEFINED FILES ################### #
    ####################################################################

    ####################################################################
    # ###################### START - BLACKBEARD ###################### #

    # INFO START
    print("[INFO] Starting Blackbeard...")  # Displayed on PC Command Line
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Starting Blackbeard...")  # Displayed on Raspberry Pi Command Line

    # Load Object Detection
    print("[INFO] Loading Object Detection...")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Loading Object Detection...")
    net = load_yolo(config_path, weights_path)
    obj_names, obj_labels = load_labels(labels_path)
    sleep(1)
    print("[INFO] Object Detection Loaded.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Object Detection Loaded.")

    # Capture video stream from RTSP URL
    print("[INFO] Stream Capture Starting...")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Stream Capture Starting...")
    stream_video = cv2.VideoCapture(rtsp_url)
    sleep(1)
    print("[INFO] Stream Capture Started.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Stream Capture Started.")

    # INFO READY
    print("[INFO] Blackbeard is running...")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Blackbeard is running...")

    while stream_video.isOpened():

        # Reading image from stream
        _, image = stream_video.read()

        ########################################################
        # ######### START OBJECT DETECTION PIPELINE #########  #

        # Get detected objects from stream
        for detected_objects in object_detection(net, obj_labels, image, cuda=1):

            # PC
            print("[INFO] Card Detected:", detected_objects)
            send_msg_by_mqtt(pi_ip, pi_channel, message=("[INFO] Card Detected:", detected_objects))

            print("---------------------------------------------")
            send_msg_by_mqtt(pi_ip, pi_channel, "---------------------------------------------")

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
            send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Closing Blackbeard...")
            break

    sleep(1)

    # Tearing down object detection
    teardown_obj_detection(obj_names)

    # Releasing stream
    stream_video.release()
    sleep(1)
    print("[INFO] Video stream released.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Closing Blackbeard...")

    # ####################### END - BLACKBEARD ####################### #
    ####################################################################

    print("[INFO] Blackbeard closed.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Blackbeard closed.")

    print("---------------------------------------------")
    send_msg_by_mqtt(pi_ip, pi_channel, "---------------------------------------------")

    print("[INFO] Thank you for using Blackbeard!")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Thank you for using Blackbeard!")

    print("[INFO] Developed by codejacktsu & DevGlitch.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Developed by codejacktsu & DevGlitch.")
