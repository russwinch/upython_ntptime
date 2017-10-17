"""retrieves time from ntpserver and displays it on oled screen"""

import time
import ntptime  # this file name is same as this module - need to change
import machine
import ssd1306

LASTUPDATE = None
UPDATEINTERVAL = None


i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(64, 48, i2c) # width, height, pins

def set_time():
    """set time function"""
    global LASTUPDATE       # these globals need to be difine at global level
    global UPDATEINTERVAL
    LASTUPDATE = time.time()
    try:
        ntptime.settime()
        UPDATEINTERVAL = 300 #5mins - MAGIC NUMBER!
        print('succesfully synced time from ntp server: ' + ntptime.host)
        print('next update in ' + str(UPDATEINTERVAL) + ' seconds')
        # return True
    except OSError:
        UPDATEINTERVAL = 10 #seconds
        print('error, couldn\'t retrieve time')
        print('trying again in ' + str(UPDATEINTERVAL) + ' seconds')
        # return False

def check_update(last, interv):
    """check updeate function"""
    if time.time() - (interv) > last:
        return True     # else: not required
    return False

def pad(p):
    """pad function"""
    if p < 10:  # MAGIC NUMBER!
        return '0' + str(p)     # else: not required
    return str(p)

def print_time(h, m, s):
    """print time function"""
    print(time.localtime())
    oled.fill(0) # clear the screen
    oled.text(pad(h + 1) + ':' + pad(m) + ':' + pad(s), 0, 0) #hack for BST!!
    oled.show()

def print_bin_time(h, m, s):
    """print bin time function"""
    print(time.localtime())
    oled.fill(0) # clear the screen
    oled.text("{0:08b}".format(h + 1), 0, 0) #hack for BST!!
    oled.text("{0:08b}".format(m), 0, 10)
    oled.text("{0:08b}".format(s), 0, 20)
    oled.show()

set_time()
oldTime = time.time()

while True:
    if check_update(LASTUPDATE, UPDATEINTERVAL): # '== True' no need
        set_time()

    if time.time() != oldTime:
        oldTime = time.time()
        # printTime(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        print_bin_time(time.localtime()[3], time.localtime()[4], time.localtime()[5])
