import class_viz2 as cp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys 
import time

original_stdout = sys.stdout

plt.figure(1)
plt.ion()

############################################################
#Para o algoritmo pra identificar circulo
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2
prev_frame_time = 0
new_frame_time = 0
############################################################

rbt = cp.VizCoppelia2()   #cria comunicacao com o viz

rbt.startMission() #começa a rodar a sim

#-----------------valores de constantes do pid---------------
Kp = 2.5
Kd = 0.5
Ki = 0.05
#------------------------------------------------------------

rbt_ref = 15.0 #referencial de velocidade
perror = 0 #erro prévio
global integral, prop, derivative, p_error #variaveis utilizadas
integral = 0 
derivative = 0

#------------------------------------------------------------

e = []
error = 0

def calculate_pid():
    return ((Kp * prop) + (integral) + (derivative)) #calculo do pid

#------------------------------------------------------------

while rbt.t < 6:
    rbt.step()

	####################algoritmo de circulo##############################
	#pegar a imagem e identificar o circulo
    frame = rbt.getImage()
	#trata a imagem de identificar circulo
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (7, 7), 0)
	
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = int(fps)
    fps = str(fps)

	#cv2.putText(frame, fps, (200, 200), font, 1,(0,0,255), 3, cv2.LINE_AA)

    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.4, 110,
                              param1=160,param2=50,minRadius=10, maxRadius=100)
    # param1 = sensibility paramqqqq2 = accurrancy
    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1] <= dist(i[0],i[1],prevCircle[0],prevCircle[1])):
                    chosen = i

		#print(fps)
        ###################calculos de erro, pid e motores##############
        error = 130 - chosen[0]
        error = np.clip(error, -130,130)
        #k = 0
        #e.insert(k,float(error))
        #k = k + 1
        print(error) #distancia em x do centro pra linha do robo
        ################################################################

        ############coloca o circulo####################################
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,180,180), 3)
        cv2.circle(frame,(chosen[0], chosen[1]), chosen[2], (255,0,255),3)
        frame = cv2.line(frame, (chosen[0],chosen[1]), (130,chosen[1]), (255,0,0), 1)
        prevCircle = chosen 
        ################################################################

    ##########atuadores dos motores#############
    lm = rbt.motorl
    rm = rbt.motorr
        #rbt.motorvel(lm,1)
        #rbt.motorvel(rm,1)
    if (error != 0):
        prop = error
        integral = (integral + Ki*error*0.05)
        derivative = Kd*(error - perror)/0.05
        perror = error
    if (error < -5):
        rbt.motorvel(lm, rbt_ref + abs(calculate_pid())/20)
        rbt.motorvel(rm,rbt_ref) #- abs(calculate_pid())/50.0)
    elif(error > 5):
        rbt.motorvel(rm, rbt_ref + abs(calculate_pid())/20)
        rbt.motorvel(lm,rbt_ref) #- abs(calculate_pid())/50.0)
    elif (error > -5 or error < 5):
        rbt.motorvel(rm,rbt_ref)
        rbt.motorvel(lm,rbt_ref)
    ############################################

    frame = cv2.line(frame, (130,0), (130,250),(255,0,0), 1)

    #cv.imshow('circles', blurFrame)
	#cv2.imshow('circles', frame)
	######################################################################
    
    #################plota camera###############
    
    plt.subplot(121)
    plt.gca().imshow(frame, origin='lower')
    plt.title('t = %.1f' % rbt.t)

    #plt.subplot(122)
    #plt.cla()
    #t = [traj['t'] for traj in rbt.traj]
    
    #plt.plot(t,e)
    #plt.xlabel('t[s]')
    #plt.ylabel('e')

    plt.pause(0.01)
    ############################################
plt.show()
rbt.stopMission()
