import paho.mqtt.publish as publish


def send_msg_by_mqtt(pi_ip, channel="blackbeard", message="Hello from DevGlitch!"):
    """Send a message to the raspberry pi using MQTT protocol
    :param pi_ip: Address IP of the raspberry pi
    :param channel: MQTT channel name
    :param message: Text of the message
    :return: publish single MQTT message
    """
    publish.single(channel, message, hostname=pi_ip)
