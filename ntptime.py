"""retrieves time from ntpserver and displays it on oled screen"""

import time
import ntptime
import machine
import ssd1306

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(64, 48, i2c) # width, height, pins

def setTime():
    global LASTUPDATE
    global UPDATEINTERVAL
    LASTUPDATE = time.time()
    try:
        ntptime.settime()
        UPDATEINTERVAL = 300 #5mins
        print('succesfully synced time from ntp server: ' + ntptime.host)
        print('next update in ' + str(UPDATEINTERVAL) + ' seconds')
        # return True
    except OSError:
        UPDATEINTERVAL = 10 #seconds
        print('error, couldn\'t retrieve time')
        print('trying again in ' + str(UPDATEINTERVAL) + ' seconds')
        # return False

def checkUpdate(last, interv):
    if time.time() - (interv) > last:
        return True
    else:
        return False

def pad(p):
    if p < 10:
        return '0' + str(p)
    else:
        return str(p)

def printTime(h, m, s):
    print(time.localtime())
    oled.fill(0) # clear the screen
    oled.text(pad(h + 1) + ':' + pad(m) + ':' + pad(s), 0, 0) #hack for BST!!
    oled.show()

def printBinTime(h, m, s):
    print(time.localtime())
    oled.fill(0) # clear the screen
    oled.text("{0:08b}".format(h + 1), 0, 0) #hack for BST!!
    oled.text("{0:08b}".format(m), 0, 10)
    oled.text("{0:08b}".format(s), 0, 20) 
    oled.show()

setTime()
oldTime = time.time()

while True:
    if checkUpdate(LASTUPDATE, UPDATEINTERVAL) == True:
        setTime()

    if time.time() != oldTime:
        oldTime = time.time()
        # printTime(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        printBinTime(time.localtime()[3], time.localtime()[4], time.localtime()[5])
