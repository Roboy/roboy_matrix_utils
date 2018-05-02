import time
import math
import datetime
import os
import iio
import sys
import rospkg
rospack = rospkg.RosPack()
sys.path.append(rospack.get_path('led_control')+'/src')
from leds import MatrixLeds



RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0


contexts = iio.scan_contexts()
uri = next(iter(contexts), None)
ctx = iio.Context(uri)

leds = MatrixLeds()
imu = ctx.devices[0]

a = datetime.datetime.now()

while True:
	
	
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = float((c for c in imu.channels if c.id == "accel_x").next().attrs['raw'].value)
    ACCy =  float((c for c in imu.channels if c.id == "accel_y").next().attrs['raw'].value)
    ACCz = float((c for c in imu.channels if c.id == "accel_z").next().attrs['raw'].value)
    GYRx = float((c for c in imu.channels if c.id == "anglvel_x").next().attrs['raw'].value)
    GYRy = float((c for c in imu.channels if c.id == "anglvel_y").next().attrs['raw'].value)
    GYRz = float((c for c in imu.channels if c.id == "anglvel_z").next().attrs['raw'].value)
    MAGx = float((c for c in imu.channels if c.id == "magn_x").next().attrs['raw'].value)
    MAGy = float((c for c in imu.channels if c.id == "magn_y").next().attrs['raw'].value)
    MAGz = float((c for c in imu.channels if c.id == "magn_z").next().attrs['raw'].value)


    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    print "Loop Time | %5.2f|" % ( LP ),


    #Convert Gyro raw to degrees per second
    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN


    #Calculate the angles from the gyro. 
    gyroXangle+=rate_gyr_x*LP
    gyroYangle+=rate_gyr_y*LP
    gyroZangle+=rate_gyr_z*LP


    #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG


    #convert the values to -180 and +180
    AccXangle -= 180.0
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0



    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
    CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



    #Calculate heading
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI

    #Only have our heading between 0 and 360
    if heading < 0:
        heading += 360


    #Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


    #Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))


    #Calculate the new tilt compensated values
    magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360
    
    led_id = int((CFangleX+CFangleY)%leds.leds_num)
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


    if 1:			#Change to '0' to stop showing the angles from the accelerometer
        print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  " % (AccXangle, AccYangle)),

    if 1:			#Change to '0' to stop  showing the angles from the gyro
        print ("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f" % (gyroXangle,gyroYangle,gyroZangle)),

    if 1:			#Change to '0' to stop  showing the angles from the complementary filter
        print ("\033[1;35;40m   \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m" % (CFangleX,CFangleY)),
        
    if 1:			#Change to '0' to stop  showing the heading
        print ("HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f" % (heading,tiltCompensatedHeading))
        




    #slow program down a bit, makes the output more readable
    time.sleep(0.03)
