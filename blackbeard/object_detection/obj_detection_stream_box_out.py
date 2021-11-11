# Adapted from repo botwizer by DevGltich
# https://github.com/DevGlitch/botwizer

# Resources used:
# https://github.com/AlexeyAB/darknet
# https://www.youtube.com/watch?v=Z_uPIUbGCkA

import cv2
import numpy as np
from time import sleep


def stream_object_detection_box(rtsp_url, config_path, weights_path, labels_path):
    """Running YOLO on a streaming feed to detect objects
    :param rtsp_url: RTSP URL of stream to analyse
    :param config_path: path of the .cfg file
    :param weights_path: path of the .weights file
    :param labels_path: path of the .names file
    :return: video with bounding box and label of object(s) detected
    :rtype: OpenCV window
    """

    # INFO
    print("[INFO] Initializing...")
    sleep(1)

    # Reads and load model stored in Darknet model files
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    print("[INFO] Model loaded.")
    sleep(1)

    # Object Labels
    obj_names = open(labels_path)
    obj_labels = obj_names.read().strip().split("\n")
    print("[INFO] Object labels loaded.")
    sleep(1)

    # initialize a list of colors to represent each possible class label
    # np.random.seed(14)
    colors = np.random.randint(0, 255, size=(len(obj_labels), 3), dtype="uint8")

    # Reads stream RTSP URL
    print("[INFO] Stream Capture Starting...")
    stream_video = cv2.VideoCapture(rtsp_url)
    print("[INFO] Stream Capture Started.")

    # # For writing output video
    _, image = stream_video.read()
    # img_row, img_col = image.shape[:2]
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (img_col, img_row))

    # INFO
    print("[INFO] Starting Object Detection Analysis...")

    while stream_video.isOpened():

        # INFO
        print("[INFO] Running...")

        # FPS
        # fps = stream_video.get(cv2.CAP_PROP_FPS)
        # print("[INFO] FPS using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

        _, image = stream_video.read()
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
        outputs = net.forward(layer_name)

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

            for i in NMS.flatten():

                # Extract coordinates of each grid box
                (x, y) = (grid[i][0], grid[i][1])
                (w, h) = (grid[i][2], grid[i][3])

                # Create a bounding box around the object
                color = [int(c) for c in colors[labels[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=2)

                # Add label to the bounding box
                text = "{}: {:.4f}".format(obj_labels[labels[i]], probabilities[i])  # w/ probabilities
                # text = "{}".format(obj_labels[labels[i]])  # w/o probabilities
                cv2.putText(
                    image, text, (x, y - 5),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                    color=color, thickness=2
                )

            # Write image to output video file
            # Uncommment this line below if you need to save the output to a video
            # out.write(image)

            # Open image to show the output with detected objects
            # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)  # for smaller size window
            cv2.imshow("Image", image)

        if ord("q") == cv2.waitKey(1):
            print("[INFO] Stopping...")
            break

        # else:
        #     cv2.imshow("Image", image)

    # Close names file
    obj_names.close()

    # Release stream
    stream_video.release()

    # Close all open windows
    cv2.destroyAllWindows()

    # INFO
    print("[INFO] Done.")
