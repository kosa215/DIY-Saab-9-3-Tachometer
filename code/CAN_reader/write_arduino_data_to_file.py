import serial
import time
ser = serial.Serial("/dev/ttyACM0")
ser.flushInput()
b=open("canlog.txt","w")
timeinitial=time.time()
while True:
    #print(time.time()-timeinitial)
    timedel=time.time()-timeinitial
    if(timedel>600):
        break
    lineIn = ser.readline()
    b.write(str(timedel)+"  "+str(lineIn)+"\n")


    #print(lineIn)
b.close()
print("DONE")