#!/usr/bin/env python
#coding=utf-8
import rospy
import pyaudio
import wave
from roboy_cognition_msgs.srv import PlaySound
from roboy_cognition_msgs.msg import SpeechSynthesis
from roboy_control_msgs.msg import Emotion

def play(req):
    elapsed_time = 0
    timestamps = list(req.timestamps)
    emotions = list(req.emotions)

    if len(timestamps) != len(emotions):
        rospy.logerr("Mismatch of emotions and timestamp array sizes")
        return False

    emotion_pub = rospy.Publisher('/roboy/cognition/face/emotion', Emotion, queue_size=1)
    speech_pub = rospy.Publisher('/roboy/cognition/speech/synthesis', SpeechSynthesis, queue_size=1)
    speech_pub.publish(phoneme='sil')

    chunk = 1024
    sample_rate = 22050
    seconds_per_buffer = float(chunk) / sample_rate

    f = wave.open(req.filepath,"rb")
    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(f.getsampwidth()), \
                    channels = f.getnchannels(), \
                    rate = f.getframerate(), \
                    output = True)

    data = f.readframes(chunk)
    msg = SpeechSynthesis()
    while data:
        for s, e in zip(timestamps, emotions):
            if abs(s-elapsed_time) <= seconds_per_buffer:
                emotion_pub.publish(emotion=e)
                print(e)
                timestamps.remove(s)
                emotions.remove(e)
        msg = SpeechSynthesis()
        msg.phoneme  = 'o'
        speech_pub.publish(msg)
        stream.write(data)
        data = f.readframes(chunk)
        elapsed_time +=seconds_per_buffer
    msg.phoneme = 'sil'
    speech_pub.publish(msg)
    stream.stop_stream()
    stream.close()

    p.terminate()

    return True


def replay_server():
    rospy.init_node('sound_play_server')
    rospy.Service('/roboy/matrix/sound/play', PlaySound, play)
    print "Ready to play sounds"
    rospy.spin()

if __name__ == "__main__":
    replay_server()
