# coding:utf-8
from basic_functions import *
import serial
from time import time, sleep

Status = 0

def grab(num):
    s = str(num) + ' ' + '1000'
    ser_motor.write((s + '\n').encode())

def release(num):
    s = str(num) + ' ' + '2000'
    ser_motor.write((s + '\n').encode())

def release_big(num):
    s = str(num) + ' ' + '3000'
    ser_motor.write((s + '\n').encode())

def chon(num):
    s = str(num) + ' ' + '4000'
    ser_motor.write((s + '\n').encode())

def send_command(cmd):
    s = ' '.join(str(i) for i in cmd)
    ser_motor.write((s + '\n').encode())

def set_status(st):
    global Status
    Status = st

def controller(solution):
    global Status
    for twist in solution:
        print('satus:{0}'.format(Status))
        if Status == 0:
            break

        for i in range(4):
            grab(i)
        sleep(0.1)
        #print(twist, twists_key[twist])
        for action in twists_key[twist]:
            for each_action in action:
                send_command(each_action)
            if action[0][1] == 4000:
                sleep(0.25)
            elif action[0][1] >= 1000:
                sleep(0.15)
            else:
                sleep(0.3)
        # for i in range(4):
        #     chon(i)
        #sleep(1)

ser_motor = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
sleep(2)
