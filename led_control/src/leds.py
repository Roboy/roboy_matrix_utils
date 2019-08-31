#!/usr/bin/env python

import rospy
import time
import numpy
import random
from roboy_control_msgs.msg import ControlLeds
from std_msgs.msg import Empty, Int32
import math

class MatrixLeds(object):
    """docstring for MatrixLeds"""
    def __init__(self):
        super(MatrixLeds, self).__init__()
        self.run = True
        self.channels = 4 # red green white blue
        self.leds_num = 35
        self.mode=0

    def write_pixels(self,pixels):
        # image is a list of size 4*36
        with open('/dev/matrixio_everloop','wb') as bin_file:
            bin_file.write(bytearray(pixels))
        bin_file.close()


    def dimming_puls(self, duration=0):
        # mode 1
        # dims in & out changing colors
        while True:
            if (duration!=0 and time.time()-start>duration):
                break
            #color = [0,0,0,half_brightness]
            pixels  = color * self.leds_num
            self.write_pixels(pixels)
            # self.show(pixels)
            time.sleep(0.02)
            if (count!=1 and (count-1)%brightness==0):
                d = -d
            if((count-1)%(2*brightness)==0):
            #    print "CHANGED COLOR"
                if (pos==3):
                    pos=0
                else:
                    pos += 1
            half_brightness += d
            count += abs(d)
            color = [0]*4
            color[pos] = half_brightness
            pixels = pixels[-2:] + pixels[:-2]

    def tail_clock(self, duration=0):
        # mode 2
        brightness = 1
        tail = 15
        led = 0
        #print "duration: ",duration
        start = time.time()
        while self.run and self.mode==2:
            if (duration!=0 and time.time()-start > duration):
                break
            intensity = brightness
            pixels = [0] * self.channels * self.leds_num
            if (led > 35 or led < 0):
                led=0
            for l in range(led-tail,led):
                intensity += 4
                pixels[l*self.channels+3]=intensity
            self.write_pixels(pixels)
            led +=1
            time.sleep(0.02)

    def set_color(self, red, green, blue, white):
        color_array = []
        for x in range(0,30):
            color_array += [red, green, blue, white]
        self.write_pixels(color_array)

    def turn_off(self):
        self.write_pixels([0]*self.channels*self.leds_num)

    def color_wave(self, wait=0.04):
        brightness = 0
        tick = 1
        stripsize = self.leds_num/2
        # cycle = stripsize*25

        pixel_colors = []

        # while (tick % cycle):
        while self.run and self.mode == 4:
            tick += 1
            offset = self.map2PI(tick*2)
            pixel_colors = []
            for i in range(0, self.leds_num):
                ang = self.map2PI(i) - offset
                rsin = math.sin(ang)
                gsin = math.sin(2.0 * ang / 3.0 + self.map2PI(int(stripsize/6)))
                bsin = math.sin(4.0 * ang / 5.0 + self.map2PI(int(stripsize/3)))
                pixel_color = [self.trig_scale(rsin), self.trig_scale(gsin), self.trig_scale(bsin), brightness]
                pixel_colors += pixel_color
            self.write_pixels(pixel_colors)
            time.sleep(wait)

    def map2PI(self, i):
        return math.pi*2.0*float(i) / float(self.leds_num)

    def trig_scale(self, val):
        val += 1.0
        val *= 5.0 #127.0
        return int(val) & 255

def mode_callback(msg):
    leds.run = True
    if (msg.mode==0):
        print "off"
        leds.mode=0
        leds.turn_off()
    elif (msg.mode==1):
        leds.mode=1
        print "puls"
        leds.dimming_puls(msg.duration)
    elif (msg.mode==2):
        leds.mode=2
        print "tail"
        leds.tail_clock(msg.duration)

def off_callback(msg):
    print "off"
    leds.run = False
    leds.turn_off()

def freeze_callback(msg):
    print "freeze"
    leds.run = False
    leds.mode=-1
    leds.set_color(0,0,0,15)

def mode_simple_callback(msg):
    leds.run = True
    if (msg.data==0):
        print "off"
        leds.mode=0
        leds.turn_off()
    elif (msg.data==1):
        leds.mode=1
        print "puls"
        leds.dimming_puls(0)
    elif (msg.data==2):
        leds.mode=2
        print "tail"
        leds.tail_clock(0)
    elif (msg.data==3):
        leds.mode = 3
        for i in range(5):
            print "red"
            leds.set_color(255,0,0,5)

            time.sleep(0.5)
            print "blue"
            leds.set_color(0,0,255,5)
            time.sleep(0.5)
    elif (msg.data == 4):
        leds.mode = 4
        print "rainbow"
        leds.color_wave()

def led_listener():
    rospy.init_node('roboy_led_control')
    rospy.Subscriber("/roboy/control/matrix/leds/mode", ControlLeds, mode_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/off", Empty, off_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/freeze", Empty, freeze_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/mode/simple", Int32, mode_simple_callback)
    leds.mode=1
    leds.dimming_puls(4)
    # leds.turn_off()
    # time.sleep(1)
    # leds.color_wave()
    #import pdb; pdb.set_trace()
    rospy.spin()



if __name__ == '__main__':
    global leds
    leds = MatrixLeds()
    led_listener()
