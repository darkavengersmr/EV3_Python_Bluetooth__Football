#!/usr/bin/env python3

# Подключаем модуль для управления EV3
from ev3dev.ev3 import *
# Подключаем модуль для чтения данных с HID-устройств
import evdev

# Создаем объект device, измените на ваш /dev/input/event2
device = evdev.InputDevice('/dev/input/event2')

StatusGo = 0
StatusLR = 0

# Целевая скорость, робот наберет ее когда разгонится
speed = 100

# Реальная скорость, с нее робот стартует
real_speedB = 0
real_speedC = 0

speedB = 0
speedC = 0

# Признак зарершения программы (нажат акнопка Start на джойстике)
STOP = False

# Создаем объекты - моторы B и C
B = LargeMotor('outB')
C = LargeMotor('outC')

# Цикл пока не нажата кнопка Start на джойстике
while not STOP:
    # Читаем список событий с джойстика
    gen = device.read()
    try:
       # Для всех событий в списке
       for event in gen:
           # Выделяем те, которые возникли при нажатиях кнопок
           if event.type == evdev.ecodes.EV_KEY:
               # преобразуем такие события в строку myStr
               myStr = str(event)
               
               # если отпущена кнопка "Влево"
               if myStr.find("code 168, type 01, val 00") >= 0:
                   StatusLR = 0
               # если нажата кнопка "Влево"
               if myStr.find("code 168, type 01, val 01") >= 0:
                   StatusLR = -1
               # если удерживается кнопка "Влево"
               if myStr.find("code 168, type 01, val 02") >= 0:
                   StatusLR = -2
               # если отпущена кнопка "Вправо"
               if myStr.find("code 208, type 01, val 00") >= 0:
                   StatusLR = 0
               # если нажата кнопка "Вправо"
               if myStr.find("code 208, type 01, val 01") >= 0:
                   StatusLR = 1
               # если удерживается кнопка "Вправо"
               if myStr.find("code 208, type 01, val 02") >= 0:
                   StatusLR = 2
               # если отпущена кнопка "Вперед"	 	 
               if myStr.find("code 172, type 01, val 00") >= 0:
                   StatusGo = 0
               # если нажата кнопка "Вперед"
               if myStr.find("code 172, type 01, val 01") >= 0:
                   StatusGo = speed*0.75
               # если удерживается кнопка "Вперед"
               if myStr.find("code 172, type 01, val 02") >= 0:
                   StatusGo = speed
               # если отпущена кнопка "Назад"
               if myStr.find("code 114, type 01, val 00") >= 0:
                   StatusGo = 0
               # если нажата кнопка "Назад"
               if myStr.find("code 114, type 01, val 01") >= 0:
                   StatusGo = -1*(speed * 0.75)
               # если удерживается кнопка "Назад"
               if myStr.find("code 114, type 01, val 02") >= 0:
                   #print ("GO BREAK")
                   StatusGo = -1*speed
               # если нажата кнопка "Start"         
               if myStr.find("code 164, type 01, val 02") >= 0:
                   print ("BREAK! STOP PROGRAMM")
                   STOP = True
               # Кнопка - среднее значение скорости
               if myStr.find("code 164, type 01, val 01") >= 0:
                   speed = 75
               # Кнопка нажата - уменьшить скорость
               if myStr.find("code 115, type 01, val 01") >= 0:
                   speed = speed - 5
                   if(speed < 5):
                       speed = 5
               # Кнопка удерживается - уменьшить скорость        
               if myStr.find("code 115, type 01, val 02") >= 0:
                   speed = speed - 1
                   if(speed < 5): 
                       speed = 5
               # Кнопка нажата - увеличить скорость
               if myStr.find("code 113, type 01, val 01") >= 0:
                   speed = speed + 5
                   if(speed > 100): 
                       speed = 100
               # Кнопка удерживается - увеличить скорость
               if myStr.find("code 113, type 01, val 02") >= 0:
                   speed = speed + 1
                   if(speed > 100): 
                       speed = 100

    except IOError:
        pass
    
    # перебрасываем статусы нажатий в мощности моторов  
    speedB = StatusGo
    speedC = StatusGo
    
    # Поворот влево
    if(StatusLR < 0):
        speedB = speedB-(25*abs(StatusLR))
        speedC = speedC+(25*abs(StatusLR))         
    # поворот вправо
    if(StatusLR > 0):
        speedC = speedC-(25*StatusLR)
        speedB = speedB+(25*StatusLR)
    
    # ограничение скорости
    if(speedB > 100):
        speedB = 100
    if(speedC > 100):
        speedC = 100
    if(speedB < -100):
        speedB = -100
    if(speedC < -100):
        speedC = -100

    # плавный разгон и торможение
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
    
    # подаем рассчитанные мощности на моторы        
    B.run_forever(speed_sp=real_speedB*9)
    C.run_forever(speed_sp=real_speedC*9)

# останавливаем моторы после вылета из цикла         
B.stop(stop_action="hold")
C.stop(stop_action="hold")

# сигнал завершения программы
Sound.beep()
