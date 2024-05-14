import sys
sys.path.append("coppeliasim_zmqremoteapi/")
from coppeliasim_zmqremoteapi_client import *
import numpy as np
import time


class VizCoppelia2:
    def __init__(self):
        
        self.t = 0.0

        self.vlm = 0.0
        self.vrm = 0.0

        self.dt = 0.0

        self.initCoppeliaSim()

    def initCoppeliaSim(self):
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')
        self.sim.stopSimulation()

        self.robot = self.sim.getObject('./base1')
        if self.robot == -1:
            print ('Remote API function call returned with error code (robot): ', -1)

        self.motorl = self.sim.getObject('./left_back_motor')
        if self.motorl == -1:
            print ('Remote API function call returned with error code (motorL): ', -1)
			
        self.motorr = self.sim.getObject('/right_back_motor')
        if self.motorr == -1:
            print ('Remote API function call returned with error code (motorR): ', -1)
		
        self.cam = self.sim.getObject('/Vision_sensor')
        if self.cam == -1:
            print ('Remote API function call returned with error code: ', -1)
			
        print('ready!')

    def getStates(self):
        self.t = self.getTime() - self.tinit

        return self.t
	
    def startMission(self):
        self.sim.startSimulation()

        self.client.setStepping(True)

        self.tinit = self.getTime()

        self.getStates()
        #self.setU(0.0)

        self.saveTraj()
        
    def stopMission(self):
        self.sim.stopSimulation()
        
    def step(self):
        self.client.step()

        t0 = self.t

        self.getStates()

        self.dt = self.t - t0

        self.saveTraj()
    
    def saveTraj(self):
		
		# dados
        data = {	't'     : self.t, 
					'vr'    : self.vrm,
                    'vl'    : self.vlm,
                    }
				
		# se ja iniciou as trajetorias
        try:
            self.traj.append(data)
		# se for a primeira vez
        except:
            self.traj = [data]

    def getTime(self):
        while True:
            t = self.sim.getSimulationTime()
            if (t != -1.0):
                return t

    def motorvel(self,motor,targetvel):
        self.sim.setJointTargetVelocity(motor,targetvel)       
    
    def setPanTilt(self, pan=np.deg2rad(0.0), tilt=np.deg2rad(-35.0)):
        return
	    

    def getImage(self):
        while True:
            image, resolution = self.sim.getVisionSensorImg(self.cam)
            if image != -1:
                break
		# trata imagem		
        img = np.frombuffer(image, dtype=np.uint8)
        img.resize([resolution[1], resolution[0],3])
        return img
		
	########################################
	# termina a classe
    def __del__(self):
		# fecha simulador
        self.stopMission()
		
        print ('Program finished!')
			
	########################################
	# termina a classe
    def __exit__(self):
        for _ in range(2):
            time.sleep(.1)
            self.stopMission()
        self.__del__()

				
    
	    
