import paho.mqtt.client as mqtt
from random import random

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect")
    else:
        print("Expected disconnect")

def on_message(client, userdata, message):
    print("Received message: \"" + str(message.payload) + "\" on topic \"" + 
            message.topic + "\" with QoS " + str(message.qos))

def main():
    print("MQTT Publisher")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect_async("mqtt.eclipseprojects.io")
    client.loop_start()

    while True:
        try:
            key = input().lower()
            if key == "w":
                move = "FORWARD"
            elif key == "a":
                move = "LEFT"
            elif key == "s":
                move = "BACK"
            elif key == "d":
                move = "RIGHT"
            else:
                print("Invalid move")
                continue
            client.publish("ece180d/test", move, qos=1)
        except KeyboardInterrupt:
            break

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
