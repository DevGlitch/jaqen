# Adapted from repo botwizer by DevGltich
# https://github.com/DevGlitch/botwizer

# Resources used:
# https://github.com/AlexeyAB/darknet

import cv2
import time
import numpy as np


def img_object_detection_box(img_path, config_path, weights_path, labels_path):
    """Running YOLO on an image to detect objects
    :param img_path: path of image to analyse
    :param config_path: path of the .cfg file
    :param weights_path: path of the .weights file
    :param labels_path: path of the .names file
    :return: showing image with bounding box and label of object(s) detected
    :rtype: image (opencv window)
    """

    # Reads and load model stored in Darknet model files
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    # Object Labels
    obj_names = open(labels_path)
    obj_labels = obj_names.read().strip().split("\n")

    # initialize a list of colors to represent each possible class label
    np.random.seed(14)
    colors = np.random.randint(0, 255, size=(len(obj_labels), 3), dtype="uint8")

    # Reads image from provided path
    read_img = cv2.imread(img_path)

    # Get the number of rows and columns of the image
    img_row, img_col = read_img.shape[:2]

    # Creating a 4-dimensional blob from image
    # SwapRB to True increase classification accuracy
    blob = cv2.dnn.blobFromImage(read_img, (1 / 255), (416, 416), swapRB=True)

    # Putting blob as the input of the network
    net.setInput(blob)

    # Getting each layer name
    layer_name = net.getLayerNames()
    layer_name = [layer_name[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Timing network output
    time_start = time.perf_counter()
    print("Starting YOLO analysis...")
    outputs = net.forward(layer_name)
    time_stop = time.perf_counter() - time_start
    print(f"YOLO ran for: {time_stop:.2f}s")

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
    NMS = cv2.dnn.NMSBoxes(grid, probabilities, 0.5, 0.5)

    # If at least one object has been detected
    if len(NMS) > 0:

        for i in NMS.flatten():

            # Extract coordinates of each grid box
            (x, y) = (grid[i][0], grid[i][1])
            (w, h) = (grid[i][2], grid[i][3])

            # Create a bounding box around the object
            color = [int(c) for c in colors[labels[i]]]
            cv2.rectangle(read_img, (x, y), (x + w, y + h), color, 2)

            # Add label to the bounding box
            text = "{}: {:.4f}".format(obj_labels[labels[i]], probabilities[i])
            cv2.putText(
                read_img, text, (x + 10, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

    # If no object has been detected
    else:
        print("No object detected in the picture.")
        pass

    obj_names.close()

    # Open image to show the output with detected objects
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow("Image", read_img)
    cv2.waitKey(0)
