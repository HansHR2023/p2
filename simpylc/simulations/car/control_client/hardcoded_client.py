'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import time as tm
import traceback as tb
import math as mt
import sys as ss
import os
import socket as sc

ss.path +=  [os.path.abspath (relPath) for relPath in  ('..',)] 

import socket_wrapper as sw
import parameters as pm

import torch
from torch import nn
import pickle as pkl


class HardcodedClient:
    def __init__ (self):
        self.steeringAngle = 0
        

        #load and init trained model

        with open (pm.sampleFileName, 'w') as self.sampleFile:
            with sc.socket (*sw.socketType) as self.clientSocket:
                self.clientSocket.connect (sw.address)
                self.socketWrapper = sw.SocketWrapper (self.clientSocket)
                self.halfApertureAngle = False

                while True:
                    self.input ()
                    self.sweep ()
                    self.output ()
                    self.logTraining ()
                    tm.sleep (0.02)

    def input (self):
        sensors = self.socketWrapper.recv ()

        if not self.halfApertureAngle:
            self.halfApertureAngle = sensors ['halfApertureAngle']
            self.sectorAngle = 2 * self.halfApertureAngle / pm.lidarInputDim
            self.halfMiddleApertureAngle = sensors ['halfMiddleApertureAngle']
            
        if 'lidarDistances' in sensors:
            self.lidarDistances = sensors ['lidarDistances']
        else:
            self.sonarDistances = sensors ['sonarDistances']
    
   
    def lidarSweep (self):
        # self.model = torch.load('../../../../notebooks/data/lidar_model_1.pth')
        self.model = torch.load('../../../../notebooks/data/lidar_model_large.pth')
        
        # self.model = pickle.load(open('../../../../notebooks/data/lidar_2.pkl', 'rb'))

        sample = [pm.finity for entryIndex in range (pm.lidarInputDim + 1)]

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle):
            sectorIndex = round (lidarAngle / self.sectorAngle)
            sample [sectorIndex] = min (sample [sectorIndex], self.lidarDistances [lidarAngle])

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)

        lidar_data = sample[:-1]
        input_tensor = torch.Tensor(lidar_data)

        self.steeringAngle = self.model(input_tensor).item()
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle)

    def sonarSweep (self):
        self.model = torch.load('../../../../notebooks/data/sonar_model_weights_2.pth')
        
        sample = [pm.finity for entryIndex in range (pm.sonarInputDim + 1)]

        for entryIndex, sectorIndex in ((2, -1), (0, 0), (1, 1)):
            sample [entryIndex] = self.sonarDistances [sectorIndex]

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)


        sonar_data = sample[:-1]
        input_tensor = torch.Tensor(sonar_data)

        self.steeringAngle = self.model(input_tensor).item() ### LET OP: klopt naam model???
        self.targetVelocity = pm.getTargetVelocity (self.steeringAngle)

    def sweep (self):
        if hasattr (self, 'lidarDistances'):
            self.lidarSweep ()
        else:
            self.sonarSweep ()

    def output (self):
        actuators = {
            'steeringAngle': self.steeringAngle,
            'targetVelocity': self.targetVelocity
        }

        self.socketWrapper.send (actuators)

    def logLidarTraining (self):
        sample = [pm.finity for entryIndex in range (pm.lidarInputDim + 1)]

        for lidarAngle in range (-self.halfApertureAngle, self.halfApertureAngle):
            sectorIndex = round (lidarAngle / self.sectorAngle)
            sample [sectorIndex] = min (sample [sectorIndex], self.lidarDistances [lidarAngle])

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)

    def logSonarTraining (self):
        sample = [pm.finity for entryIndex in range (pm.sonarInputDim + 1)]

        for entryIndex, sectorIndex in ((2, -1), (0, 0), (1, 1)):
            sample [entryIndex] = self.sonarDistances [sectorIndex]

        sample [-1] = self.steeringAngle
        print (*sample, file = self.sampleFile)

    def logTraining (self):
        if hasattr (self, 'lidarDistances'):
            self.logLidarTraining ()
        else:
            self.logSonarTraining ()

HardcodedClient ()
