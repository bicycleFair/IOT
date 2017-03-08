import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json, time
import ssl

pins = [17]


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def gpio_setlow(m):
    for pin in pins:
        if pin != m:
            GPIO.output(pin, GPIO.LOW)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    message = str(msg.payload)
    if message == "on":
        GPIO.output(17, True)
    else:
        GPIO.output(17, False)


#creating a client with client-id=mqtt-test
client = mqtt.Client()
client.tls_set(ca_certs="/home/pi/client/ca.crt",certfile="/home/pi/client/client.crt",keyfile="/home/pi/client/client.key",
                cert_reqs=ssl.CERT_REQUIRED,
              	tls_version=ssl.PROTOCOL_TLSv1_2,
		ciphers=None)
client.on_connect = on_connect
mqtt.on_subscribe = on_subscribe
client.on_message = on_message
gpio_setup()

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support



#mqttc.tls_insecure_set(True)

#connecting to
client.connect("129.63.17.141", 8883, 60)
client.subscribe("encyclopedia/#", qos=1)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

#gpio_destroy()


