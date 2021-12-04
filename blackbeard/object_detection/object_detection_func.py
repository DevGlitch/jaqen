"""
Functions to create and run an object detection pipeline

Resources used:
https://github.com/DevGlitch/botwizer
https://github.com/AlexeyAB/darknet

Developed by DevGlitch
"""

import cv2
import numpy as np
from time import sleep


def load_yolo(config_path, weights_path):
    """Load model and config files
    :param config_path: path of the .cfg file
    :param weights_path: path of the .weights file
    :return: loaded model files using darknet
    """
    # Reads and load model stored in Darknet model files
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    sleep(1)
    print("[INFO] Model loaded.")

    return net


def load_labels(labels_path):
    """Load labels used in the model
    :param labels_path: path of the .names file
    :return: object names and labels
    """
    # Object Labels
    obj_names = open(labels_path)
    obj_labels = obj_names.read().strip().split("\n")
    sleep(1)
    print("[INFO] Object labels loaded.")

    return obj_names, obj_labels


def labels_colors(obj_labels):
    """Create label colors
    :param obj_labels: loaded object labels of the model
    :return: list
    """
    # Use a random seed if you'd like to always keep the same colors
    # np.random.seed(14)

    # initialize a list of colors to represent each possible class label
    colors = np.random.randint(0, 255, size=(len(obj_labels), 3), dtype="uint8")

    return colors


def object_detection(
    net, obj_labels, image, debug=False, colors=None, out=None, cuda=False
):
    """Running YOLO on a video or stream to detect objects
    :param net: loaded darknet model and config file
    :param obj_labels: loaded object labels of the model
    :param image: image from OpenCV video capture
    :param debug: debug view parameter
    :param colors: list of colors from labels_colors function
    :param out: video output file details from write_out_video_init function
    :param cuda: OpenCV with or without CUDA support
    :return: detected objects
    :rtype: list or OpenCV window
    """

    # Getting image shape
    img_row, img_col = image.shape[:2]

    # Creating a 4-dimensional blob from image
    # SwapRB to True increase classification accuracy
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Putting blob as the input of the network
    net.setInput(blob)

    # Getting each layer name
    layer_name = net.getLayerNames()
    # OpenCV with or without CUDA support(2D-array vs 1D-array being returned)
    if cuda:
        layer_name = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
    else:
        layer_name = [layer_name[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(layer_name)

    # Initializing lists
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

            # Selecting only detections that are superior to 70% probability
            # Anything below 70% is ignored as probability is too low
            # You can increase this to higher or lower probability if needed
            if prob > 0.85:

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

        if debug is False:

            # List objects where it stores the obj_names labels detected in the image
            objects = []

            # Add each object detected to the list objects
            for i in NMS.flatten():

                # Appending to the object list
                objects += [f"{obj_labels[labels[i]]}"]

            # Yielding list of the detected objects
            yield objects

        if debug is True:

            # List objects where it stores the obj_names labels detected in the image
            objects = []

            for i in NMS.flatten():

                # Extract coordinates of each grid box
                (x, y) = (grid[i][0], grid[i][1])
                (w, h) = (grid[i][2], grid[i][3])

                # Create a bounding box around the object
                color = [int(c) for c in colors[labels[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=2)

                # Add label to the bounding box
                text = "{}: {:.4f}".format(
                    obj_labels[labels[i]], probabilities[i]
                )  # w/ probabilities
                # text = "{}".format(obj_labels[labels[i]])  # w/o probabilities
                cv2.putText(
                    image,
                    text,
                    (x, y - 5),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=color,
                    thickness=2,
                )

                # Appending to the object list
                objects += [f"{obj_labels[labels[i]]}"]

            if out is not None:
                # Write image to output video file
                # Uncomment this line below if you need to save the output to a video
                out.write(image)

            # Open image to show the output with detected objects
            # cv2.imshow("Image", image)

            yield image, objects

    # For debug
    else:
        print("[INFO] No object detected.")
        print("---------------------------------------------")


def write_out_video_init(image, output_name):
    """Initialize writing output video
    This need to be placed and initialized before the while loop
    :param image: image from OpenCV video capture
    :param output_name: name for the output file (excl. extension)
    :return: Video Writer output details
    """
    # Getting image shape
    img_row, img_col = image.shape[:2]

    # Video writer using XVID
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    # Video writer to write images to output.mp4
    out = cv2.VideoWriter(f"{output_name}.mp4", fourcc, 20.0, (img_col, img_row))

    return out


def teardown_obj_detection(obj_names):
    """Tearing down anything used for object detections
    :param obj_names: opened file of the object labels
    :return: none
    """
    # Closing object labels file
    obj_names.close()

    # Close all open windows
    cv2.destroyAllWindows()

    sleep(1)
    print("[INFO] Teardown of object detection completed.")
