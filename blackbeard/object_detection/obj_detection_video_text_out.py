# Adapted from repo botwizer by DevGltich
# https://github.com/DevGlitch/botwizer

# Resources used:
# https://github.com/AlexeyAB/darknet

import cv2
import time
import numpy as np


def vid_object_detection_txt(vid_path, config_path, weights_path, labels_path):
    """Running YOLO on a video to detect objects
    :param vid_path: path of video to analyse
    :param config_path: path of the .cfg file
    :param weights_path: path of the .weights file
    :param labels_path: path of the .names file
    :return: object(s) detected
    :rtype: list
    """

    # Reads and load model stored in Darknet model files
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    # Object Labels
    obj_names = open(labels_path)
    obj_labels = obj_names.read().strip().split("\n")

    # initialize a list of colors to represent each possible class label
    # np.random.seed(14)
    colors = np.random.randint(0, 255, size=(len(obj_labels), 3), dtype="uint8")

    # Reads video from provided path
    # vid_file = os.path.join(vid_path)
    vid_cap = cv2.VideoCapture(vid_path)

    # For writing output video
    _, image = vid_cap.read()
    img_row, img_col = image.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (img_col, img_row))

    # # List objects where it stores the obj_names labels detected in the image
    # objects = []

    while vid_cap.isOpened():

        _, image = vid_cap.read()
        img_row, img_col = image.shape[:2]

        # Creating a 4-dimensional blob from image
        # SwapRB to True increase classification accuracy
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # Putting blob as the input of the network
        net.setInput(blob)

        # Getting each layer name
        layer_name = net.getLayerNames()
        layer_name = [layer_name[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # # Timing network output
        # time_start = time.perf_counter()
        # print("Starting YOLO analysis...")
        outputs = net.forward(layer_name)
        # time_stop = time.perf_counter() - time_start
        # print(f"YOLO ran for: {time_stop:.2f}s")

        grid, probabilities, labels = [], [], []

        # Find each single output
        # This for loop is based on information from darknet's code and opencv
        for output in outputs:

            # Find each single detection in output
            for detection in output:

                # Get probability score and label of the detection
                score = detection[5:]
                label = np.argmax(score)
                prob = score[label]

                # Selecting only detections that are superior to 50% probability
                # Anything below 50% is ignored as probability is too low
                # You can increase this to higher or lower probability if needed
                if prob > 0.5:

                    # Working on each bounding box of the grid created by YOLO
                    grid_box = detection[:4] * np.array(
                        [img_col, img_row, img_col, img_row]
                    )
                    (X, Y, width, height) = grid_box.astype("int")
                    x = X - (width / 2)
                    y = Y - (height / 2)

                    # Appending to the lists
                    probabilities.append(float(prob))
                    labels.append(label)
                    grid.append([int(x), int(y), int(width), int(height)])

        # Performs Non Maximum Suppression given boxes and corresponding scores.
        # This filters the boxes in the image grid.
        # It keeps only the ones with the highest probability
        NMS = cv2.dnn.NMSBoxes(grid, probabilities, 0.6, 0.6)

        # If at least one object has been detected
        if len(NMS) > 0:

            # List objects where it stores the obj_names labels detected in the image
            objects = []

            for i in NMS.flatten():

                objects += [
                    f"{obj_labels[labels[i]]}"
                ]

                # print("The objects are:\n", objects)

                yield objects

    # Close names file
    obj_names.close()

    # Close video file
    vid_cap.release()

    # return objects
