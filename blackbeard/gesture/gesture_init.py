import numpy as np
import mediapipe as mp
import tensorflow as tf


# load mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# load model
tflite_save_path = 'model/model.tflite'
interpreter = tf.lite.Interpreter(model_path=tflite_save_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# gesture variables
inf_class = {0: 'Hit', 1: 'Stand', 2: 'Split', 3: 'Reset', 4: 'None'}
inf_class_idx = 4


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
    x_rng, y_rng, z_rng = lm_x.max() - lm_x.min(), lm_y.max() - lm_y.min(), lm_z.max() - lm_z.min()
    data_gest = np.ravel([(k - k.min()) / (k.max() - k.min()) for i, k in enumerate(data_gest)])
    data_gest = np.append(data_gest, [x_rng, y_rng, z_rng])
    return data_gest.astype('float32')


def gesture_inference(data):
    """
    inference

    param data: np.array
    return: int class
    """
    interpreter.set_tensor(input_details[0]['index'], np.array([data]))
    interpreter.invoke()
    tflite_results = interpreter.get_tensor(output_details[0]['index'])
    inf_idx = np.argmax(np.squeeze(tflite_results))
    if np.squeeze(tflite_results)[inf_class_idx] < 0.95:
        return 4
    return inf_idx
