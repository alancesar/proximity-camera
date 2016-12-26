#!/usr/bin/env python
# -*- coding: utf-8 -*-

'Take a shot by when serial ports sends "1" and upload the image to FTP server'
from ftplib import FTP
import sys
import time
import os
import serial
import picamera

def upload_file(filename):
    'Sends a file to FTP server'
    ftp = FTP(FTP_ADDRESS)
    ftp.login('ftp', 'ftp')
    ftp.cwd('public')
    ftp.cwd('photos')
    ftp.storbinary('STOR ' + filename, open(filename, 'r+'))
    ftp.quit()

def take_shot(camera):
    'Take a shot using Rasberry Pi Camera'
    filename = str(int(round(time.time() * 1000))) + '.jpg'
    camera.capture(filename)
    return filename

def process(filename):
    'Sends the image to FTP server and remove the local file'
    upload_file(filename)
    os.remove(filename)

def read_serial(ser):
    'Read the serial data and convert to a "int" value'
    while ser.inWaiting:
        return int(ser.readline())

PORT = sys.argv[1]
SERIAL = serial.Serial(PORT, 9600)
SERIAL.write('1')
FTP_ADDRESS = sys.argv[2]
CAMERA = picamera.PiCamera()
CAMERA.resolution = (1024, 768)

while True:
    if read_serial(SERIAL) == 1:
        process(take_shot(CAMERA))
    time.sleep(0.5)
