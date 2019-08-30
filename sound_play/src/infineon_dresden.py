#!/usr/bin/env python
import rospy
import sys
from roboy_cognition_msgs.srv import PlaySound, PlaySoundRequest

basepath = "/home/roboy/Documents/infineon-dresden/"
names = [
    "1-hey.wav",
    "2-glueckwunsch.wav",
    "3-mikrophonen.wav",
    "4-MEMS.wav",
    "5-klar.wav",
    "6-power.wav",
    "7-magnet.wav",
    "8-kamerachip.wav",
    "9-radar.wav",
    "10-kaum.wav",
    "11-sim.wav",
    "12-spass.wav",
    "13-kommher.wav"]

if __name__ == '__main__':

    # emotions = []
    play_sound_srv = rospy.ServiceProxy("/roboy/matrix/sound/play", PlaySound)
    play_sound_srv(PlaySoundRequest(filepath=basepath+names[int(sys.argv[1])-1], emotions=[], timestamps=[]))
    # play_sound_srv(lookup["smd_21"])
