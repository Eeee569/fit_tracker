import RPi.GPIO as GPIO
import time
import requests
GPIO.setmode(GPIO.BCM)




channel = [3,5,7]
# or
for i in channel:
    print(i)
    GPIO.setup(i, GPIO.IN)


def send_output(output):
    r = requests.post('10.2.242.249', json={"ouput_list": output})
    print(r.status_code)


while(1):
    output = []
    for i in channel:
        if GPIO.input(i):
            output.append(1)
        else:
            output.append(0)
    send_output(output)
    print(output)
    time.sleep(1)