import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np


server_socket = socket.socket()
server_socket.bind(("192.168.1.65", 8000))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        # Rewind the stream, open it as an image with PIL and do some
        image_stream.seek(0)
        image = Image.open(image_stream)
        image = np.array(image)
        #         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Raspi Cam', image)
        cv2.waitKey(10)

finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()