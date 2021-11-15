"""
Originally from https://forums.raspberrypi.com/viewtopic.php?t=238538

Script to be stored in the Raspberry Pi in order to receive message from the MQTT local server.

Adapted and modified by DevGlitch
"""

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    """ When launching mqtt and receiving response from the server
    :return: displaying connection message
    """
    print("[INFO] MQTT Client successfully connected (result code "+str(rc) + ").")
    # Subscribing to the channel
    client.subscribe(channel)
    print("[INFO] Ready to listen to Blackbeard's instructions.")


def on_message(client, userdata, msg):
    """ When a message is received from the server
    :return: displaying server message
    """
    # Convert byte message to string
    message = str(msg.payload)

    # Display message while removing unnecessary characters
    print("[BLACKBEARD] " + message[2:-1])


# Setting up server and channel
server = "localhost"
channel = "blackbeard"

client = mqtt.Client()

# Print connection info when connected
client.on_connect = on_connect

# Print message when received from server
client.on_message = on_message

# Connecting to server
client.connect(server, 1883, 60)

# Looping until exit by user
client.loop_forever()
