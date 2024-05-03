import class_viz as cp
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
#prevCircle = None
#dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2
#prev_frame_time = 0
#new_frame_time = 0
############################################################

rbt = cp.VizCoppelia()   #cria comunicacao com o viz

rbt.startMission() #começa a rodar a sim

while rbt.t < 5.0:
	
	# lê sensores
	rbt.step()
	
	# seta direcao
	#rbt.setSteer(0*np.deg2rad(10.0*np.sin(rbt.t)))
	
	#atua
	if rbt.t < 2.0:
		rbt.setU(0.5)
	else:
		rbt.setU(0.0)
		
	# pega imagem
	image = rbt.getImage()

	####################algoritmo de circulo##############################
	#pegar a imagem e identificar o circulo
	#frame = rbt.getImage()
	#trata a imagem de identificar circulo
	#grayFrame = cv2.cv2tColor(frame, cv2.COLOR_BGR2GRAY)
	#blurFrame = cv2.GaussianBlur(grayFrame, (7, 7), 0)
	
	#font = cv2.FONT_HERSHEY_SIMPLEX
	#new_frame_time = time.time()
	#fps = 1/(new_frame_time-prev_frame_time)
	#prev_frame_time = new_frame_time

	#fps = int(fps)
	#fps = str(fps)

	#cv2.putText(frame, fps, (7, 70), font, 3, 3, cv2.LINE_AA)

	#circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.4, 110,
    #                          param1=160,param2=50,minRadius=10, maxRadius=100)
    # param1 = sensibility paramqqqq2 = accurrancy
	#if circles is not None:
	#   circles = np.uint16(np.around(circles))
	#	chosen = None
	#
	#	for i in circles[0, :]:
	#		if chosen is None: chosen = i
	#		if prevCircle is not None:
	#			if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1] <= dist(i[0],i[1],prevCircle[0],prevCircle[1])):
	#				chosen = i

	#	print(fps)
	#	cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,180,180), 3)
	#	cv2.circle(frame,(chosen[0], chosen[1]), chosen[2], (255,0,255),3)
	#	prevCircle = chosen 

    
    #mostra os circulos numa telinha
    #cv2.imshow('circles', blurFrame)
	#cv2.imshow('circles', frame)

	######################################################################

	########################################
	# plota	
	plt.subplot(121)
	#plt.cla()
	plt.gca().imshow(image, origin='lower')
	plt.title('t = %.1f' % rbt.t)
	
	plt.subplot(122)
	#plt.cla()
	t = [traj['t'] for traj in rbt.traj]
	v = [traj['v'] for traj in rbt.traj]
	plt.plot(t,v)
	plt.ylabel('v[m/s]')
	plt.xlabel('t[s]')
	
	plt.pause(0.01)

#plt.savefig('Coast Down Graph.pdf')
plt.show()
rbt.stopMission()
#print(perro)
