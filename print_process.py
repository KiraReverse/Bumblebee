# import ctypes
# import ctypes.wintypes
# from ctypes import WinDLL
# from ctypes import windll, byref, c_ubyte
# from ctypes.wintypes import RECT, HWND
# import pyautogui
# from collections import namedtuple
# import time
# from time import perf_counter
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
import pygetwindow
# import cv2
# # import pytesseract
# # pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"







async def main():
    print("Main function started")
    aa = pygetwindow.getAllTitles()
    for _, a in enumerate(aa):
        print(f'{_}={a}')
    print(f'')
    # print("pygetwindow.getActiveWindow: ", pygetwindow.getActiveWindow())
    print(f'')
    # print("pygetwindow.getActiveWindowTitle: ", pygetwindow.getActiveWindowTitle())
    print(f'')
    # print("pygetwindow.getAllWindows: ", pygetwindow.getAllWindows())
    print(f'')



# Run the event loop
if __name__ == "__main__":    
    asyncio.run(main())