import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect")
    else:
        print("Expected disconnect")

def on_message(client, userdata, message):
    print("Received message: \"" + str(message.payload) + "\" on topic \"" + 
            message.topic + "\" with QoS " + str(message.qos))

def main():
    print("MQTT Subscriber")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect_async("mqtt.eclipseprojects.io")
    client.loop_start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            break

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
