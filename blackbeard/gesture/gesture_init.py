import numpy as np
import tensorflow as tf
import cv2
import time


# load model
tflite_save_path = "gesture/model/model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_save_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def gesture_preprocess(landmark):
    """
    convert landmarks for trainable data
    66 features
    X (21): 0-20
    Y (21): 21-41
    Z (21): 42-62
    X,Y,Z range (3): 63-65
    params landmark: mediapipe landmark for 1 hand
    params label: str
    return: np.array (1,66)
    """
    lm_x = np.array([])
    lm_y = np.array([])
    lm_z = np.array([])
    for hlm in landmark.landmark:
        lm_x = np.append(lm_x, hlm.x)
        lm_y = np.append(lm_y, hlm.y)
        lm_z = np.append(lm_z, hlm.z)
    data_gest = [lm_x, lm_y, lm_z]
    x_rng, y_rng, z_rng = (
        lm_x.max() - lm_x.min(),
        lm_y.max() - lm_y.min(),
        lm_z.max() - lm_z.min(),
    )
    data_gest = np.ravel(
        [(k - k.min()) / (k.max() - k.min()) for i, k in enumerate(data_gest)]
    )
    data_gest = np.append(data_gest, [x_rng, y_rng, z_rng])
    return data_gest.astype("float32")


def gesture_inference(data, confidence=0.95):
    """
    inference
    param data: np.array
    param confidence: float - threshold for inference
    return: int class
    """
    interpreter.set_tensor(input_details[0]["index"], np.array([data]))
    interpreter.invoke()
    tflite_results = interpreter.get_tensor(output_details[0]["index"])
    inf_idx = np.argmax(np.squeeze(tflite_results))
    if np.squeeze(tflite_results)[inf_idx] < confidence:
        return -1
    return inf_idx


def gesture_pipeline(
    image, gest_time, hands, mp_hands, mp_drawing, mp_drawing_styles, debug=True
):
    """
    param image: stream image
    param gest_time: timer
    param debug: bool - debug view
    return int: gesture id
    return image: drawn image
    return time: updated timer
    """
    inf_class = {-1: "None", 0: "Hit", 1: "Stand", 2: "Split", 3: "Reset"}
    inf_class_idx = -1

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        if (time.time() - gest_time) > 0.5:
            #                 print("detected hand")
            for hand_landmarks in results.multi_hand_landmarks:
                # inference
                gest_data = gesture_preprocess(hand_landmarks)
                inf_class_idx = gesture_inference(gest_data)

                if debug:
                    # draw
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )
    else:
        gest_time = time.time()
    return inf_class[inf_class_idx], image, gest_time
