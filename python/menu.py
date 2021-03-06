# -*- coding:utf-8 -*-
import LCD_1in44
import LCD_Config
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont,ImageColor
import threading
import time
from os import listdir
from os.path import isfile, join

KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16
#init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

def time_white():
        global draw
        draw.text((80, 118), "00:00:00", fill = "WHITE")


def open_folder(what):
        mypath =  "/boot/led-hat/code/menus/%s"%(what)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        return onlyfiles
def setup():

        # 240x240 display with hardware SPI:
        disp = LCD_1in44.LCD()
        Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT #SCAN_DIR_DFT = D2U_L2R
        disp.LCD_Init(Lcd_ScanDir)
        disp.LCD_Clear()
        # Create blank image for drawing. Make sure to create image with mode '1' for 1-bit color.
        width = 128; height = 128; image = Image.new('RGB', (width, height));
        return disp,image

def main_menu(disp,image):

        global draw
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        #Draw time background
        draw.rectangle((128,128,69,118),outline = "WHITE",fill="WHITE")

        draw.text((15, 10), 'Video Games', fill = "WHITE")
        draw.text((15, 20), 'Apps & tools', fill = "WHITE")
        disp.LCD_ShowImage(image,0,0)

        i = 0

        while 1:

                #Draw Time
                threading.Timer(1,time_white).start()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                draw.text((80, 118), str(current_time), fill = "RED")

                if i <= 0 :
                        i = 1
                if i > 2 :
                        i = 2
                if GPIO.input(KEY_UP_PIN) == 0:
                        i -= 1
                if GPIO.input(KEY_DOWN_PIN) == 0:
                        i += 1

                if i == 1: # button is released
                        draw.text((15, 10), 'Video Games', fill = "RED")
                        if GPIO.input(KEY_RIGHT_PIN) == 0:
                                return i
                else:
                        draw.text((15, 10), 'Video Games', fill = "WHITE")
                if i == 2:
                        draw.text((15, 20), 'Apps & tools', fill = "RED")
                        if GPIO.input(KEY_RIGHT_PIN) == 0:
                                return i
                else:
                        draw.text((15, 20), 'Apps & tools', fill = "WHITE")

                disp.LCD_ShowImage(image,0,0)

def open_menu(arr,disp,image):

        global draw
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,128,128), outline=0, fill=0)

        #Draw time background
        draw.rectangle((128,128,69,118),outline = "WHITE",fill="WHITE")

        #Draw all files
        for a in range(len(arr)):
                draw.text((15, 10*a+10), str(arr[a])[:-3], fill = "WHITE")

        disp.LCD_ShowImage(image,0,0)

        i = 0
        end_i = len(arr)

        while 1:

                #Draw Time
                threading.Timer(1,time_white).start()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                draw.text((80, 118), str(current_time), fill = "RED")

                #Keys Input
                if i < 0 :
                        i = 0
                if i > end_i :
                        i = end_i
                if GPIO.input(KEY_UP_PIN) == 0:
                        i -= 1
                if GPIO.input(KEY_DOWN_PIN) == 0:
                        i += 1
                if GPIO.input(KEY_RIGHT_PIN) == 0:
                        return execute_script(str(arr[i]))
                if GPIO.input(KEY_LEFT_PIN) == 0:
                        return main_menu(disp,image)

                #Draw red if selected
                for a in range(len(arr)):
                        if i == a:
                                draw.text((15, 10*a+10), str(arr[a])[:-3], fill = "RED")
                        else:
                                draw.text((15, 10*a+10), str(arr[a])[:-3], fill = "WHITE")



                disp.LCD_ShowImage(image,0,0)

def execute_script(what):
        print what


#MAIN CODE
disp,image = setup()
width = 128; height = 128;
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
print "**STARTING**"

i = main_menu(disp,image)
time.sleep(1)
disp.LCD_Clear()
if i == 1:
        arr = open_folder("videogames")
        open_menu(arr,disp,image)
if i == 2:
        arr = open_folder("appstools")
        open_menu(arr,disp,image)