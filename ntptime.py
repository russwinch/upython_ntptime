""" retrieves time from ntpserver and displays it on oled screen"""

import time
import ntptime
import machine
import ssd1306

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(64, 48, i2c) # width, height, pins

ntptime.settime()
while True:
    print(time.localtime())

    oled.fill(0) # clear the screen
    oled.text(str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' +
            str(time.localtime()[5]), 0, 0)
    oled.show()

    time.sleep(1)
