# Gesture Detection:

- use ipynb for data exploration, data collection, and model training
- import gesture_init.py for production

Key Functions:
- gesture_preprocess(landmark)
- gesture_inference(processed_data)

Loop format:
If detects hand for over 0.5 sec, then initiate gesture recognition

detect_time = time.time()

if results.multi_hand_landmarks:
    if (time.time() - detect_time) > 0.5:
        print("detected hand")
        for hand_landmarks in results.multi_hand_landmarks:
            # inference
else:
    detect_time = time.time()