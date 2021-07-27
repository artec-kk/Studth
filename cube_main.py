# coding:utf-8
from basic_functions import *
from solver_c import solver
from controller import controller, set_status
from detector import detector
from time import sleep, time

import tkinter as tk
import threading

Status = 0  # 0: stop, 1: start
def solve(callback):
    global Status

    pos_wait = True # enable camera check
    stickers = None

    stickers = detector(pos_wait)
    print('sticker:', stickers)

    for i in range(6):
        print(stickers[i * 9:i * 9 + 9])
    try:
        # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F' solved in 55.71 sec
        # L U F' U' F D' R' U' D2 R B2 R D2 F2 L' F2 U2 R D2 U' solved in 51.26 sec
        # L B R2 D2 B R2 D2 B' D2 F L2 F U R' D U2 L D' U2 48.25 sec
        # U B2 L2 U F2 R2 U R2 B2 D' F2 D2 R' D' U2 B' R B2 L2 F U2 38.05 sec
        solution = solver(stickers)
        print(solution)
        strt = time()
        controller(solution)
        print('done in', time() - strt, 'sec')
        callback()
    except:
        print('error')
        callback()


def shuffle(callback):
    global Status

    stickers = None
    print('mode:2')
    w, g, r, b, o, y = range(6)
    # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
    stickers = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w]

    for i in range(6):
        print(stickers[i * 9:i * 9 + 9])
    try:
        # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F' solved in 55.71 sec
        # L U F' U' F D' R' U' D2 R B2 R D2 F2 L' F2 U2 R D2 U' solved in 51.26 sec
        # L B R2 D2 B R2 D2 B' D2 F L2 F U R' D U2 L D' U2 48.25 sec
        # U B2 L2 U F2 R2 U R2 B2 D' F2 D2 R' D' U2 B' R B2 L2 F U2 38.05 sec
        solution = solver(stickers)
        print(solution)
        strt = time()
        controller(solution)
        print('done in', time() - strt, 'sec')
        callback()
    except:
        print('error')
        callback()
