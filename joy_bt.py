#!/usr/bin/env python3

from ev3dev.ev3 import *
import evdev

device = evdev.InputDevice('/dev/input/event2')
StatusGo = 0
StatusLR = 0
speed = 100

real_speedB = 0
real_speedC = 0
speedB = 0
speedC = 0

STOP = False

B = LargeMotor('outB')
C = LargeMotor('outC')

while not STOP:
    gen = device.read()
    try:
       for event in gen:
           if event.type == evdev.ecodes.EV_KEY:
               myStr = str(event)
                 
               if myStr.find("code 168, type 01, val 00") >= 0:
                   #print ("Go left! <>")
                   StatusLR = 0         
               if myStr.find("code 168, type 01, val 01") >= 0:
                   #print ("Go left! <>")
                   StatusLR = -1
               if myStr.find("code 168, type 01, val 02") >= 0:
                   #print ("Go left! FAST!")
                   StatusLR = -2

               if myStr.find("code 208, type 01, val 00") >= 0:
                   #print ("Go right! <>")
                   StatusLR = 0
               if myStr.find("code 208, type 01, val 01") >= 0:
                   #print ("Go right! <>")
                   StatusLR = 1
               if myStr.find("code 208, type 01, val 02") >= 0:
                   #print ("Go right! FAST!")
                   StatusLR = 2	 	 
               if myStr.find("code 172, type 01, val 00") >= 0:
                   #print ("STOP")
                   StatusGo = 0
               if myStr.find("code 172, type 01, val 01") >= 0:
                   #print ("GO")
                   StatusGo = speed*0.75
               if myStr.find("code 172, type 01, val 02") >= 0:
                   #print ("GO")
                   StatusGo = speed
               if myStr.find("code 114, type 01, val 00") >= 0:
                   #print ("STOP")
                   StatusGo = 0
               if myStr.find("code 114, type 01, val 01") >= 0:
                   #print ("GO BREAK")
                   StatusGo = -1*(speed * 0.75)
               if myStr.find("code 114, type 01, val 02") >= 0:
                   #print ("GO BREAK")
                   StatusGo = -1*speed
         
               if myStr.find("code 164, type 01, val 02") >= 0:
                   print ("BREAK! STOP PROGRAMM")
                   STOP = True

               if myStr.find("code 164, type 01, val 01") >= 0:
                   print ("Speed Stabil")
                   speed = 75
               if myStr.find("code 115, type 01, val 01") >= 0:
                   speed = speed - 5
                   if(speed < 5):
                       speed = 5        
               if myStr.find("code 115, type 01, val 02") >= 0:
                   speed = speed - 1
                   if(speed < 5): 
                       speed = 5
               if myStr.find("code 113, type 01, val 01") >= 0:
                   speed = speed + 5
                   if(speed > 100): 
                       speed = 100
               if myStr.find("code 113, type 01, val 02") >= 0:
                   speed = speed + 1
                   if(speed > 100): 
                       speed = 100

    except IOError:
        pass
      
    speedB = StatusGo
    speedC = StatusGo

    if(StatusLR < 0):
        speedB = speedB-(25*abs(StatusLR))
        speedC = speedC+(25*abs(StatusLR))         
    if(StatusLR > 0):
        speedC = speedC-(25*StatusLR)
        speedB = speedB+(25*StatusLR)

    if(speedB > 100):
        speedB = 100
    if(speedC > 100):
        speedC = 100
    if(speedB < -100):
        speedB = -100
    if(speedC < -100):
        speedC = -100

    if(abs(speedB) > 5 and abs(speedC) > 5):
        real_speedB = real_speedB*0.95 + speedB*0.05
        real_speedC = real_speedC*0.95 + speedC*0.05

    if(speedB == 0 and speedC == 0):
        real_speedB = real_speedB*0.95
        real_speedC = real_speedC*0.95

    if(speedB == 0 and abs(real_speedB) < 5):
        real_speedB = 0
    if(speedC == 0 and abs(real_speedC) < 5):
        real_speedC = 0
             
    B.run_forever(speed_sp=real_speedB*9)
    C.run_forever(speed_sp=real_speedC*9)
         
B.stop(stop_action="hold")
C.stop(stop_action="hold")

Sound.beep()

