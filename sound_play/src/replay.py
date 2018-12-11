#!/usr/bin/env python
#coding=utf-8
import rospy
import pyaudio
import wave
from roboy_cognition_msgs.srv import Talk

def play(req):
    filename = req.text
    #define stream chunk
    chunk = 1024

    #open a wav format music
    f = wave.open(filename,"rb")
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  \
                    channels = f.getnchannels(),  \
                    rate = f.getframerate(),  \
                    output = True)
    #read data
    data = f.readframes(chunk)

    #play stream  
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()

    return True


def replay_server():
    rospy.init_node('sound_play_server')
    s = rospy.Service('/roboy/matrix/sound/play', Talk, play)
    print "Ready to play sounds"
    rospy.spin()

if __name__ == "__main__":
    replay_server()
