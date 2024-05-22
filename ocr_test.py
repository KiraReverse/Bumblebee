

import ctypes
import ctypes.wintypes
from ctypes import WinDLL
from ctypes import windll, byref, c_ubyte
# from ctypes.wintypes import RECT, HWND
# import pyautogui
# from collections import namedtuple
import time
from time import perf_counter
# import unittest
# # from initinterception import sleep
import asyncio
# import win32gui
# from pytweening import easeInPoly, easeOutPoly, easeInOutPoly
# from humancursor import SystemCursor
# from helper import Helper
# from configparser import ConfigParser
# import tkinter as tk
# import customtkinter
# import threading
# from PIL import Image, ImageTk
# from datetime import datetime
# from datetime import time as dtime    
# import os
# import gc
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from game import Game
# from runesolver import RuneSolver
# from action import Action
# from initinterception import keydown, keyup, keyupall, sleep, sleeplol
# from mss import mss as mss_module
# # from mss.windows import MSS as mss
# import mss
# import mss.tools
# import numpy as np
# from multiprocessing import JoinableQueue
# from multiprocessing import Process
# import keyboard as pythonkeyboard
# from pynput.mouse import Listener, Button
# from pynput import keyboard
# import pygetwindow
import cv2
import easyocr
from matplotlib import pyplot as plt
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



# These ctypes structures are for Win32 INPUT, MOUSEINPUT, KEYBDINPUT, and HARDWAREINPUT structures,
# used by SendInput and documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646270(v=vs.85).aspx
# Thanks to BSH for this StackOverflow answer: https://stackoverflow.com/questions/18566289/how-would-you-recreate-this-windows-api-structure-with-ctypes
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.wintypes.LONG),
        ('dy', ctypes.wintypes.LONG),
        ('mouseData', ctypes.wintypes.DWORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', ctypes.wintypes.WORD),
        ('wScan', ctypes.wintypes.WORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', ctypes.wintypes.DWORD),
        ('wParamL', ctypes.wintypes.WORD),
        ('wParamH', ctypes.wintypes.DWORD)
    ]

class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [
            ('mi', MOUSEINPUT),
            ('ki', KEYBDINPUT),
            ('hi', HARDWAREINPUT),
        ]

    _anonymous_ = ('i', )
    _fields_ = [
        ('type', ctypes.wintypes.DWORD),
        ('i', _I),
    ]
    
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC















async def main():
    print("Main function started")


    # ## https://www.youtube.com/watch?v=HHHkh9IOqhI
    # # tessdata_dir_config = r'--tessdata-dir "C:\\Program Files\\Tesseract-OCR"'
    # # g = Game((8, 63, 200, 150)) #
    # # img = g.get_screenshot()
    # # img = cv2.imread("score.png")
    # # img = cv2.imread("../image/34.png")    
    # # img = cv2.imread("../image/pytesseract.png")    
    # # img = cv2.imread("../image/2/4275__.png")    
    # # img = cv2.imread("../image/3/49.png")    
    # img = cv2.imread("../image/liedetector.png")
    # # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower_background = np.array([35, 40, 40])
    # upper_background = np.array([85, 255, 255])
    # background_mask = cv2.inRange(hsv_image, lower_background, upper_background)
    # foreground_mask = cv2.bitwise_not(background_mask)
    # kernel = np.ones((3, 3), np.uint8)
    # cleaned_foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    # cleaned_foreground_mask = cv2.morphologyEx(cleaned_foreground_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    # img = cv2.bitwise_and(img, img, mask=cleaned_foreground_mask)
    # # _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)    
    # # img = cv2.bitwise_not(img)
    # print(f'{type(img)=}')
    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # while True:
    #     try:
    #         now=perf_counter()
    #         # imgstring = pytesseract.image_to_string(img, lang='eng')
    #         # imgstring = pytesseract.image_to_string(img, config='--psm 6 --tessdata-dir \"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"')
    #         # imgstring = pytesseract.image_to_string(img, config='--psm 6')
    #         imgstring = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
    #         # imgstring = pytesseract.image_to_string(img, config='--psm 6 digits')
    #         # imgstring = pytesseract.image_to_string(img, config='--psm 6 --oem 3 digits')
    #         print(f"PYTESSERACT!!!!!!!!! = {imgstring} {perf_counter()-now:.10f}")
    #         # g.read_score()
    #         time.sleep(.5)
    #     except Exception as e:
    #         print(f'pytesseract e: {e=}')

    ## EasyOCR ## https://www.youtube.com/watch?v=ZVKaWPW9oQY
    # g = Game((8, 63, 200, 150)) #
    # img = g.get_screenshot()
    imagepath='../image/captcha.png'
    # img = cv2.imread("score.png")
    # img = cv2.imread("../image/pytesseract.png")    
    # img = cv2.imread("../image/2/4275__.png")    
    # img = cv2.imread("../image/3/49.png")    
    # img = cv2.imread("../image/liedetector.png")
    # img = cv2.imread("../image/34.png")    
    img = cv2.imread(imagepath)    
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower_background = np.array([35, 40, 40])
    # upper_background = np.array([85, 255, 255])
    # background_mask = cv2.inRange(hsv_image, lower_background, upper_background)
    # foreground_mask = cv2.bitwise_not(background_mask)
    # kernel = np.ones((3, 3), np.uint8)
    # cleaned_foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    # cleaned_foreground_mask = cv2.morphologyEx(cleaned_foreground_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    # img = cv2.bitwise_and(img, img, mask=cleaned_foreground_mask)
    # _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)    
    # img = cv2.bitwise_not(img)
    print(f'{type(img)=}')
    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # if True:
    reader = easyocr.Reader(['en'], gpu=True)
    for i in range(1):
    # while True:
        try:
            now=perf_counter()
            result = reader.readtext(imagepath)
            print(f"{perf_counter()-now:.10f}")
            for r in result:
                print(f'{r=} {r[0]=} {r[0][0]=}')
                top_left=tuple([int(r[0][0][0]),int(r[0][0][1])])
                btm_right=tuple([int(r[0][2][0]),int(r[0][2][1])])
                text=r[1]
                img = cv2.rectangle(img, top_left, btm_right, (0,255,0), 5)
                img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2, cv2.LINE_AA)
            plt.imshow(img)
            plt.show()
            time.sleep(.5)
        except Exception as e:
            print(f'e: {e=}')





# Run the event loop
if __name__ == "__main__":    
    asyncio.run(main())