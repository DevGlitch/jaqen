import cv2
import os
import time
import numpy as np


def vid_object_detection_box(vid_path):
    """Running YOLO on a video to detect objects
    :param vid_path: path of video to analyse
    :return: video with object(s) detected
    :rtype: mp4
    """

    # Files from Darknet

    # YOLO V3 - For general object detection
    # config = "../object_detection/yolo/cfg/yolov3.cfg"
    # weights = "../object_detection/yolo/weights/yolov3.weights"

    # Custom YOLOV4-Tiny Trained on Cards Dataset
    config = "../object_detection/yolo/cfg/yolov4-tiny-blackbeard.cfg"
    weights = "../object_detection/yolo/weights/yolov4-tiny-obj_170000.weights"

    # Reads network model stored in Darknet model files
    # OpenCV dnn module is used to load YOLO network
    net = cv2.dnn.readNetFromDarknet(config, weights)

    # Using Common Objects in Context (COCO) Labels
    # (https://cocodataset.org/)
    # obj_names = open("../object_detection/yolo/obj_names/coco.names")
    # obj_labels = obj_names.read().strip().split("\n")

    # Playing Cards Labels
    obj_names = open("yolo/obj_names/blackbeard.names")
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

            out.write(image)

            # Open image to show the output with detected objects
            # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)  # for smaller size window
            cv2.imshow("Image", image)

        if ord("q") == cv2.waitKey(1):
            break

    # Close names file
    obj_names.close()

    # Close video file
    vid_cap.release()

    # Close all open windows
    cv2.destroyAllWindows()
