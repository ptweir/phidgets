#!/usr/bin/env python

"""Copyright 2008 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/

modified by Peter Weir, Caltech Jan. 2010
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.6'
__date__ = 'Dec 18 2009'

#Basic imports
from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, PositionChangeEventArgs
from Phidgets.Devices.Servo import Servo, ServoTypes

#measured high stopped pulse width = 1522
#measured low stopped pulse width = 1499
#median stopped pulse width = 1511

stopPW = 1511
goPW = 130


#Create an servo object
try:
    servo = Servo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (servo.isAttached(), servo.getDeviceType(), servo.getSerialNum(), servo.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of motors: %i" % (servo.getMotorCount()))

#Event Handler Callback Functions
def ServoAttached(e):
    attached = e.device
    print("Servo %i Attached!" % (attached.getSerialNum()))

def ServoDetached(e):
    detached = e.device
    print("Servo %i Detached!" % (detached.getSerialNum()))

def ServoError(e):
    source = e.device
    print("Servo %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))

def ServoPositionChanged(e):
    source = e.device
    print("Servo %i: Motor %i Current Pulse Width (velocity command): %f" % (source.getSerialNum(), e.index, e.position))

#Main Program Code
try:
    servo.setOnAttachHandler(ServoAttached)
    servo.setOnDetachHandler(ServoDetached)
    servo.setOnErrorhandler(ServoError)
    servo.setOnPositionChangeHandler(ServoPositionChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    servo.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    servo.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        servo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    DisplayDeviceInfo()

try:
    print("Setting the servo type for motor 0 to RAW_us_MODE")
    servo.setServoType(0, ServoTypes.PHIDGET_SERVO_RAW_us_MODE)

    print("Move in positive direction")
    servo.setPosition(0, stopPW + goPW)
    sleep(5)
    
    print("Move in negative direction")
    servo.setPosition(0, stopPW - goPW)
    sleep(5)
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Enter to stop and quit....")

chr = sys.stdin.read(1)

try:
    print("stopping...")
    servo.setPosition(0, stopPW)
    sleep(1)
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Closing...")

try:
    servo.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
