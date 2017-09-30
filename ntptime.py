"""retrieves time from ntpserver and displays it on oled screen"""

import time
import ntptime
import machine
import ssd1306

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(64, 48, i2c) # width, height, pins

def setTime():
    try:
        ntptime.settime()
        print('succesfully updated time')
    except OSError:
        print('error, couldn\'t retrieve time')

def pad(p):
    if p < 10:
        return '0' + str(p)
    else:
        return str(p)

def printTime(h, m, s):
    oled.fill(0) # clear the screen
    oled.text(pad(h + 1) + ':' + pad(m) + ':' + pad(s), 0, 0) #hack for BST!!
    oled.show()

setTime()

while True:
    print(time.localtime())
    printTime(time.localtime()[3], time.localtime()[4], time.localtime()[5])

    time.sleep(1)

