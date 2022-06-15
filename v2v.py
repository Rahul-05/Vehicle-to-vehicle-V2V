############################ Dependencies #################################
import subprocess as spc
#import bluetooth
import RPi.GPIO as GPIO
import time


############################################## Code ####################

#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 12
GPIO_ECHO = 22
motorPin13 = 13
motorPin11 = 11
motorPin16 = 16
motorPin18 = 18
enablePin = 15
 
#set GPIO direction (IN / OUT)
#GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#GPIO.setup(GPIO_ECHO, GPIO.IN)

def rssi():
    res=spc.check_output("getsi")
    lis=res.split()
    lis2=[]
    for x in range(len(lis)):
        temp=lis[x]
        #print(temp)
        temp=str(temp, 'UTF-8')
        #print (temp)
        lis2.append(temp)
    idx=lis2.index('ESSID:"One"')
    idx=idx-2
    db = lis2[idx].replace('level=-', '')
    db = int(db)
    return db


def setup():    
    GPIO.setmode(GPIO.BOARD)
    # initialize the GPIO Pins to Output Mode
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(motorPin13, GPIO.OUT) 
    GPIO.setup(motorPin11, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)
    GPIO.setup(motorPin16, GPIO.OUT) 
    GPIO.setup(motorPin18, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)
    # set all the GPIO pins initially to LOW 
    GPIO.output(enablePin, GPIO.LOW)
    GPIO.output(motorPin13, GPIO.LOW)
    GPIO.output(motorPin11, GPIO.LOW)
        # initialize the GPIO Pins to Output Mode
 
    # set all the GPIO pins initially to LOW 
    GPIO.output(enablePin, GPIO.LOW)
    GPIO.output(motorPin16, GPIO.LOW)
    GPIO.output(motorPin18, GPIO.LOW)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def loop():
    # first, enable the channel
    pwm=GPIO.PWM(enablePin,110)
    pwm.start(70) 
    #GPIO.output(enablePin, 100)
    
    while True:
        val = input("Enter your value: ")
        print(val)
        dist = distance()
        db = rssi()
        if val == 'w':
            while True:
                 fwd()
                 dist = distance()
                 db = rssi()
                 if dist <= 40 and db>35:
                    overtake()
                 elif dist<=40 and db<35:
                    stop()
                 print('%.1f cm'% dist)
                 print(db)

        elif val == 's':
            back()

        elif val == 'a':
            left()

        elif val == 'd':
            right()

        elif val == 'o': # turn 45 and fwd
            pwm.start(80)
            overtake()

        elif val == 'q':
            destroy()

        elif val == 'x':
            stop()

       # elif dist <= 20:
           # overtake()
        

def fwd():
    GPIO.output(motorPin13, GPIO.HIGH)
    GPIO.output(motorPin11, GPIO.LOW)
    GPIO.output(motorPin16, GPIO.HIGH)
    GPIO.output(motorPin18, GPIO.LOW)

def back():
    GPIO.output(motorPin13, GPIO.LOW)
    GPIO.output(motorPin11, GPIO.HIGH)
    GPIO.output(motorPin16, GPIO.LOW)
    GPIO.output(motorPin18, GPIO.HIGH)


def left():
    GPIO.output(motorPin13, GPIO.LOW)
    GPIO.output(motorPin11, GPIO.HIGH)
    GPIO.output(motorPin16, GPIO.HIGH)
    GPIO.output(motorPin18, GPIO.LOW)

    
def right():
    GPIO.output(motorPin13, GPIO.HIGH)
    GPIO.output(motorPin11, GPIO.LOW)
    GPIO.output(motorPin16, GPIO.LOW)
    GPIO.output(motorPin18, GPIO.HIGH)

def overtake():
     right()
     time.sleep(1/3)
     fwd()
     time.sleep(0.45)
     left()
     time.sleep(0.375)
     fwd()
     time.sleep(0.5)
     left()
     time.sleep(1/2)
     fwd()
     time.sleep(0.35)
     right()
     time.sleep(0.42)
     fwd()

def stop():
    pwm=GPIO.PWM(enablePin,110)
    pwm.start(0)

def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    print("Initializing Resources")
    setup()
   # while True:
       # dist = distance()
       # print('%.1f cm'% dist )
       # time.sleep(1)

    try:
        loop()
    except KeyboardInterrupt:   # close the script by pressing CTRL + C
        destroy()

