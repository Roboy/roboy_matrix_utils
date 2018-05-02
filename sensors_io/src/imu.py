import iio
import pdb
import math
import time
import rospkg
import sys

rospack = rospkg.RosPack()
sys.path.append(rospack.get_path('led_control')+'/src')
from leds import MatrixLeds

leds = MatrixLeds()
contexts = iio.scan_contexts()
uri = next(iter(contexts), None)
ctx = iio.Context(uri)
for dev in ctx.devices:
	for chn in dev.channels:
		print('\t\t\t%s: %s (%s)' % (chn.id, chn.name or "", 'output' if chn.output else 'input'))

		if len(chn.attrs) != 0:
			print('\t\t\t%u channel-specific attributes found:' % len(chn.attrs))

		for attr in chn.attrs:
			try:
				print('\t\t\t\t' + attr + ', value: ' + chn.attrs[attr].value)
			except OSError as e:
				print('Unable to read ' + attr + ': ' + e.strerror)

imu = ctx.devices[0]
while True:
	time.sleep(0.5)

	accelX = float((c for c in imu.channels if c.id == "accel_x").next().attrs['raw'].value)
	accelY = float((c for c in imu.channels if c.id == "accel_y").next().attrs['raw'].value)
	accelZ = float((c for c in imu.channels if c.id == "accel_z").next().attrs['raw'].value)

	gyroX = float((c for c in imu.channels if c.id == "anglvel_x").next().attrs['raw'].value)/57.3
	gyroY = float((c for c in imu.channels if c.id == "anglvel_y").next().attrs['raw'].value)/57.3
	gyroZ = float((c for c in imu.channels if c.id == "anglvel_z").next().attrs['raw'].value)/57.3

	magX = float((c for c in imu.channels if c.id == "magn_x").next().attrs['raw'].value)
	magY = float((c for c in imu.channels if c.id == "magn_y").next().attrs['raw'].value)
	magZ = float((c for c in imu.channels if c.id == "magn_z").next().attrs['raw'].value)

	pitch = math.atan2 (accelY ,( math.sqrt ((accelX * accelX) + (accelZ * accelZ))))
	roll = math.atan2(-accelX ,( math.sqrt((accelY * accelY) + (accelZ * accelZ))))


	Yh = (magY * math.cos(roll)) - (magZ * math.sin(roll))
	Xh = (magX * math.cos(pitch))+(magY * math.sin(roll)*math.sin(pitch)) + (magZ * math.cos(roll) * math.sin(pitch))

	yaw =  math.atan2(Yh, Xh)


	roll = roll*57.3
	pitch = pitch*57.3
	yaw = yaw*57.3
	
	led_id = int((roll+pitch)%leds.leds_num)
	color = [0,0,0,0]
	img = leds.leds_num * color
	
        ids = range(led_id-3, led_id+3)
        for id in ids:
            if (id>leds.leds_num-1):
                _id = id-leds.leds_num-1
            elif (id<0):
                _id = leds.leds_num + id
            else:
                _id = id
            img[_id*4] = 1
            img[_id*4+3] = 25
	leds.write_pixels(img)

	#print "roll: ", roll, "\t\tpitch: ", pitch, "\t\tyaw: ", yaw
