import paho.mqtt.client as mqtt
import ssl,time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("switch", help="remotely control LED")
args = parser.parse_args()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

#creating a client with client-id=mqtt-test
client = mqtt.Client()
client.on_connect = on_connect
mqtt.on_publish = on_publish

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support

client.tls_set(ca_certs="/Users/Joe/Desktop/mosquitto/client2/ca.crt",
	            certfile="/Users/Joe/Desktop/mosquitto/client2/client.crt",
	            keyfile="/Users/Joe/Desktop/mosquitto/client2/client.key",
                cert_reqs=ssl.CERT_REQUIRED,
              	tls_version=ssl.PROTOCOL_TLSv1_2,
		ciphers=None)

#mqttc.tls_insecure_set(True)

#connecting to
client.connect("129.63.17.143", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_start()
switch = args.switch
(rc, mid) = client.publish("encyclopedia/temperature", switch, qos=1)




