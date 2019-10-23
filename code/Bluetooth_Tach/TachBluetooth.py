import pygame
import numpy as np
import hollow
from hollow import textOutline
import obd
import math


MEDIA_FOLDER = "media_called_by_python/"	#relative path to folder that contains images

#empirically determined, (Engine RPM)/(Vehicle speed [mph])
#index 1 is first gear, index 2 is second, etc.
gear_ratios=(0, 189.5,98,65,49.5,39.6,33, 0)
splits=(0, 143.75,81.5,57.25,44.55,36.3) 	#splitting points between gear ratios. Generally, splits(n) = ave(gear_ratios(n),gear_ratios(n+1))


connection = obd.OBD() 	#connect to bluetooth OBDII reader

#the only 2 things we are going to query in this program
cmd_rpm = obd.commands.RPM
cmd_speed = obd.commands.SPEED


pygame.init()		#use pygame for drawing mainly
display_width=480
display_height=320
font = pygame.font.SysFont('kozgopr6nmedium', 69) 					#Font for gear indicator
backdrop = pygame.image.load(MEDIA_FOLDER+'all_but_needle.png') 	#background, just a static image
needle_img= pygame.image.load(MEDIA_FOLDER+'needle_outlined.png') 	#needle for tachometer, rotate according to readings

#Setup the scene parameters. The following line is for fullscreen, use the one after it for a window instead.
tachDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
#tachDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Saab Tach')	#name of window, if fullscreen isn't on.

screen_rect = backdrop.get_rect()
rect_for_rotated_needle = needlehazy.get_rect(center=screen_rect.center)

pygame.mouse.set_visible(0)		#hide cursor

black = (0,0,0)
white = (255,255,255)
text_back_color = black				#square around drawn text, match background or it will look funked up.
text_interior_color = (255,125,0)	#color of inside of drawn letters. 255,125,0 is orange-ish.
text_outline_color = white			#outline of letter. 


def check_for_termination():
	#check to see if user has tried quitting the program

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            self.sighandle()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                print("pressed CTRL-C to quit")
                pygame.display.quit()
                pygame.quit()
                self.sighandle()
    
    
def get_angle(rpm):
    #INPUT: number of rpms
	#OUTPUT: angle to turn needle image in degrees. Formula found using a protractor. 
	
    output = np.maximum(-(rpm*250/7000),-250)
    
    return output



def gear_detection(rpm, speed):
	#INPUT: number of rpms, vehicle speed in rpm
	#OUTPUT: estimated gear. 
	# Indicates neutral (-1) when vehicle is at standstill, otherwise a gear 1-6.
	
	
    if(speed == 0):
        current_gear = -1 #Neutral
    else:
        current_ratio = rpm/(speed+0.01) #avoid divide by zero
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



speed_read_counter=0	#counter that helps space out speed readings
bad_message_count=0		#count of bad messages since last reset

while(1):	#loop that gets readings and updates displayed image

    check_for_termination()    
    
	# send command, and parse the response
    rpm_raw = connection.query(cmd_rpm).value 
    if(rpm_raw==None):
        rpm_raw=0
        bad_message_count=bad_message_count+1
    else:
        rpm_raw=rpm_raw.magnitude

	#query rpm more often because we would like a smooth rpm at the expense of gear detection
    #each query takes 0.04 seconds, so only update speed every 3 times (0.16 s for full cycle of 3 rpm reads and 1 speed read)
    if((speed_read_counter%3)==0):
        speed_raw = connection.query(cmd_speed).value 
        if(speed_raw==None):
            speed_raw=0
        else:
            speed_raw=speed_raw.to("mph").magnitude
	
	#update counter that helps space out speed readings.
    speed_read_counter=speed_read_counter+1

 

    rpm_measured = rpm_raw
    veh_speed_measured = speed_raw
    current_gear=gear_detection(rpm_measured,veh_speed_measured)
        
	#draw the background, empty gauge with no needle
    tachDisplay.blit(backdrop, (0, 0))           
        
	#figure out how much to rotate needle, rotate it, and draw it.
    angle_for_needle = get_angle(rpm_measured)
    rotated_needle = pygame.transform.rotate(needle_img,angle_for_needle)
    rect_for_rotated_needle = rotated_needle.get_rect(center=rect_for_rotated_needle.center)
    tachDisplay.blit(rotated_needle,rect_for_rotated_needle)   
		
	#these 4 lines convert the gear to text to be drawn.	
    if(current_gear>0):
        text_to_draw= str(current_gear)
    else:
        text_to_draw="N"
        
	#these 5 lines draw the gear indicator
    outlined_letter = textOutline(font, text_to_draw, text_interior_color, text_outline_color)
    text_to_get_box = font.render(text_to_draw, True, text_interior_color, text_back_color)
    textRect = text_to_get_box.get_rect() 
    textRect.center = (440, 34) 
    tachDisplay.blit(outlined_letter,textRect)   

    pygame.display.update()		#update drawing

	#clear buffers, and if too many bad rpm readings received reset obd connection
    pygame.event.pump()
    if(bad_message_count>30):
        connection.close()
        connection = obd.OBD()
        bad_message_count=0

