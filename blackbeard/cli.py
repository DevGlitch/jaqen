from object_detection.object_detection_func import *
from remote_gpio.gpio_func import *
from mqtt.mqtt_func import *
from gpiozero import Button
import keyboard
import mediapipe as mp
from gesture.gesture_init import gesture_pipeline
from blackjack.blackjack import Game
from blackjack.rules import cards
import time


def main():

    ####################################################################
    # ################## START - USER DEFINED FILES ################## #

    # run v4l2rtspserver on raspi

    # Custom YOLOV4-Tiny Trained on Playing Cards Dataset
    config_path = "../blackbeard/object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights_path = "../blackbeard/object_detection/yolo/weights/blackbeard_yolov4-tiny-obj_170000.weights"
    labels_path = "../blackbeard/object_detection/yolo/obj_names/blackbeard.names"

    # Raspberry Pi IP Address
    pi_ip = "YOUR_PI_IP_ADDRESS"
    # pi_ip = "192.168.1.98"

    # RTSP Stream URL
    rtsp_url = "rtsp://" + pi_ip + ":8554/unicast"

    # MQTT channel
    pi_channel = "blackbeard"

    # Connecting to GPIO remotely
    factory = connect_remote_gpio(pi_ip)
    # GPIO22 - Turn the backlight on and off
    # GPIO23 & GPIO24 - Two temporary buttons next to the display
    stop_button = Button(24, pin_factory=factory)

    # Debug view
    debug = True

    # ################### END - USER DEFINED FILES ################### #
    ####################################################################

    # Waiting for Button GPIO23 to be press to start Blackbeard
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Press Start.")
    print("[INFO] Press Start.")
    button_wait_for_press(23, factory)  # Top button

    ####################################################################
    # ###################### START - BLACKBEARD ###################### #

    # INFO START
    print("[INFO] Starting Blackbeard...")  # Displayed on PC Command Line
    send_msg_by_mqtt(
        pi_ip, pi_channel, "[INFO] Starting Blackbeard..."
    )  # Displayed on Raspberry Pi Command Line

    # Load Object Detection
    print("[INFO] Loading Object Detection...")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Loading Object Detection...")
    net = load_yolo(config_path, weights_path)
    obj_names, obj_labels = load_labels(labels_path)
    final_cards = set()
    sleep(1)
    print("[INFO] Object Detection Loaded.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Object Detection Loaded.")

    # Load Gesture Detection
    print("[INFO] Loading Gesture Detection...")
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    sleep(1)
    print("[INFO] Gesture Detection Loaded.")

    # Load Blackjack logic
    print("[INFO] Loading Gesture Detection...")
    ###
    game = Game(cards)
    ###
    sleep(1)
    print("[INFO] Gesture Detection Loaded.")

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

    with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:

        # timing
        gest_time = time.time()  # gesture timer
        non_reset_time = time.time()  # reset timer
        reset_time = 0
        ob_time = time.time()  # object detection timer

        while stream_video.isOpened():

            # Reading image from stream
            _, image = stream_video.read()

            ########################################################
            # ######### START OBJECT DETECTION PIPELINE #########  #

            # Get detected objects from stream
            if (time.time() - ob_time) > 1.5:
                for detected_objects in object_detection(net, obj_labels, image, cuda=1):

                    # msg = "[INFO] Card Detected:" + str(set(detected_objects))
                    # print(msg)
                    # send_msg_by_mqtt(pi_ip, pi_channel, msg)

                    # print("---------------------------------------------")
                    # send_msg_by_mqtt(
                    #     pi_ip, pi_channel, "----------------------------------------"
                    # )
                    curr_cards = set(detected_objects)
                ob_time = time.time()

            # ########## END OBJECT DETECTION PIPELINE ##########  #
            ########################################################

            ########################################################
            # ############## START GESTURE PIPELINE #############  #

            gest_class, image, gest_time = gesture_pipeline(
                image, gest_time, hands, mp_hands, mp_drawing, mp_drawing_styles, debug
            )

            # ############### END GESTURE PIPELINE ##############  #
            ########################################################

            ########################################################
            # ######## START BLACKJACK STRATEGY PIPELINE ########  #

            # hot fix - reset
            if gest_class != "Reset":
                non_reset_time = time.time()
            elif gest_class == "Reset":
                reset_time = time.time() - non_reset_time
                if reset_time > 3:
                    gest_class = "Reset"
                else:
                    gest_class = "Reset-Pending"

            for card in curr_cards:
                game.game_update(card=card, gest=gest_class)

            # ######### END BLACKJACK STRATEGY PIPELINE #########  #
            ########################################################

            # ##################### MQTT MSG ####################  #

            send_msg_by_mqtt(
                pi_ip, pi_channel, f"Count: {game.count}"
            )
            send_msg_by_mqtt(
                pi_ip, pi_channel, f"Next Bet: ${game.bet_size()}"
            )
            send_msg_by_mqtt(
                pi_ip, pi_channel, f"Detected Action: {game.action} | Opt Action: {game.opt}"
            )
            send_msg_by_mqtt(
                pi_ip, pi_channel, f"Player Cards: {game.hand} | Total: {game.ptotal}"
            )
            send_msg_by_mqtt(
                pi_ip, pi_channel, f"Dealer Cards: {game.dealer} | Total: {game.dtotal}"
            )

            ########################################################

            # debug view
            if debug:
                cv2.putText(
                    image,
                    f"Game Phase: {game.phase_label()}",
                    (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
                cv2.putText(
                    image,
                    f"Count: {game.count} | Next Bet: ${game.bet_size()}",
                    (0, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
                cv2.putText(
                    image,
                    f"Gesture: {gest_class} | Action: {game.action} | Opt Action: {game.opt}",
                    (0, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
                cv2.putText(
                    image,
                    f"Player Cards: {game.hand} | Total: {game.ptotal}",
                    (0, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
                cv2.putText(
                    image,
                    f"Dealer Cards: {game.dealer} | Total: {game.dtotal}",
                    (0, 125),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )
                # cv2.putText(
                #     image,
                #     f"Debug Etc: {round(non_reset_time,3)}| Left: {reset_time}",
                #     (0, 150),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     0.9,
                #     (36, 255, 12),
                #     2,
                # )
                cv2.imshow("Debug View", image)
                cv2.waitKey(5)

            # Commands to stop Blackbeard
            if keyboard.is_pressed("q"):
                print("[INFO] Closing Blackbeard...")
                send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Closing Blackbeard...")
                break

            elif stop_button.is_held:
                print("[INFO] Closing Blackbeard...")
                send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Closing Blackbeard...")
                break

    sleep(1)
    # Tear down debug view
    if debug:
        cv2.destroyAllWindows()

    # Tearing down object detection
    teardown_obj_detection(obj_names)

    # Releasing stream
    stream_video.release()
    sleep(1)
    print("[INFO] Video stream released.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Video stream released.")

    # ####################### END - BLACKBEARD ####################### #
    ####################################################################

    print("[INFO] Blackbeard closed.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Blackbeard closed.")

    print("---------------------------------------------")
    send_msg_by_mqtt(pi_ip, pi_channel, "----------------------------------------")

    print("[INFO] Thank you for using Blackbeard!")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] Thank you for using Blackbeard!")

    print("[INFO] Developed by codejacktsu & DevGlitch.")
    send_msg_by_mqtt(pi_ip, pi_channel, "[INFO] by codejacktsu & DevGlitch")
