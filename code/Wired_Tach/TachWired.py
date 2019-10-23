import pygame
import serial
import time
import numpy as np

#THIS IS MID-DEVELOPMENT-CYCLE SOFTWARE USED FOR RAPID DEVELOPMENT. FOR ANNOTATIONS AND ORGANIZATION, SEE FINAL PRODUCT SOFTWARE IN THE GIT REPO. 

MEDIA_FOLDER = "media_called_by_python/"	#relative path to folder that contains images

gear_ratios=(0, 189.5,98,65,49.5,39.6,33, 0)
splits=(0, 143.75,81.5,57.25,44.55,36.3)

#try 2 ports
ser = serial.Serial("/dev/ttyACM0")
if not ser.isOpen():
    time.sleep(1)
    ser=serial.Serial("/dev/ttyACM1")

ser.flushInput()


pygame.init()
font = pygame.font.SysFont('kozgopr6nmedium', 69) 


display_width=480
display_height=320

backdrop = pygame.image.load(MEDIA_FOLDER+'all_but_needle.png') 	#background, just a static image
needlebold= pygame.image.load(MEDIA_FOLDER+'needle_outlined.png') 	#needle for tachometer, rotate according to readings


tachDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
#tachDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Saab Tach')

screen_rect = backdrop.get_rect()
rect_for_rotated_bold = needlebold.get_rect(center=screen_rect.center)


black = (0,0,0)
white = (255,255,255)

def check_for_termination():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.sighandle()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                print("pressed CTRL-C as an event")
                self.sighandle()



pygame.mouse.set_visible(0)

def get_tach_value_from_hex_string(data):
    inint=int(data,16)
    number=inint/4

    return number


    
    
def get_angle(rpm):
    
    output = np.maximum(-(rpm*250/7000),-250)
    
    return output

def get_int_from_2_chunks(ch1,ch2):
    if(len(ch2)==1):
        ch2="0"+ch2
    inint=int(ch1+ch2,16)
    return inint

def get_tach_value_from_int(mint):
    return mint/4
    
def get_vehicle_speed_from_ints(arra):
    ave=np.average(arra)
    return ave/50

def gear_detection(rpm, speed):
    if(speed == 0):
        current_gear = -1 #Neutral
    else:
        current_ratio = rpm/(speed+0.01)
        if(current_ratio<splits[3]):
            if(current_ratio>splits[4]):
                current_gear = 4
            else:
                if(current_ratio>splits[5]):
                    current_gear = 5
                else:
                    current_gear = 6
            
            
        else:
            if(current_ratio<splits[2]):
                current_gear = 3
            else:
                if(current_ratio<splits[1]):
                    current_gear=2
                else:
                    current_gear=1
    return current_gear

rpms=np.array([0,0,0,0,0,0])
while(1):

    check_for_termination()
    #screen.fill([255, 255, 255])
    tachDisplay.blit(backdrop, (0, 0))
    ser.flushInput()
    ser.readline()    
    #time.sleep(0.1)
    lineIn=str(ser.readline()) #it is, read the data
    #f.write(lineIn)
    
    spaces=np.zeros(11,np.int)
    spaces[0]=int(lineIn.find(" "))
    for i in range(10):
        print(spaces)
        spaces[i+1]=lineIn.find(" ",spaces[i]+1)


    if((spaces > -1).all()):
        
        chunks=["","","","","","","","","","",""]
        int_data=np.empty(5)
        
        for j in range(10):
            chunks[j]=lineIn[spaces[j]+1:spaces[j+1]]
            

        for j in range(5):
            int_data[j]=get_int_from_2_chunks(chunks[j*2],chunks[j*2+1])


        rpm_measured=get_tach_value_from_int(int_data[0])
        veh_speed_measured=get_vehicle_speed_from_ints(int_data[1:5])
        current_gear=gear_detection(rpm_measured,veh_speed_measured)
                 

        
        angle_for_bold = get_angle(rpm_measured)
        rotated_bold = pygame.transform.rotate(needlebold,angle_for_bold)
        rect_for_rotated_bold = rotated_bold.get_rect(center=rect_for_rotated_bold.center)
        tachDisplay.blit(rotated_bold,rect_for_rotated_bold) 
		
        if(current_gear>0):
            text_to_draw= str(current_gear)
        else:
            text_to_draw="N"
        
        text = font.render(text_to_draw, True, (255,125,0), black)
        textRect = text.get_rect() 
        textRect.center = (420, 69-12)
        tachDisplay.blit(text,textRect)
        
        pygame.display.update()
