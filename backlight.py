#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

###############
# PHY === BCM #
###############
#  11  ==  17 # BTN_1
#  15  ==  22 # BTN_2
#  16  ==  23 # BTN_3
#  13  ==  27 # BTN_4
#  12  ==  18 # BL_0
###############

def bl_cb(freq):
    pwm.ChangeDutyCycle(25)
    print("***Backlight set to",freq)

# BCM GPIO Channels
BL_0 = 18
BTN_1 = 17
BTN_2 = 22
BTN_3 = 23
BTN_4 = 27

# Backlight Max Value
bl_cur = 100
bl_freq_max = 1023

# Use BCM Numbering
GPIO.setmode(GPIO.BCM)

# Declare GPIO_18 as OUTPUT
GPIO.setup(BL_0, GPIO.OUT)

# Initialize Button 1 on GPIO 17
GPIO.setup(BTN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initiaize at full brightness
pwm = GPIO.PWM(BL_0, bl_freq_max)
pwm.start(bl_cur)
time.sleep(1)

# Event Detects for buttons
GPIO.add_event_detect(BTN_1, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(BTN_2, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(BTN_3, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(BTN_4, GPIO.FALLING, bouncetime=200)

try:
    while 1:
        if GPIO.event_detected(BTN_1):
            if bl_cur > 25:
                bl_cur = bl_cur-25
            elif bl_cur <= 25:
                bl_cur = 1
            pwm.ChangeDutyCycle(bl_cur)
            print("brightness is: ",bl_cur)
        elif GPIO.event_detected(BTN_2):
            if bl_cur < 25:
                bl_cur = 25
            elif bl_cur >= 75:
                bl_cur = 100
            else:
                bl_cur += 25
            pwm.ChangeDutyCycle(bl_cur)
            print("brightness is: ",bl_cur)
        elif GPIO.event_detected(BTN_3):
            print("Button 3")
        elif GPIO.event_detected(BTN_4):
            pwm.ChangeDutyCycle(0)
            print("Button 4")
except KeyboardInterrupt:
    GPIO.cleanup()
