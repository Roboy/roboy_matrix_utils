#!/usr/bin/env python

import rospy
import time
import numpy
import random
from roboy_communication_control.msg import ControlLeds
from std_msgs.msg import Empty, Int32


class MatrixLeds(object):
    """docstring for MatrixLeds"""

    def __init__(self):
        super(MatrixLeds, self).__init__()
        self.run = True
        self.channels = 4  # red green white blue
        self.leds_num = 36
        self.mode = 0

    def write_pixels(self, pixels):
        # image is a list of size 4*36
        with open('/dev/matrixio_everloop', 'wb') as bin_file:
            bin_file.write(bytearray(pixels))
        bin_file.close()

    def dimming_puls(self, duration=0):
        # mode 1
        # dims in & out changing colors
        brightness = 50
        half_brightness = 0  # int(100 / 2)
        # leds_num = 36
        pixels = [0, 0, 0, half_brightness] * self.leds_num
        count = 0
        d = 1
        pos = 0
        color = [0, 0, 0, half_brightness]
        start = time.time()
        while self.run and self.mode == 1:
            if (duration != 0 and time.time() - start > duration):
                break
            # color = [0,0,0,half_brightness]
            pixels = color * self.leds_num
            self.write_pixels(pixels)
            # self.show(pixels)
            time.sleep(0.02)
            if (count != 1 and (count - 1) % brightness == 0):
                d = -d
            if ((count - 1) % (2 * brightness) == 0):
                #    print "CHANGED COLOR"
                if (pos == 3):
                    pos = 0
                else:
                    pos += 1
            half_brightness += d
            count += abs(d)
            color = [0] * 4
            color[pos] = half_brightness
            # pixels = pixels[-2:] + pixels[:-2]

    def tail_clock(self, duration=0):
        # mode 2
        brightness = 3
        tail = 30
        led = 0
        # print "duration: ",duration
        start = time.time()
        while self.run and self.mode == 2:
            if (duration != 0 and time.time() - start > duration):
                break
            intensity = brightness
            pixels = [0] * self.channels * self.leds_num
            if (led > 35 or led < 0):
                led = 0
            for l in range(led - tail, led):
                intensity += 4
                pixels[l * self.channels + 3] = intensity
            self.write_pixels(pixels)
            led += 1
            time.sleep(0.02)

    def pulsing_face(self, duration=0):
        # mode 1
        # dims in & out changing colors
        brightness = 50
        half_brightness = 0  # int(100 / 2)
        # leds_num = 36
        pixels = [0, 0, 0, half_brightness] * self.leds_num
        count = 0
        d = 1
        pos = 0
        color = [0, 0, 0, half_brightness]
        start = time.time()
        while self.run and self.mode == 3:
            if duration != 0 and time.time() - start > duration:
                break
            # color = [0,0,0,half_brightness]
            pixels = [0, 0, 0, 0]
            for i in range(1, self.leds_num):
                if i in [3, 4, 5, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]:
                    pixels += color
                else:
                    pixels += [0, 0, 0, 0]
            self.write_pixels(pixels)
            # self.show(pixels)
            time.sleep(0.02)
            if count != 1 and (count - 1) % brightness == 0:
                d = -d
            if (count - 1) % (2 * brightness) == 0:
                #    print "CHANGED COLOR"
                if pos == 3:
                    pos = 0
                else:
                    pos += 1
            half_brightness += d
            count += abs(d)
            color = [0] * 4
            color[pos] = half_brightness
            # pixels = pixels[-2:] + pixels[:-2]

    def point_towards(self, point_led, duration=8, color=3):
        # mode 2
        brightness = 50
        tail = 30
        led_r = point_led
        led_l = point_led
        # print "duration: ",duration
        start = time.time()
        # while mode == 2:
        #     if duration != 0 and time.time() - start > duration:
        #         break
        #     intensity = brightness
        #     pixels = [0] * channels * leds_num
        #     if led > 35 or led < 0:
        #         led = 0
        #     for l in range(led - tail, led):
        #         intensity += 4
        #         pixels[l * channels + 3] = intensity
        #     write_pixels(pixels)
        #     led += 1
        #     time.sleep(0.02)
        clockwise_r = False
        clockwise_l = True

        allowed_l = list()
        for i in range(1, 6):
            allowed_l.append(point_led - i)

        # map them to our range
        for i in range(len(allowed_l)):
            if allowed_l[i] < 0:
                allowed_l[i] = 36 + allowed_l[i]

        for i in range(len(allowed_l)):
            if allowed_l[i] > 35:
                allowed_l[i] = allowed_l[i] - 36
        print "allowed_l: ", allowed_l

        allowed_r = list()
        for i in range(1, 6):
            allowed_r.append(point_led + i)

        # map them to our range
        for i in range(len(allowed_r)):
            if allowed_r[i] < 0:
                allowed_r[i] = 36 + allowed_r[i]

        for i in range(len(allowed_r)):
            if allowed_r[i] > 35:
                allowed_r[i] = allowed_r[i] - 36
        print "allowed_r: ", allowed_r

        forbidden_l = list()
        for i in range(0, 36):
            if i not in allowed_l:
                forbidden_l.append(i)

        forbidden_r = list()
        for i in range(0, 36):
            if i not in allowed_r:
                forbidden_r.append(i)

        while self.run and self.mode == 4:
            if duration != 0 and time.time() - start > duration:
                break

            if led_l == 36:
                led_l = 0
            if led_r == 36:
                led_r = 0
            print "led_l: ", led_l
            print "led_r: ", led_r
            print "clockwise_l, ", clockwise_l
            print "clockwise_r, ", clockwise_r

            pixels = [0] * self.channels * self.leds_num
            pixels[led_r * self.channels + color] = brightness
            pixels[led_l * self.channels + color] = brightness

            self.write_pixels(pixels)

            if led_l in forbidden_l:
                clockwise_l = not clockwise_l

            if led_r in forbidden_r:
                clockwise_r = not clockwise_r

            if led_r == 0 and not clockwise_r:
                led_r = 36

            if led_l == 0 and not clockwise_l:
                led_l = 36

            if clockwise_r:
                led_r += 1
            else:
                led_r -= 1

            if clockwise_l:
                led_l += 1
            else:
                led_l -= 1

            time.sleep(0.05)

    def set_color(self, red, green, blue, white):
        color_array = []
        for x in range(0, 35):
            color_array += [red, green, blue, white]
        self.write_pixels(color_array)

    def turn_off(self):
        self.write_pixels([0] * self.channels * self.leds_num)


