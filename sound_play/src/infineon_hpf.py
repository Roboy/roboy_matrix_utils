#!/usr/bin/env python
import rospy
import sys
from roboy_cognition_msgs.srv import PlaySound, PlaySoundRequest

basepath = rospy.get_param("base_path")
lookup = {"div_1": PlaySoundRequest(filepath=basepath+"Division/1.wav", emotions=["img:money"], timestamps=[5.0]),
          "div_2": PlaySoundRequest(filepath=basepath+"Division/2.wav", emotions=[], timestamps=[]),
          "div_3": PlaySoundRequest(filepath=basepath+"Division/3.wav", emotions=[], timestamps=[]),
          "div_4": PlaySoundRequest(filepath=basepath+"Division/4.wav", emotions=[], timestamps=[]),
          "div_5": PlaySoundRequest(filepath=basepath+"Division/5.wav", emotions=[], timestamps=[]),
          "smd_1": PlaySoundRequest(filepath=basepath+"SMD/_1_.wav", emotions=[], timestamps=[]),
          "smd_2": PlaySoundRequest(filepath=basepath+"SMD/_2_.wav", emotions=[], timestamps=[]),
          "smd_3": PlaySoundRequest(filepath=basepath+"SMD/_3_.wav", emotions=[], timestamps=[]),
          "smd_4": PlaySoundRequest(filepath=basepath+"SMD/_4_.wav", emotions=[], timestamps=[]),
          "smd_5": PlaySoundRequest(filepath=basepath+"SMD/_5_.wav", emotions=[], timestamps=[]),
          "smd_6": PlaySoundRequest(filepath=basepath+"SMD/_6_.wav", emotions=[], timestamps=[]),
          "smd_7": PlaySoundRequest(filepath=basepath+"SMD/_7_.wav", emotions=[], timestamps=[]),
          "smd_8": PlaySoundRequest(filepath=basepath+"SMD/_8_.wav", emotions=[], timestamps=[]),
          "smd_9": PlaySoundRequest(filepath=basepath+"SMD/_9_.wav", emotions=[], timestamps=[]),
          "smd_10": PlaySoundRequest(filepath=basepath+"SMD/_10_.wav", emotions=[], timestamps=[]),
          "smd_11": PlaySoundRequest(filepath=basepath+"SMD/_11_.wav", emotions=[], timestamps=[]),
          "smd_12": PlaySoundRequest(filepath=basepath+"SMD/_12_.wav", emotions=[], timestamps=[]),
          "smd_13": PlaySoundRequest(filepath=basepath+"SMD/_13_.wav", emotions=[], timestamps=[]),
          "smd_14": PlaySoundRequest(filepath=basepath+"SMD/_14_.wav", emotions=[], timestamps=[]),
          "smd_15": PlaySoundRequest(filepath=basepath+"SMD/_15_.wav", emotions=[], timestamps=[]),
          "smd_16": PlaySoundRequest(filepath=basepath+"SMD/_16_.wav", emotions=[], timestamps=[]),
          "smd_17": PlaySoundRequest(filepath=basepath+"SMD/_17_.wav", emotions=[], timestamps=[]),
          "smd_18": PlaySoundRequest(filepath=basepath+"SMD/_18_.wav", emotions=[], timestamps=[]),
          "smd_19": PlaySoundRequest(filepath=basepath+"SMD/_19_.wav", emotions=[], timestamps=[]),
          "smd_20": PlaySoundRequest(filepath=basepath+"SMD/_20_.wav", emotions=[], timestamps=[]),
          "smd_21": PlaySoundRequest(filepath=basepath+"SMD/_21_.wav", emotions=[], timestamps=[])}

if __name__ == '__main__':

    # emotions = []
    play_sound_srv = rospy.ServiceProxy("/roboy/matrix/sound/play", PlaySound)
    play_sound_srv(lookup[sys.argv[1]])
    # play_sound_srv(lookup["smd_21"])