def mode_callback(msg):
    leds.run = True
    if msg.mode == 0:
        print "off"
        leds.mode = 0
        leds.turn_off()
    elif msg.mode == 1:
        leds.mode = 1
        print "puls"
        leds.dimming_puls(msg.duration)
    elif msg.mode == 2:
        leds.mode = 2
        print "tail"
        leds.tail_clock(msg.duration)
    elif msg.mode == 3:
        leds.mode = 3
        print "face"
        leds.pulsing_face(msg.duration)


def point_callback(msg):
    leds.mode = 4
    print "point"
    leds.point_towards(msg.data)


def off_callback(msg):
    print "off"
    leds.run = False
    leds.turn_off()


def freeze_callback(msg):
    print "freeze"
    leds.run = False
    leds.mode = -1
    leds.set_color(0, 0, 0, 15)


def mode_simple_callback(msg):
    leds.run = True
    if msg.data == 0:
        print "off"
        leds.mode = 0
        leds.turn_off()
    elif msg.data == 1:
        leds.mode = 1
        print "puls"
        leds.dimming_puls(0)
    elif msg.data == 2:
        leds.mode = 2
        print "tail"
        leds.tail_clock(0)
    elif msg.mode == 3:
        leds.mode = 3
        print "face"
        leds.pulsing_face(0)


def led_listener():
    rospy.init_node('roboy_led_control')
    rospy.Subscriber("/roboy/control/matrix/leds/mode", ControlLeds, mode_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/off", Empty, off_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/freeze", Empty, freeze_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/mode/simple", Int32, mode_simple_callback)
    rospy.Subscriber("/roboy/control/matrix/leds/point", Int32, point_callback)
    leds.mode = 1
    leds.dimming_puls(8)
    rospy.spin()


if __name__ == '__main__':
    global leds
    leds = MatrixLeds()
    led_listener()
