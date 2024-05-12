import win32gui
import requests
import json
import os
import random
import cv2
import time
from math import log10, floor
from time import perf_counter
import numpy as np
import threading
import pygetwindow
import keyboard as pythonkeyboard
from pynput import keyboard, mouse
from pynput.keyboard import Listener as KeyListener  # type: ignore[import]
from pynput.mouse import Listener as MouseListener  # type: ignore[import]
from PIL import ImageGrab
from datetime import datetime
from game import Game
import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import *
import customtkinter
import gdi_capture
from PIL import Image, ImageTk
from configparser import ConfigParser
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from attack import leftp, leftr, rightp, rightr, sleep, npcp, npcr
from action import Action
from runesolver import RuneSolver
from initinterception import  move_relative, left_click, right_click, initiate_move, auto_capture_devices2, keydown, keyup, keyupall
from helper import Helper
from character import Character

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')


class TkinterBot(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.config2 = ConfigParser()
        self.config2.read('secret/secret.ini')
        self.minimapX = int(self.config.get('main', 'minimapX'))
        self.minimapY = int(self.config.get('main', 'minimapY'))
        self.initial_line_position = float(self.config.get('main', 'initial_line_position'))
        self.initial_line_position2 = float(self.config.get('main', 'initial_line_position2'))
        self.initial_line_position3 = float(self.config.get('main', 'initial_line_position3'))
        self.initial_line_position4 = float(self.config.get('main', 'initial_line_position4'))
        self.ipaddress = self.config.get('main', 'ipaddress')
        self.g = Game((8, 63, self.minimapX, self.minimapY)) 
        self.TOKEN = self.config2.get('telegram', 'TOKEN')
        self.chat_id = self.config2.get('telegram', 'chat_id')
        self.att = self.config.get('keybind', 'attack')
        self.jump = self.config.get('keybind', 'jump')
        self.teleport = self.config.get('keybind', 'teleport')
        self.ropeconnect = self.config.get('keybind', 'ropeconnect')
        self.npc = self.config.get('keybind', 'npc')
        self.fountainkey = self.config.get('keybind', 'fountainkey')
        self.classtype = self.config.get('keybind', 'classtype')
        self.profile = self.config.get('main', 'profile')
        self.preset = self.config.get('main', 'preset')
        self.script = self.config.get('main', 'script')
        self.rotation = self.config.get('main', 'rotation')
        self.portaldisabled = self.config.getboolean('main', 'portaldisabled')
        self.broiddisabled = self.config.getboolean('main', 'broiddisabled')
        self.runecd = int(self.config.get('main', 'runecd'))

        self.runesolver = RuneSolver()
        self.ac=None
        self.helper = Helper()
        self.character = Character()

        self.application = None
        self.threads = []
        self.stop_event = threading.Event()
        self.pause = True
        self.telegram_keep_alive = True
        self.acc_not_bind = False
        self.telegram_started = False
        self.tkinter_started = False
        self.position10 = (480, 370, 481, 371)
        self.position9 = (445, 405, 446, 406)
        self.position8 = (430, 375, 431, 376)
        self.position7 = (25, 10, 26, 11) #
        self.position6 = (390, 400, 441, 401) #broid 
        # self.position6 = (440, 400, 441, 401) #no-broid
        self.position5 = (300, 360, 301, 361)
        self.position4 = (11, 88, 200, 200)
        self.position44 = (11, 88, 200, 200)
        self.position33 = (315, 40, 316, 41) #
        self.position3 = (405, 75, 406, 76)  # 
        self.position2 = (701, 472, 702, 473)  # 
        self.polochecker = False
        self.portaldialogueX = 222
        self.portaldialogueY = 410
        self.wolfdialogueY = 435
        self.chathwnd=None
        self.maplehwnd=None
        self.whitedotoccur=False
        self.gotoportal=True
        self.pausepolochecker=False
        self.replaceropeconnect=False        
        self.triggermousetest=False
        self.rockduck=False
        self.rockduck2=False
        self.init_maple_windows()
        self.template = cv2.imread('sealed_rune.png', cv2.IMREAD_GRAYSCALE)
        
        self.loop1 = asyncio.new_event_loop()
        self.loop2 = asyncio.new_event_loop()
        self.loop3 = asyncio.new_event_loop()
        self.loop4 = asyncio.new_event_loop()
        self.loop5 = asyncio.new_event_loop()
        self.loop6 = asyncio.new_event_loop()
        self.loop7 = asyncio.new_event_loop()
        self.loop8 = asyncio.new_event_loop()
        self.loop9 = asyncio.new_event_loop()
        self.loop10 = asyncio.new_event_loop()
        self.thread1 = threading.Thread(target=self.run_thread1)
        self.thread3 = threading.Thread(target=self.run_thread3)
        self.thread6 = threading.Thread(target=self.run_thread6)

    def init_tkinter(self):
        self.title("chrome")
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        window_width = 600
        window_height = 800
        window_x = self.screen_width - window_width
        window_y = 0
        self.geometry(f"{window_width}x{window_height}+{window_x-10}+{window_y}")
        self.setup_tab()
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()
        self.setup_tab5()
        self.setup_tab6()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.tkinter_started=True

    async def async_function(self):
        try:
            self.application = Application.builder().token(self.TOKEN).build()
            # self.application.add_handler(CommandHandler('start', self.start_command))
            self.application.add_handler(CommandHandler('status', self.status_command))
            # app.add_handler(CommandHandler('help', help_command))
            # app.add_handler(CommandHandler('custom', custom_command))
            # app.add_handler(MessageHandler(filters.TEXT, handle_message))
            self.application.add_error_handler(self.error)
            # async with self.application:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            # self.root.mainloop() # press close and this line over
            # await asyncio.sleep(30)
            self.telegram_started = True
            while self.telegram_keep_alive:
            # for i in range(iterations):
                # print(f"{thread_name} - Iteration i")
                await asyncio.sleep(1)  # Simulating asynchronous work
            # print(f'finished telegram_run1')
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            # print(f'finished telegram_run2')
        except Exception as e:
            print(f'telegram {e=}')
            self.acc_not_bind = True
            self.telegram_started = True
        finally:
            pass

    def run_thread1(self):
        asyncio.set_event_loop(self.loop1)
        self.loop1.run_until_complete(self.async_function()) # telegram thread

    def run_thread3(self):
        asyncio.set_event_loop(self.loop3)
        self.loop3.run_until_complete(self.async_function3()) # main thread

    def run_thread4(self):
        asyncio.set_event_loop(self.loop4)
        self.loop4.run_until_complete(self.async_function4()) # checker thread

    def run_thread5(self):
        asyncio.set_event_loop(self.loop5)
        self.loop5.run_until_complete(self.async_function5()) # gma thread
    
    def run_thread6(self):
        asyncio.set_event_loop(self.loop6)
        self.loop6.run_until_complete(self.async_function6()) # just a button loop
    
    def run_thread7(self):
        asyncio.set_event_loop(self.loop7)
        self.loop7.run_until_complete(self.async_function7()) # script recording
    
    def run_thread8(self):
        asyncio.set_event_loop(self.loop8)
        self.loop8.run_until_complete(self.async_function8()) # script playback

    def run_thread9(self):
        asyncio.set_event_loop(self.loop9)
        self.loop9.run_until_complete(self.async_function9()) # 

    def run_thread10(self):
        asyncio.set_event_loop(self.loop10)
        self.loop10.run_until_complete(self.async_function10()) # auto clicker monster life

    def start_threads(self):
        self.thread1.start()
        self.thread3.start()
        self.thread6.start()

    async def async_function3(self):
        while not self.tkinter_started:
            time.sleep(1.01)
        self.thread4 = threading.Thread(target=self.run_thread4)
        self.thread4.start() # all the detector goes here
        self.thread5 = threading.Thread(target=self.run_thread5)
        self.thread5.start() # gma detector goes here
        self.ac=self.character.ac
        self.polocheckertimer0=0
        self.now=0
        xynotfound=0
        self.cc=False
        # ugly code starts here
        now=perf_counter()
        runetimer0=now
        runetimer=0
        rune=False
        cctimer0=now
        cctimer=0
        cc=False
        self.rune=False
        # ugly code ends here
        await initiate_move()
        while True:
            if pythonkeyboard.is_pressed("esc"):
                self.pause=True
            if self.pause:
                keyupall()
                print(f'script is paused .. click resume to resume. ')
                while self.pause:
                    time.sleep(1)
                    if self.stop_event.is_set():
                        self.thread4.join()
                        self.thread5.join()
                        return
                print(f'script resumed ..')
            #
            time.sleep(.411) # when testing ..
            # time.sleep(.011) # when real botting ..
            # time.sleep(.001) # when idk maybe you gone insane ..
            g_variable = self.g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            if x == None or y == None:
                xynotfound+=1
                if xynotfound > 70:
                    t = time.localtime()
                    currenttime = time.strftime("%H:%M:%S", t)
                    print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                    # self.characternotfound=True # USE THIS TO INFORM TELEGRAM!!!
                    await self.togglepause() # self.pause=True
                print(f'x==None, pass ..')
                time.sleep(.1)
            else: #
                xynotfound=0
                await self.character.perform_next_attack(x,y) 
                # await self.changechannel_zakum()

                now=perf_counter()                
                cctimer=now-cctimer0
                if cctimer>3000: # 60sec * 50min = 3000sec
                    # cc=True
                    keyupall()
                    await self.changechannel()
                    cctimer0=perf_counter() # reset
                    self.cc=False
                if self.cc: # this is for red dot. 
                    keyupall()
                    await self.changechannel_zakum() # we don't go ardent because it has 5 min cd. 
                    self.cc=False
                runetimer=now-runetimer0
                if runetimer > self.runecd:
                    if not await self.FindRuneCDIcon():
                        await self.character.gotorune() # and solve rune.
                    runetimer0=now

    async def FindRuneCDIcon(self): # TODO: the newest screenshot crop it. 
        self.g.generate_newest_screenshot()
        img_gray = cv2.cvtColor(self.g.get_newest_screenshot(), cv2.COLOR_BGR2GRAY)                
        w, h = self.template.shape[::-1]    
        res = cv2.matchTemplate(img_gray,self.template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        # print(f'{type(loc)=} {len(loc)=} {len(loc[0])=} {loc=}')
        # for pt in zip(*loc[::-1]):
            # print(f'{type(pt)=} {pt=}')
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            # cv2.imwrite('../image/res.png',img_rgb)
        if len(loc[0]) > 0: return True
        return False

    async def async_function4(self): # this thread do all pixel detection / checker function. 
        diedcheckercounter=0
        liedetectorcounter=0
        reddotcounter=0
        whitedotcounter=0
        runecdcounter=0
        mapledcedcounter=0
        self.cc=False
        while True:
            while self.pause:
                time.sleep(1)
                if self.stop_event.is_set():
                    return                    
            self.g.generate_newest_screenshot()
            die, red, lie, whi = self.g.run_once_detect_all()

            if die is not None:
                print(f'{die=}')
                diedcheckercounter+=1
                if diedcheckercounter > 2: # usually check 3times to confirm character really died. 
                    diedcheckercounter=0 # reset
                    print(f'character died. attempt to press ok .. ')
                    position = win32gui.GetWindowRect(self.maplehwnd)
                    x, y, w, h = position
                    if self.broiddisabled:
                        await self.helper.move_to_and_click_and_move_away(x+440,y+400); time.sleep(.1) ## TODO: write a list of offset for all reso.
                        await self.togglepause()
                        print(f'no broid. stopping bot. TODO: click map and teleport back and continue botting. ')
                    else:
                        await self.helper.move_to_and_click_and_move_away(x+390,y+400); time.sleep(.1) ## all offsets are of 800x600 reso
            
            if red is not None:
                print(f'{red=}')
                reddotcounter+=1
                if reddotcounter > 1: # usually check twice to confirm really has red dot. you can change to 0 to immediately change channel. 
                    reddotcounter=0 # reset
                    self.cc=True # we can't directly cc in this thread because cc-ing is a long process, it will block other detectors. 
                    print(f'red dot detected. changing channel. {self.cc=}')

            if lie is not None:
                print(f'{lie=}')
                liedetectorcounter+=1
                if liedetectorcounter > 1: # usually check twice
                    liedetectorcounter=0 # reset
                    await self.togglepause()
                    print(f'lie detector detector. stopping everything. [testing] {self.pause=} {self.scriptpausesignal=}')

            if whi: # this is when accidentally pressed up and enter bounty portal and dialogue come out. 
                print(f'{whi}')
                whitedotcounter+=1
                if whitedotcounter > 1: # usually check twice
                    whitedotcounter=0 # reset
                    print(f'accidentally pressed up on bounty portal? clicking end chat. [testing]')
                    position = win32gui.GetWindowRect(self.maplehwnd)
                    x, y, w, h = position
                    await self.helper.move_to_and_click_and_move_away(x+222,y+410); time.sleep(.1)


            # diedcheckerlocations = self.g.died_checker()
            # if diedcheckerlocations is not None:
            #     print(f'{diedcheckerlocations=}')
            #     diedcheckercounter+=1
            #     if diedcheckercounter > 2: # usually check 3times to confirm character really died. 
            #         diedcheckercounter=0 # reset
            #         print(f'character died. attempt to press ok .. ')
            #         position = win32gui.GetWindowRect(self.maplehwnd)
            #         x, y, w, h = position
            #         if self.broiddisabled:
            #             await self.helper.move_to_and_click_and_move_away(x+440,y+400); time.sleep(.1) ## TODO: write a list of offset for all reso.
            #             await self.togglepause()
            #             print(f'no broid. stopping bot. TODO: click map and teleport back and continue botting. ')
            #         else:
            #             await self.helper.move_to_and_click_and_move_away(x+390,y+400); time.sleep(.1) ## all offsets are of 800x600 reso
            # reddotcheckerlocations = self.g.reddot_checker()
            # if reddotcheckerlocations is not None:
            #     print(f'{reddotcheckerlocations=}')
            #     reddotcounter+=1
            #     if reddotcounter > 1: # usually check twice to confirm really has red dot. you can change to 0 to immediately change channel. 
            #         reddotcounter=0
            #         self.cc=True # we can't directly cc in this thread because cc-ing is a long process, it will block other detectors. 
            #         print(f'red dot detected. changing channel. {self.cc=}')
            # liedetectorcheckerlocations = self.g.liedetector_checker()
            # if liedetectorcheckerlocations is not None:
            #     print(f'{liedetectorcheckerlocations=}')
            #     liedetectorcounter+=1
            #     if liedetectorcounter > 1: # usually check twice
            #         liedetectorcounter=0
            #         await self.togglepause()
            #         print(f'lie detector detector. stopping everything. [testing] {self.pause=} {self.scriptpausesignal=}')
            # whitedotcheckerlocations = self.g.white_dot_checker()
            # if whitedotcheckerlocations: # this is when accidentally pressed up and enter bounty portal and dialogue come out. 
            #     print(f'{whitedotcheckerlocations}')
            #     whitedotcounter+=1
            #     if whitedotcounter > 1: # usually check twice
            #         whitedotcounter=0
            #         print(f'accidentally pressed up on bounty portal? clicking end chat. [testing]')
            #         position = win32gui.GetWindowRect(self.maplehwnd)
            #         x, y, w, h = position
            #         await self.helper.move_to_and_click_and_move_away(x+222,y+410); time.sleep(.1)

            # runecdcheckerlocations = self.g.rune_cd_checker()
            # if runecdcheckerlocations is None: # means rune no more cd
            #     print(f'rune cd icon not found. {runecdcounter=}')
            #     runecdcounter+=1
            #     if runecdcounter>1: # even rune cd we checking twice!
            #         runecdcounter=0
            #         self.rune=True
            #         print(f'rune cd is true (go solve rune!) {self.rune=}')
            # else:
            #     self.rune=False

            # mapledcedcheckerlocations = self.g.maple_dced_checker() # this is redundant because the bot will stop anyway. 
            # if mapledcedcheckerlocations:
            #     print(f'maple login screen detected! {mapledcedcounter=}')
            #     mapledcedcounter+=1
            #     if mapledcedcounter>2: # we check 3 times for dc
            #         mapledcedcounter=0
            #         await self.togglepause()
            #         print(f'maple dc-ed detected! (login screen) [testing] {self.pause=} {self.scriptpausesignal=}')
                
            # if not self.pausepolochecker and not self.portaldisabled: # i disable this because most user don't want to enter bounty portal
            #     polocheckerlocations = self.g.polo_checker() # check for portal on minimap
            #     if polocheckerlocations is not None:
            #         print(f'{polocheckerlocations=}')
            #         self.polochecker = True
            #         self.gotoportal=True
            # whitedotlocations = self.g.white_dot_checker() # this is when character botting, pressed up, accidentally entered portal, dialogue come out. 
            # if whitedotlocations is not None:
            #     whitedotcounter+=1
            #     if whitedotcounter>1: # usually check twice to confirm character really entered portal by accident. 
            #         self.whitedotoccur=True
            #         self.polochecker=True
            #         self.gotoportal=False
            # elif whitedotlocations is None:
            #     whitedotcounter=0
            
            time.sleep(4)
            # time.sleep(2)

    async def async_function9(self):
        now=perf_counter()
        thirdtimer0=now
        thirdtimer=now
        self.fourth=False
        third=False
        second=False
        self.rocklockcounter=0
        self.rocklockcounter2=0
        while True:
            while self.pause:
                time.sleep(1)
                if self.stop_event.is_set():
                    return
                self.fourth=third=second=False                
                thirdtimer0=perf_counter()
            if third:
                rockloc = self.g.rock_checker3()
            elif second:
                rockloc = self.g.rock_checker2()
            else:
                rockloc = self.g.rock_checker()
            if rockloc is not None:
                if rockloc[0]:
                    self.rocklockcounter+=1
                    print(f'rockloc {self.rocklockcounter=}')
                    self.rockduck=True
                elif rockloc[1]:
                    self.rocklockcounter2+=1
                    print(f'rockloc2 {self.rocklockcounter2=}')
                    self.rockduck2=True                    
            now=perf_counter()
            if not self.fourth:        
                thirdtimer = now-thirdtimer0                
                if thirdtimer >= 46:
                    self.fourth=True
                elif thirdtimer >= 30:
                    third=True
                    second=False
                elif thirdtimer >= 15:
                    second=True

    async def async_function5(self): # gma_checker
        while True:
            while self.pause:
                time.sleep(1)
                if self.stop_event.is_set():
                    return
            if self.chathwnd:
                gmacheckerlocations = self.seperate_gma_detector()
                if gmacheckerlocations:
                    print(f'got GM')
                else:
                    print(f'no GM')
            else:
                pass

            time.sleep(5)

    async def async_function6(self): # just a button loop
        while True:
            time.sleep(1)
            if self.stop_event.is_set():
                return
            if self.triggermousetest:
                await initiate_move()
                self.triggermousetest=False

    async def async_function7(self): # script recording thread (keyboard listener)
        self.realrecord()

    async def async_function8(self): # script playback thread
        await self.playback()

    async def async_function10(self): # auto clicker monster life
        await self.autoclicker()

    def init_maple_windows(self):
        windows=[]
        winlist=[]
        winlist = pygetwindow.getWindowsWithTitle('MapleStory')
        for w in winlist:
            windows.append(w._hWnd)
        print(f'{winlist=}')
        print(f'{windows=}')
        for windowhwnd in windows:
            position = win32gui.GetWindowRect(windowhwnd)
            x, y, w, h = position
            print(f'{windows=} {w-x=}')
            if w-x == 410:
                self.chathwnd=windowhwnd
            elif w-x == 1936 or w-x == 1382 or w-x == 1296 or w-x == 1040 or w-x == 816:
                self.maplehwnd=windowhwnd
                self.runesolver.set_maplehwnd(self.maplehwnd)
            elif w-x == 1938 or w-x == 1384 or w-x == 1298 or w-x == 1042 or w-x == 818: # some windows 10
            # elif w-x == 1944 or w-x == 1390 or w-x == 1298 or w-x == 1042 or w-x == 818: # japanese maplestory JMS
                self.maplehwnd=windowhwnd
                self.runesolver.set_maplehwnd(self.maplehwnd)
            elif w-x == 1388 or w-x == 1300 or w-x == 824 or w-x == 1374 or w-x == 2592: # extra testing from users
                self.maplehwnd=windowhwnd
                self.runesolver.set_maplehwnd(self.maplehwnd)

    def init_maple_windows_old(self):
        hwnd = 0
        windows=[]
        while True:
            hwnd = win32gui.FindWindowEx(0,hwnd,None, "MapleStory")
            if hwnd == 0:
                break
            windows.append(hwnd)
        for windowhwnd in windows:
            position = win32gui.GetWindowRect(windowhwnd)
            x, y, w, h = position
            if w-x == 410:
                self.chathwnd=windowhwnd
            else:
                self.maplehwnd=windowhwnd
                self.runesolver.set_maplehwnd(self.maplehwnd)

    def rebindchathwnd(self):
        hwnd = 0
        windows=[]
        while True:
            hwnd = win32gui.FindWindowEx(0,hwnd,None, "MapleStory")
            if hwnd == 0:
                break
            windows.append(hwnd)
        for windowhwnd in windows:
            position = win32gui.GetWindowRect(windowhwnd)
            x, y, w, h = position
            if w-x == 410:
                self.chathwnd=windowhwnd
                return True
        return False


    def seperate_gma_detector(self):
        if self.chathwnd == None:
            print(f'seperate_gma_detector: chat window not found. ')
            return
        try:
            position = win32gui.GetWindowRect(self.chathwnd)
            x, y, w, h = position
            chatposition = (x,y+385,w-15,h-25)
            screenshot = ImageGrab.grab(chatposition)
            screenshot = np.array(screenshot)
            img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            height, width = img.shape[0], img.shape[1]
            img_reshaped = np.reshape(img, ((width * height), 3), order="C")
            locations = []
            sum_x, sum_y, count = 0, 0, 0
            matches = np.where(
                (img_reshaped[:,0] >= 201) & (img_reshaped[:,0] <= 225) &
                (img_reshaped[:,1] >= 201) & (img_reshaped[:,1] <= 225) &
                (img_reshaped[:,2] >= 201) & (img_reshaped[:,2] <= 225) 
                )[0]
            for idx in matches:
                sum_x += idx % width
                sum_y += idx // width
                count += 1
            if count > 0:
                x_pos = sum_x / count
                y_pos = sum_y / count
                locations.append((x_pos, y_pos))
            return locations
        except Exception as e:
            print(f'seperate_gma_detector {e=}')

    async def polocheckerfunc(self, gotoportal):
        truefalse=True
        if gotoportal:
            portaltype = await self.runesolver.gotopoloportal(self.g)
        else:
            portaltype = await self.runesolver.checkportaltype(self.g)
        if portaltype == 'b':
            print(f'dobountyhuntrotation')
            for i in range(6):
                if not self.pause:
                    await self.character.bountyhuntrotation()
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    print(f'stillinportal')
                    if await self.pausewrapper(self.character.bountyhuntrotation): return
                else:
                    print(f'notinportal')
                    while self.g.dark_checker() is not None:
                        print(f'map transitioning ..')
                        time.sleep(1)
                    await rightp()
                    time.sleep(2.5)
                    await rightr()
                    break
            await leftp()
            time.sleep(.5)
            await leftr()
            for i in range(6):
                await npcp()
                await npcr()
                time.sleep(.1)
            time.sleep(2.)
        elif portaltype == 'g':
            print(f'doguardingrotation')
            for i in range(10):            
                await self.character.castlewallrotation()
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    print(f'stillinportal')
                    await self.character.castlewallrotation()
                else:
                    print(f'notinportal')
                    while self.g.dark_checker() is not None:
                        print(f'map transitioning ..')
                        time.sleep(1)
                    await rightp()
                    time.sleep(1.5)
                    await rightr()
                    break
            await leftp()
            time.sleep(.8)
            await leftr()
            for i in range(8):
                await npcp()
                await npcr()
                await sleep(.1)
        elif portaltype == 'd':
            print(f'dostormwingrotation')
            await self.stormwing(100)
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    print(f'stillinportal')
                    await self.stormwing(10)
                    pass
                else:
                    print(f'notinportal')
                    while self.g.dark_checker() is not None:
                        print(f'map transitioning ..')
                        time.sleep(1)
                    await rightp()
                    time.sleep(1.5)
                    await rightr()
                    break
            await leftp()
            time.sleep(.8)
            await leftr()
            for i in range(7):
                await npcp()
                await npcr()
                time.sleep(.1)
        elif portaltype == 'e':
            print(f'doespeciaspam')
            for i in range(5):
                await self.especia()
            for count in range(100): # for testing
                huntingmaptimerchecker = self.g.especia_dot_checker()
                if huntingmaptimerchecker is not None:
                    print(f'stillinportal, {count=}')
                    await self.especia()
                    pass
                else:
                    print(f'notinportal')
                    while self.g.dark_checker() is not None:
                        print(f'map transitioning ..')
                        time.sleep(1)
                    time.sleep(1.5)
                    break
            for i in range(7):
                await npcp()
                await npcr()
                time.sleep(.1)
        elif portaltype == 'r':
            print(f'fritoportalendchat')
            position = win32gui.GetWindowRect(self.maplehwnd)
            x, y, w, h = position
            time.sleep(.1)
            await self.helper.move_to(x+self.portaldialogueX,y+self.portaldialogueY)
            time.sleep(.1)
            left_click()
            self.pausepolochecker=True
            self.polocheckertimer0 = self.now
            truefalse=False
        elif portaltype == 'f':
            print(f'clickendchat')
            position = win32gui.GetWindowRect(self.maplehwnd)
            x, y, w, h = position
            time.sleep(.1)
            await self.helper.move_to(x+self.portaldialogueX,y+self.wolfdialogueY)
            time.sleep(.1)
            left_click()
            self.pausepolochecker=True
            self.polocheckertimer0 = self.now
            truefalse=False
        else:
            print(f'enterportalfailedorerror') # means enter portal failed, or error, back to training. 
        self.polochecker=False
        return truefalse

    def resumebutton(self):
        self.pause = not self.pause
        print(f'resumebutton pressed .. {self.pause}')
        if self.pause:
            self.button.configure(text='Resume', fg_color='tomato')
            self.runesolver.disablerune()
            self.character.ac.disablerune()
        else:
            self.button.configure(text='Pause', fg_color='lime')
            self.runesolver.enablerune()
            self.character.ac.enablerune()

    async def togglepause(self):
        # self.pause=True
        self.resumebutton()
        self.scriptpausesignal=True
        self.scriptbuttonstop.configure(state='normal')        

    async def pausewrapper(self, func):
        if not self.pause:
            await func()
        else:
            time.sleep(1)            
            if self.stop_event.is_set():
                # self.thread4.join()
                return True
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        # print(f'{update.message=}')
        # print(f'{self.chat_id=}')
        # print(f'{type(self.chat_id)=}')
        # print(f'{type(update.message.chat.id)=}')
        if str(update.message.chat.id) == self.chat_id:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        else:
            print(f'Denied User ({update.message.chat.id}) in {message_type}: "{text}"')
            return
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')        
        print(f'telegramstatus')
        now = perf_counter()
        photo0 = self.g.get_screenshot()
        success, photo0_encoded = cv2.imencode('.png', photo0)
        photo0_bytes = photo0_encoded.tobytes()
        files = {'photo': photo0_bytes}
        payload = {
            'chat_id': self.chat_id,
            'caption': 'dummy photo'
        }
        # response = requests.post('https://api.telegram.org/bot'+self.TOKEN+'/sendPhoto', data=payload, files=files)
        # if response.status_code == 200:
        #     print(f'{perf_counter()-now =}')
        #     print(f"success {response.json().get('description')}")
        #     print(f"success {response.json()}")
        # else:
        #     print(f"Request failed with status code_: {response.status_code}")
        #     print(f"{response.json().get('description')}")
        # await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')
        await update.message.reply_photo(photo0_bytes)
        print(f'{perf_counter()-now =}')
    
    async def especia(self):
        for i in range(1):
            await npcp()
            await npcr()
            r = random.randint(500,1000)
            r /= 1000
            await sleep(r)
            if self.pause:
                print(f'script is paused .. click resume to resume. ')
                while self.pause:
                    time.sleep(1)
                    if self.stop_event.is_set():
                        return
                print(f'script resumed ..')

    async def stormwing(self, count):
        goleft=False
        goright=True        
        top=29.0 ## 1.8 165.2 (top=24.5?) (btm=62.5) (right=138.5?)
        left=35.0 # 18.0 # 27.0
        right=130 # 125.0 # 135.0 140.0 132.5
        btm=58.0 # 54.5
        for i in range(count):            
            huntingmaptimerchecker = self.g.hunting_map_timer_checker()
            if huntingmaptimerchecker is None:
                return
            time.sleep(.3) # running real
            g_variable = self.g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            if x == None or y == None:
                xynotfound+=1
                if xynotfound > 50:
                    t = time.localtime()
                    currenttime = time.strftime("%H:%M:%S", t)
                    print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                    return
                print(f'x==None, pass ..')
                time.sleep(.1)
                pass
            else:
                xynotfound=0
                print(f'{x=} {y=} {goleft=} {goright=}')
                goleft,goright = await self.character.stormwing(x,y,goleft,goright)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(f'{update.message}')
        if update.message.chat.id == 5630992696:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        elif update.message.chat.id == 1125332211:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        else:
            print(f'Denied User ({update.message.chat.id}) in {message_type}: "{text}"')
            return
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
        await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')

    def setup_tab(self):
        self.mytab = customtkinter.CTkTabview(self,width=600,height=800,corner_radius=5)
        self.mytab.pack(padx=(1,1),pady=(1,1))
        self.tab1 = self.mytab.add("Rotation")
        self.tab2 = self.mytab.add("Script")
        self.tab3 = self.mytab.add("Design")
        self.tab4 = self.mytab.add("Telegram")
        self.tab5 = self.mytab.add("Autoclicker")
        self.tab6 = self.mytab.add("Settings")

    def setup_tab1(self):
        framebase = customtkinter.CTkFrame(self.tab1)
        framebase.pack(padx=0, pady=(0,2), fill='x', expand=False)
        framebase.columnconfigure(0,weight=1)
        framebase.columnconfigure(1,weight=1)
        framebase.columnconfigure(2,weight=1)
        frameleft = customtkinter.CTkFrame(framebase, width=195, height=120, fg_color='transparent')
        frameleft.grid_propagate(0)
        frameleft.grid(row=0,column=0,padx=(1,1),pady=(1,1))
        framecenter = customtkinter.CTkFrame(framebase, width=195, height=120)
        framecenter.grid_propagate(0)
        framecenter.grid_rowconfigure(0,weight=1)
        framecenter.grid_columnconfigure(0,weight=1)
        framecenter.grid(row=0,column=1,padx=(1,1),pady=(1,1))
        frameright = customtkinter.CTkFrame(framebase, width=195, height=120, fg_color='transparent')
        frameright.grid_propagate(0)
        frameright.grid_columnconfigure(0,weight=1)
        frameright.grid(row=0,column=2,padx=(1,1),pady=(1,1))
        self.button = customtkinter.CTkButton(framecenter, text="Resume", command=self.resumebutton, fg_color='tomato', font=('Helvetica', 16), text_color='black',hover=False)
        self.button.grid(row=0,column=0,pady=(1,1), sticky=tk.N+tk.S+tk.E+tk.W)
        self.presettemp=self.preset
        def on_select(event):
            self.presettemp = comboboxpreset.get()
        folder_path = "preset"
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith(".json")]
        json_file_names = [os.path.splitext(file)[0] for file in json_files]
        comboboxpreset = customtkinter.CTkComboBox(frameleft, values=json_file_names, state="readonly",command=on_select,justify='left', width=120)
        comboboxpreset.grid(row=0,column=0,padx=(1,1), pady=(1,1), sticky=tk.NW)
        comboboxpreset.set(json_file_names[json_file_names.index(self.preset)])
        buttonreload = customtkinter.CTkButton(frameleft, text="load preset", command=self.reload, width=100)
        buttonreload.grid(row=1,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        def new():
            profile_name = simpledialog.askstring("New Profile", "Enter the name for the new profile:")
            if profile_name:
                json_file_names.append(profile_name)
                comboboxpreset.set(json_file_names[len(json_file_names)-1])
                comboboxpreset.configure(values=json_file_names)
                self.widthentry.delete(0,tk.END)
                self.widthentry.insert(0,200)
                self.heightentry.delete(0,tk.END)
                self.heightentry.insert(0,150)
                self.button_adjustminimap_fake()
                self.update_four_lines(180,220,60,90)
                self.presettemp = comboboxpreset.get()
        buttonnew = customtkinter.CTkButton(frameleft, text="new preset", command=new, width=100)
        buttonnew.grid(row=2,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)        
        def save():
            self.preset=self.presettemp
            self.button_adjustminimap()
            allpresets=[]
            allpresets.append([self.minimapX,self.minimapY,self.line_position_slider.get(),self.line_position_slider2.get()
            ,self.line_position_slider3.get(),self.line_position_slider4.get()])
            with open(f'preset/{self.preset}.json', 'w') as json_file:
                json.dump(allpresets, json_file, indent=4)
            self.canvasimageholdertemp.save(f'image/{self.preset}.png')
            saved_window = customtkinter.CTkToplevel(frameleft, fg_color='#abcdef')
            saved_window.title('chrome')
            saved_window.resizable(False,False) # width,height
            def close():
                saved_window.destroy()
                saved_window.update()
            label=customtkinter.CTkLabel(saved_window,text=f'saved preset: {self.preset}. ', text_color='#123321')
            label.pack(padx=10,pady=(10,1), fill='none', expand=True)
            label2=customtkinter.CTkLabel(saved_window,text=f'{allpresets}', text_color='#123321')
            label2.pack(padx=10,pady=(1,10), fill='none', expand=True)
            button=customtkinter.CTkButton(saved_window,text='ok',command=close)
            button.pack(padx=10,pady=10, fill='none', expand=True)
            saved_window.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
            saved_window.wm_iconbitmap()
            saved_window.iconphoto(False, saved_window.iconpath)
            saved_window.after(200,lambda: saved_window.iconphoto(False, saved_window.iconpath))
            width=int(self.winfo_screenwidth()/2)
            height=int(self.winfo_screenheight()/2)
            saved_window.geometry(f'{width-300}+{height-200}')
        buttonsave = customtkinter.CTkButton(frameleft, text="save all", command=save, width=100)
        buttonsave.grid(row=3,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        
        def minus():
            try:
                value = int(self.widthentry.get())
                value = value-10 if value > 100 else value
                self.widthentry.delete(0,tk.END)
                self.widthentry.insert(0,str(value))
            except Exception as e:
                print(f'not a digit. {e=}')
                self.widthentry.delete(0,tk.END)
                self.widthentry.insert(0,self.minimapX)
        def plus():
            try:
                value = int(self.widthentry.get())
                value = value+10 if value < 400 else value
                self.widthentry.delete(0,tk.END)
                self.widthentry.insert(0,str(value))
            except Exception as e:
                print(f'not a digit. {e=}')
                self.widthentry.delete(0,tk.END)
                self.widthentry.insert(0,self.minimapX)
        def minus2():
            try:
                value = int(self.heightentry.get())
                value = value-10 if value > 100 else value
                self.heightentry.delete(0,tk.END)
                self.heightentry.insert(0,str(value))
            except Exception as e:
                print(f'not a digit. {e=}')
                self.heightentry.delete(0,tk.END)
                self.heightentry.insert(0,self.minimapY)
        def plus2():
            try:
                value = int(self.heightentry.get())
                value = value+10 if value < 300 else value
                self.heightentry.delete(0,tk.END)
                self.heightentry.insert(0,str(value))
            except Exception as e:
                print(f'not a digit. {e=}')
                self.heightentry.delete(0,tk.END)
                self.heightentry.insert(0,self.minimapY)
        frame = customtkinter.CTkFrame(self.tab1)
        frame.pack(padx=1, pady=2)
        widthframe = customtkinter.CTkFrame(frame, fg_color="transparent", height=30, width=150)
        widthframe.grid(row=0, column=0, padx=(2, 2), pady=1)
        widthframe.grid_columnconfigure((0, 2), weight=0)   # buttons don't expand
        widthframe.grid_columnconfigure(1, weight=0)        # entry expands
        widthsub = customtkinter.CTkButton(widthframe, text="-", command=minus,height=30, width=30)
        widthsub.grid(row=0, column=0, padx=(2, 2), pady=1, sticky='w')
        self.widthentry = customtkinter.CTkEntry (widthframe, border_width=1,justify='right',placeholder_text='x',placeholder_text_color='grey',font=('Helvetica', 12),state='normal',height=30, width=80)
        self.widthentry.grid(row=0, column=1, padx=(2, 2), pady=1, sticky='we')
        widthadd = customtkinter.CTkButton(widthframe, text="+", command=plus,height=30, width=30)
        widthadd.grid(row=0, column=2, padx=(2, 1), pady=1, sticky='w')
        heightframe = customtkinter.CTkFrame(frame, fg_color="transparent", height=30, width=150)
        heightframe.grid(row=0, column=1, padx=(0, 0), pady=1)
        heightframe.grid_columnconfigure((0, 2), weight=0)   # buttons don't expand
        heightframe.grid_columnconfigure(1, weight=0)        # entry expands
        heightsub = customtkinter.CTkButton(heightframe, text="-", command=minus2,height=30, width=30)
        heightsub.grid(row=0, column=0, padx=(1, 2), pady=1, sticky='w')
        self.heightentry = customtkinter.CTkEntry (heightframe,border_width=1,justify='right',placeholder_text='y',placeholder_text_color='grey',font=('Helvetica', 12),state='normal',height=30, width=80)
        self.heightentry.grid(row=0, column=1, padx=(2, 2), pady=1, sticky='we')
        heightadd = customtkinter.CTkButton(heightframe, text="+", command=plus2,height=30, width=30)
        heightadd.grid(row=0, column=2, padx=(2, 2), pady=1, sticky='w')
        buttonframe = customtkinter.CTkFrame(frame, fg_color="transparent", height=30, width=150)
        buttonframe.grid(row=0, column=2, padx=(1, 2), pady=1)
        button2 = customtkinter.CTkButton(buttonframe, text="adjust", command=self.button_adjustminimap,height=30, width=110)
        button2.grid(row=0, column=0, padx=(0,0), pady=(0,0))
        
        self.frame2 = customtkinter.CTkFrame(self.tab1)
        self.frame2.pack(padx=0, pady=0)
        image_path = "minimap.png"  # Replace with the actual path to your image
        img = PhotoImage(file=image_path)
        self.canvas = customtkinter.CTkCanvas(self.frame2, width=self.minimapX-8, height=self.minimapY-63)
        self.canvas.grid(row=0, column=0, rowspan=1, padx=0, pady=(0,0))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        #reload
        if self.preset:
            width=(self.minimapX-8)*2
            height=(self.minimapY-63)*2
            img_cropped = Image.open(f'image/{self.preset}.png')
            tk_image = ImageTk.PhotoImage(img_cropped)
            self.canvas.delete("all")
            self.canvas.config(width=width,height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            self.canvas.image = tk_image
            self.canvasimageholdertemp = img_cropped
            self.canvas_width=(self.minimapX-8)*2
            self.canvas_height=(self.minimapY-63)*2
        else:
            hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
            top, left, bottom, right = 8, 63, self.minimapX, self.minimapY
            with gdi_capture.CaptureWindow(hwnd) as gdiimg:
                img_cropped = gdiimg[left:right, top:bottom]
                img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
                height, width = img_cropped.shape[:2]
                width = width*2
                height = height*2
                img_cropped = cv2.resize(img_cropped, (width, height))
                img_cropped = Image.fromarray(img_cropped)
                tk_image = ImageTk.PhotoImage(img_cropped)
                self.canvas.delete("all")
                self.canvas.config(width=width,height=height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                self.canvas.image = tk_image 
                canvasimageholdertemp = img_cropped
                self.canvas_width=width
                self.canvas_height=height

        if True:
            self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, height, fill="red", width=2)    
            self.line_position_slider = customtkinter.CTkSlider(self.frame2,from_=2,to=self.canvas_width,orientation='horizontal',number_of_steps=self.canvas_width-2, width=self.canvas_width, command=self.update_line_position)
            self.line_position_slider.grid(row=1, column=0, pady=0, padx=0, sticky='we')
            
            self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, height, fill="yellow", width=2)    
            self.line_position_slider2 = customtkinter.CTkSlider(self.frame2,from_=2,to=self.canvas_width,orientation='horizontal',number_of_steps=self.canvas_width-2, width=self.canvas_width, command=self.update_line_position2)
            self.line_position_slider2.grid(row=2, column=0, pady=(0,2), padx=0, sticky='we')

            self.vertical_line3 = self.canvas.create_line(self.canvas_width, self.initial_line_position3, 2, self.initial_line_position3, fill="lime", width=2)
            self.line_position_slider3 = customtkinter.CTkSlider(self.frame2,to=2,from_=self.canvas_height,orientation='vertical',number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3, command=self.update_line_position3)
            self.line_position_slider3.grid(row=0, column=1, rowspan=3, pady=(0,0), padx=(2,1), sticky='ns')

            self.vertical_line4 = self.canvas.create_line(self.canvas_width, self.initial_line_position4, 2, self.initial_line_position4, fill="lightblue", width=2)
            self.line_position_slider4 = customtkinter.CTkSlider(self.frame2,to=2,from_=self.canvas_height,orientation='vertical',number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3, command=self.update_line_position4)
            self.line_position_slider4.grid(row=0, column=2, rowspan=3, pady=(0,0), padx=(0,0), sticky='ns')
            
            self.reload()
            def on_select_rotation(event): # tag UI placement order # can only initializd after reload() # todo: organize code nicer
                self.rotation = self.comboboxrotation.get()
                self.character.set_rotation(self.rotation)
            rotation_list = self.character.get_rotation_list()
            self.comboboxrotation = customtkinter.CTkComboBox(frameright, values=rotation_list, state="readonly",command=on_select_rotation,justify='left', width=140)
            self.comboboxrotation.grid(row=0,column=0,padx=(1,1), pady=(1,1), sticky=tk.NE)
            self.comboboxrotation.set(rotation_list[rotation_list.index(self.rotation)])

            self.frame4 = customtkinter.CTkFrame(self.tab1, height=50, width=100)
            self.frame4.pack(padx=0, pady=0, side='bottom', fill='x')
            button4 = customtkinter.CTkButton(self.frame4, text="Test Mouse", command=self.testmouse, font=('Helvetica', 12))
            button4.grid(row=0, column=0, pady=(0,0), padx=(1,1))
            button5 = customtkinter.CTkButton(self.frame4, text="Rebind Mouse", command=self.rebindmouse, font=('Helvetica', 12))
            button5.grid(row=0, column=1, pady=(0,0), padx=(1,1))
            button6 = customtkinter.CTkButton(self.frame4, text="Rebind Chat Window", command=self.rebindchathwnd, font=('Helvetica', 12))
            button6.grid(row=0, column=2, pady=(0,0), padx=(1,1))

    def testmouse(self):
        self.triggermousetest=True
        print(f'{self.triggermousetest=}')

    def rebindmouse(self):
        print(f'rebind mouse. ')
        auto_capture_devices2()

    def button_adjustminimap_fake(self):
        minimapX = int(self.widthentry.get())
        minimapY = int(self.heightentry.get())
        hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        top, left, bottom, right = 8, 63, minimapX, minimapY
        with gdi_capture.CaptureWindow(hwnd) as img:            
            img_cropped = img[left:right, top:bottom]
            height = (right-left)*2
            width = (bottom-top)*2
            img_cropped = cv2.resize(img_cropped, (width, height))
            img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
            img_cropped = Image.fromarray(img_cropped)
            tk_image = ImageTk.PhotoImage(img_cropped)
            self.canvas.delete("all")
            self.canvas.configure(width=width,height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            self.canvas.image = tk_image
            self.canvasimageholdertemp = img_cropped            
            self.canvas_width=width
            self.canvas_height=height
        self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, height, fill="red", width=2)    
        self.line_position_slider.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position(self.line_position_slider.get())
        self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, height, fill="yellow", width=2)    
        self.line_position_slider2.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position2(self.line_position_slider2.get())
        self.vertical_line3 = self.canvas.create_line(self.canvas_width, self.initial_line_position3, 2, self.initial_line_position3, fill="lime", width=2)
        self.line_position_slider3.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position3(self.line_position_slider3.get())
        self.vertical_line4 = self.canvas.create_line(self.canvas_width, self.initial_line_position4, 2, self.initial_line_position4, fill="lightblue", width=2)
        self.line_position_slider4.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position4(self.line_position_slider4.get())
        self.g = Game((8, 63, self.minimapX, self.minimapY)) #   

    def button_adjustminimap(self, setimage=False):
        try: # will remain as original value even if error
            self.minimapX = int(self.widthentry.get())
        except Exception as e:
            print(f'adjust button: {e=}')
            self.widthentry.delete(0,tk.END)
            self.widthentry.insert(0,self.minimapX)
        try: # will remain as original value even if error
            self.minimapY = int(self.heightentry.get())
        except Exception as e:
            print(f'adjust button: {e=}')
            self.heightentry.delete(0,tk.END)
            self.heightentry.insert(0,self.minimapY)
        if self.minimapX > 400:
            self.minimapX=400
        if self.minimapY > 300:
            self.minimapY=300
        if self.minimapX < 100:
            self.minimapX=100
        if self.minimapY < 100:
            self.minimapY=100
        if setimage:
            width=(self.minimapX-8)*2
            height=(self.minimapY-63)*2
            img_cropped = Image.open(f'image/{self.preset}.png')
            tk_image = ImageTk.PhotoImage(img_cropped)
            self.canvas.delete("all")
            self.canvas.configure(width=width,height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            self.canvas.image = tk_image
            self.canvasimageholdertemp = img_cropped
            self.canvas_width=width
            self.canvas_height=height
            initial_line_position = self.canvas_width / 2
        else:
            hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
            top, left, bottom, right = 8, 63, self.minimapX, self.minimapY
            with gdi_capture.CaptureWindow(hwnd) as img:            
                img_cropped = img[left:right, top:bottom]
                height = (right-left)*2
                width = (bottom-top)*2
                img_cropped = cv2.resize(img_cropped, (width, height))
                img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
                img_cropped = Image.fromarray(img_cropped)
                tk_image = ImageTk.PhotoImage(img_cropped)
                self.canvas.delete("all")
                self.canvas.configure(width=width,height=height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
                self.canvas.image = tk_image
                self.canvasimageholdertemp = img_cropped
                
                self.canvas_width=width
                self.canvas_height=height
                initial_line_position = self.canvas_width / 2

        self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, height, fill="red", width=2)    
        self.line_position_slider.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position(self.line_position_slider.get())
        
        self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, height, fill="yellow", width=2)    
        self.line_position_slider2.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position2(self.line_position_slider2.get())
        
        self.vertical_line3 = self.canvas.create_line(self.canvas_width, self.initial_line_position3, 2, self.initial_line_position3, fill="lime", width=2)
        self.line_position_slider3.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position3(self.line_position_slider3.get())

        self.vertical_line4 = self.canvas.create_line(self.canvas_width, self.initial_line_position4, 2, self.initial_line_position4, fill="lightblue", width=2)
        self.line_position_slider4.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position4(self.line_position_slider4.get())
        
        self.line_position_slider.set(self.line_position_slider.get())
        self.line_position_slider2.set(self.line_position_slider2.get())
        self.line_position_slider3.set(self.line_position_slider3.get())
        self.line_position_slider4.set(self.line_position_slider4.get())
        self.g = Game((8, 63, self.minimapX, self.minimapY)) #
        self.character.setup(
            left=self.line_position_slider.get()/2,
            right=self.line_position_slider2.get()/2,
            top=self.line_position_slider3.get()/2,
            btm=self.line_position_slider4.get()/2,
            classtype=self.classtype,
            runesolver=self.runesolver,
            g=self.g,
            rotation=self.rotation,
            maplehwnd=self.maplehwnd
        )

    def update_four_lines(self,line1,line2,line3,line4):        
        self.line_position_slider.set(line1)
        self.line_position_slider2.set(line2)
        self.line_position_slider3.set(line3)
        self.line_position_slider4.set(line4)
        self.update_line_position(line1)
        self.update_line_position2(line2)
        self.update_line_position3(line3)
        self.update_line_position4(line4)

    def update_line_position(self, value):
        self.canvas.coords(self.vertical_line, float(value), 0, float(value), self.canvas_height)
    
    def update_line_position2(self, value):
        self.canvas.coords(self.vertical_line2, float(value), 0, float(value), self.canvas_height)

    def update_line_position3(self, value):
        self.canvas.coords(self.vertical_line3, 0, float(value), self.canvas_width, float(value))
    
    def update_line_position4(self, value):
        self.canvas.coords(self.vertical_line4, 0, float(value), self.canvas_width, float(value))

    def reload(self):
        self.pause=True
        self.preset=self.presettemp
        try:
            allpresets=[]
            with open(f'preset/{self.preset}.json', 'r') as json_file:
                arrays = json.load(json_file)
            for array in arrays:
                for item in array:
                    allpresets.append(item)
            self.minimapX=allpresets[0]
            self.minimapY=allpresets[1]
            self.widthentry.delete(0,tk.END)
            self.widthentry.insert(0,self.minimapX)
            self.heightentry.delete(0,tk.END)
            self.heightentry.insert(0,self.minimapY)
            self.button_adjustminimap(setimage=True)
            self.update_line_position(allpresets[2])
            self.update_line_position2(allpresets[3])
            self.update_line_position3(allpresets[4])
            self.update_line_position4(allpresets[5])
            self.line_position_slider.set(allpresets[2])
            self.line_position_slider2.set(allpresets[3])
            self.line_position_slider3.set(allpresets[4])
            self.line_position_slider4.set(allpresets[5])
  
        except Exception as e:
            print(f'reading json: {e=}')
        self.left=self.line_position_slider.get()/2
        self.right=self.line_position_slider2.get()/2
        self.top=self.line_position_slider3.get()/2
        self.btm=self.line_position_slider4.get()/2
        self.character.setup(left=self.left,right=self.right,top=self.top,btm=self.btm)
            
    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())

    def setup_tab2(self):
        framerecord = customtkinter.CTkFrame(self.tab2, fg_color='#81b253')
        framerecord.pack(padx=1, pady=1)
        def new():
            script_name = simpledialog.askstring("New Script", "Enter the name for the new script:")
            if script_name:
                script_name=script_name+'.json'
                json_file_names.append(script_name)
                comboboxpreset.set(json_file_names[len(json_file_names)-1])
                comboboxpreset.configure(values=json_file_names)
                self.scripttemp = comboboxpreset.get()
                length=0
                self.signature=''
                self.labelscript.configure(text=f'script duration: {length}')
                labelpointa.configure(text=f'(None, None)')
        buttonnew = customtkinter.CTkButton(framerecord, text="new script", command=new)
        buttonnew.grid(row=2,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        buttonnew.pack(padx=(1,1),pady=(1,1))
        def on_select(event):
            self.scripttemp = comboboxpreset.get()
            self.script = comboboxpreset.get()
            try:
                with open(f'point/{self.scripttemp}', 'r') as jsonfile:
                    data = json.load(jsonfile)
                    self.pointx=data[0]
                    self.pointy=data[1]
                    labelpointa.configure(text=f'({self.pointx}, {self.pointy})')
                length=0
                self.signature=''
                with open(f'script/{self.scripttemp}', 'r') as jsonfile:
                    data = json.load(jsonfile)            
                    for index, action in enumerate(data):
                        if action['type']=='keyUp':
                            self.signature+=action['button']
                    length=round(data[-1]['time'],4)
                self.labelscript.configure(text=f'script duration: {length}')
            except Exception as e:
                self.labelscript.configure(text=f'script duration: ')
        folder_path = "script"
        file_list = os.listdir(folder_path)
        json_file_names = [file for file in file_list if file.endswith(".json")]
        comboboxpreset = customtkinter.CTkComboBox(framerecord, values=json_file_names, state="readonly",command=on_select,justify='center')
        comboboxpreset.pack(padx=(1,1), pady=(1,1))
        comboboxpreset.set(json_file_names[json_file_names.index(self.script)])
        def clock():
            if self.recordstatus:
                return
            else:
                elapsed = perf_counter()-self.time
                time_label.configure(text="{:.4f}s".format(elapsed))
                time_label.after(1000,clock)
        def record():
            if self.recordstatus:
                self.recordstatus=not self.recordstatus
                self.record_button.configure(fg_color='#ff9966', text='Stop', text_color='black',state='disabled')
                self.time=perf_counter()
                clock()
                self.thread7 = threading.Thread(target=self.run_thread7)
                self.thread7.start()
            else:
                pass
        self.scripttemp=self.script
        self.recordstatus=True
        self.input_events=[]
        self.realrecordstopsignal=False
        self.record_button = customtkinter.CTkButton(framerecord, text="Record",fg_color='#55eecc',text_color='black',command=record, font=('Helvetica', 12))
        self.record_button.pack(padx=1, pady=1)
        time_label = customtkinter.CTkLabel(framerecord, text='0.0000s', font=('Helvetica', 12), text_color='black')
        time_label.pack(padx=1,pady=1)
        def save():
            self.script=self.scripttemp
            with open(f'script/{self.script}', 'w') as json_file:
                json.dump(self.input_events, json_file, indent=4)
            pointA = (self.pointx,self.pointy)
            with open(f'point/{self.script}', 'w') as json_file:
                json.dump(pointA, json_file, indent=4)
            saved_window = customtkinter.CTkToplevel(framerecord, fg_color='#abcdef')
            saved_window.title('chrome')
            saved_window.resizable(False,False)#width,height
            def close():
                saved_window.destroy()
                saved_window.update()
            label=customtkinter.CTkLabel(saved_window,text=f'saved script: {self.script}. ', text_color='#123321')
            label.pack(padx=10,pady=(10,1), fill='none', expand=True)
            button=customtkinter.CTkButton(saved_window,text='ok',command=close)
            button.pack(padx=10,pady=10, fill='none', expand=True)
            saved_window.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
            saved_window.wm_iconbitmap()
            saved_window.iconphoto(False, saved_window.iconpath)
            saved_window.after(200,lambda: saved_window.iconphoto(False, saved_window.iconpath))
            width=int(self.winfo_screenwidth()/2)
            height=int(self.winfo_screenheight()/2)
            saved_window.geometry(f'{width-300}+{height-200}')
        buttonsave = customtkinter.CTkButton(framerecord, text="save all", command=save)
        buttonsave.pack(padx=(1,1),pady=(1,1))
        framescript = customtkinter.CTkFrame(self.tab2, fg_color='#81b253')
        framescript.pack(padx=1, pady=1)
        def setpointa():
            g_variable = self.g.get_player_location()
            self.pointx, self.pointy = (None, None) if g_variable is None else g_variable
            labelpointa.configure(text=f'({self.pointx}, {self.pointy})')
        buttonsetpointa = customtkinter.CTkButton(framescript, text="set point A", command=setpointa)
        buttonsetpointa.pack(padx=1, pady=1)
        labelpointa=customtkinter.CTkLabel(framescript,text=f'', text_color="#010101",justify='left')
        labelpointa.pack(padx=1,pady=1)
        length=0
        self.signature=''
        with open(f'script/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)            
            for index, action in enumerate(data):
                if action['type']=='keyUp':
                    self.signature+=action['button']
            length=round(data[-1]['time'],4)
        self.labelscript=customtkinter.CTkLabel(framescript,text=f'script duration: {length}', text_color="#010101",justify='left')
        self.labelscript.pack(padx=1,pady=1)
        def showscript():
            showscript_window = customtkinter.CTkToplevel(framescript, fg_color='#abcdef')
            showscript_window.title('chrome')
            showscript_window.resizable(False,False)#width,height
            label=customtkinter.CTkLabel(showscript_window,text=f'script signature: {self.signature}. ', text_color='#123321')
            label.pack(padx=10,pady=(10,1), fill='none', expand=True)
            def close():
                showscript_window.destroy()
                showscript_window.update()
            button=customtkinter.CTkButton(showscript_window,text='ok',command=close)
            button.pack(padx=10,pady=10, fill='none', expand=True)
            showscript_window.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
            showscript_window.wm_iconbitmap()
            showscript_window.iconphoto(False, showscript_window.iconpath)
            showscript_window.after(200,lambda: showscript_window.iconphoto(False, showscript_window.iconpath))
            width=int(self.winfo_screenwidth()/2)
            height=int(self.winfo_screenheight()/2)
            showscript_window.geometry(f'{width-300}+{height-200}')
        buttonshowscript = customtkinter.CTkButton(framescript, text="show script", command=showscript)
        buttonshowscript.pack(padx=1, pady=1)
        with open(f'point/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)
            self.pointx=data[0]
            self.pointy=data[1]
            labelpointa.configure(text=f'({self.pointx}, {self.pointy})')
        framesonic = customtkinter.CTkFrame(self.tab2, fg_color='#81b253')
        framesonic.pack(padx=1, pady=1)
        def stop():
            self.scriptstopsignal=True
            self.thread8.join() 
            buttonplayback.configure(state='normal')
            buttonpause.configure(state='disabled')
            self.scriptbuttonstop.configure(state='disabled')       
        self.scriptstopsignal=False
        imageknuckles = customtkinter.CTkImage(Image.open("assets/knuckles1.png"),size=(140,140))
        self.scriptbuttonstop = customtkinter.CTkButton(framesonic, text="stop", command=stop, fg_color='#ea511f', text_color='black',state='disabled')
        # self.scriptbuttonstop = customtkinter.CTkButton(framesonic, text="", command=stop, fg_color='#ea511f', text_color='black',image=imageknuckles,state='disabled')
        # self.scriptbuttonstop = customtkinter.CTkButton(framesonic, text="", command=stop, fg_color='#ff1400', text_color='black',image=imageknuckles)
        self.scriptbuttonstop.pack(padx=(1,1),pady=(1,1))
        def pause():
            self.scriptpausesignal=not self.scriptpausesignal
            self.scriptbuttonstop.configure(state='normal') if self.scriptpausesignal else self.scriptbuttonstop.configure(state='disabled')
        self.scriptpausesignal=False
        imagetails = customtkinter.CTkImage(Image.open("assets/tails1.png"),size=(140,140))
        buttonpause = customtkinter.CTkButton(framesonic, text="pause/resume", command=pause, fg_color='#f1bf1f', text_color='black',state='disabled')
        # buttonpause = customtkinter.CTkButton(framesonic, text="", command=pause, fg_color='#f1bf1f', text_color='black',image=imagetails,state='disabled')
        # buttonpause = customtkinter.CTkButton(framesonic, text="", command=pause, fg_color='#f1b000', text_color='black',image=imagetails)
        buttonpause.pack(padx=(1,1),pady=(1,1))
        def playback():
            self.thread8 = threading.Thread(target=self.run_thread8)
            self.thread8.start()
            self.scriptpausesignal=False
            self.scriptstopsignal=False
            buttonplayback.configure(state='disabled')
            buttonpause.configure(state='normal')
            self.scriptbuttonstop.configure(state='disabled')
        imagesonic = customtkinter.CTkImage(Image.open("assets/sonic1.png"),size=(140,140))
        buttonplayback = customtkinter.CTkButton(framesonic, text="play", command=playback, fg_color='#0d7adf', text_color='black')
        # buttonplayback = customtkinter.CTkButton(framesonic, text="", command=playback, fg_color='#0d7adf', text_color='black',image=imagesonic)
        buttonplayback.pack(padx=(1,1),pady=(1,1))

    async def changechannel_zakum(self):
        async def press(button,sleep):
                await button()
                time.sleep(sleep)
        position = win32gui.GetWindowRect(self.maplehwnd)
        x, y, w, h = position
        # set a limit for cc, in case character died, stop it from spamming cc! i've been banned once due to this spamming! no appeal. 
        for i in range(10): # set a limit on how many tries to attempt to move to zakum map to avoid BAN!
            print(f'this is try no.{i} ..')
            if i > 8: self.togglepause() # something wrong. you are done. # self.pause=True # hopefully this work. not tested. yet. #self.scriptstopsignal=True
            if self.pause: return
            await self.character.ac.bossuipr() # remember set it in settings.ini
            await self.helper.move_to_and_click(x+104,y+204) # zakum 800x600
            await self.helper.move_to_and_click(x+510,y+562) # gobutton 800x600
            if self.helper.still_in_zakum_map2(self.g,self.maplehwnd):
                break # successfully entered zakum map. exit loop. 
        time.sleep(1.)
        await self.character.ac.ccbuttonpr()
        time.sleep(5.) # in case character were still using some skills just before enter zakum map. you can change this number just becareful. 
        [await self.character.ac.leftpr() for _ in range(random.randint(1, 5))]
        [await self.character.ac.downpr() for _ in range(random.randint(1, 3))] # why not
        await self.character.ac.enterpr()
        time.sleep(2.) # 
        while self.helper.still_in_zakum_map2(self.g,self.maplehwnd): # move character to zakum entrance portal to go out. 
            await self.helper.adjustportal2(g=self.g,spot=21,distx=10.5,docorrection=True,ca=self.character.ac) 
            [await press(self.character.ac.uppr,.06) for _ in range(random.randint(1, 2))]
        # check for red dot/guild dot/bl dot after cc
        await self.helper.checkreddotaftercomeoutfromzakummap(hwnd=self.maplehwnd,ca=self.character.ac, position1=(self.minimapX,self.minimapY)) # sorry perfectionist =(
        # TODO: repeat this function for guild dot 
        # TODO: count number of red dot/guild dot/bl dot (instanced map)
        

    async def changechannel(self): # ardentmill version
        position = win32gui.GetWindowRect(self.maplehwnd)
        x, y, w, h = position
        async def gotoardent():
            await self.helper.move_to_and_click(x+559,y+233) # click somewhere else to prevent typing in chat. 
            time.sleep(.5)
            await self.character.ac.ardentp(11,31)
            await self.character.ac.ardentr(3,11)
            time.sleep(.5)
            await self.helper.move_to_and_click(x+539,y+253) # ardentmill offset (800x600) TODO: write a list of offset for all reso. 
            time.sleep(.5)
            await self.character.ac.enterpr()
            time.sleep(3)
        async def checkstillinardentmill():            
            for i in range(7):
                if i > 5: self.togglepause() # self.pause=True
                if self.pause: return False
                weareinardentyesno = self.g.ardentdetector()
                if self.g.ardentdetector() is None:
                    print(f'we are not in ardentmill. {i=} {weareinardentyesno=}')
                    await gotoardent()
                else:
                    print(f'we are in ardentmill. {i=} {weareinardentyesno=}')
                    await self.helper.move_to_and_click(x+559,y+233) # click somewhere else to prevent typing in chat. 
                    time.sleep(.5)
                    await self.character.ac.ardentpr() # close the ui
                    time.sleep(.5)
                    return True
        async def press(button,sleep):
                await button()
                time.sleep(sleep)
        # go to ardent code starts here. 
        if not await checkstillinardentmill(): # if return False, means either user paused or tries end (5 times). 
            return # then we return and bye. if True, proceed. 
        await self.character.ac.ccbuttonpr() # proceed. 
        time.sleep(3.)        
        [await self.character.ac.leftpr() for _ in range(random.randint(1, 10))]
        time.sleep(.5)        
        await self.character.ac.enterpr()
        time.sleep(2.) # adjust this to your pc loading speed i guess, mine need 5 seconds to cc. 
        [await press(self.character.ac.uppr,.06) for _ in range(random.randint(4, 10))] # ideally TODO: check ardentmill map loaded. 
        time.sleep(2.) # coming out from ardent. TODO: check if back to hunting map.
        for i in range(10): # set a limit to check. 
            if i > 8: self.togglepause() # self.pause=True # set a limit
            if self.pause: return
            if self.g.ardentdetector() is None: # we not in ardent. 
                if self.g.ardentmaploading() is not None: # still loading. (whole maple dark)
                    time.sleep(.5) # do nothing for .5 seconds. 
                else:
                    if self.g.ardentdetector() is None: # final check that we not in ardent
                        break
            else: # we still in ardent TODO: if exceed x number of time, just cc again to align with portal and press up. 
                time.sleep(.5)
        await self.helper.checkreddotaftercomeoutfromzakummap(hwnd=self.maplehwnd,ca=self.character.ac, position1=(self.minimapX,self.minimapY)) #
        # TODO: set a limit for cc, in case character died, stop it from spamming cc! i've been banned once due to this spamming! no appeal can be made.  

    async def playback(self):
        time.sleep(1)
        now=perf_counter()
        runetimer0=now
        runetimer=0
        rune=False
        cctimer0=now
        cctimer=0
        self.cc=False
        with open(f'script/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)
            while True:
                print(f'starting script {self.script} in 1 ..')
                time.sleep(1) # testing 
                for index, action in enumerate(data):
                    # print(f'running: {index=} {action=}')
                    if pythonkeyboard.is_pressed("esc"):
                        self.scriptpausesignal=True
                        self.scriptbuttonstop.configure(state='normal')
                        print(f'yes p={self.scriptpausesignal}')
                    if self.scriptpausesignal:
                        keyupall()
                        print(f'script is paused .. ')
                        while self.scriptpausesignal:
                            if self.scriptstopsignal:
                                return
                            # do nothing
                            time.sleep(1)
                            if self.stop_event.is_set():
                                return
                        print(f'script resumed ..')

                    if action['type'] == 'keyDown':
                        if action['button'] == 'f9':
                            # print('read f9')
                            await self.adjustcharacter(self.pointx,self.pointy)
                        if action['button'] == 'f10':
                            # print('f10')
                            # await self.adjustcharacter(self.pointx,self.pointy)
                            pass
                        key = action['button']
                        # print(f'press {key=}')
                        keydown(key)
                    elif action['type'] == 'keyUp':
                        key = action['button']
                        # print(f'release {key=}')
                        keyup(key)
                    try:
                        next_action = data[index + 1]
                    except IndexError:
                        # this was the last action in the list
                        break
                    elapsed_time = next_action['time'] - action['time']
                    # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
                    if elapsed_time < 0:
                        raise Exception('Unexpected action ordering.')
                    elapsed_time = round(elapsed_time, -int(floor(log10(abs(elapsed_time)))) + (2))
                    # if next_action['type'] == 'keyUp' or action['button'] == '06' or next_action['button'] == '06':
                    if next_action['type'] == 'keyUp':
                        pass
                    else:
                        if elapsed_time < 0.001:
                            elapsed_time = 0.001
                        elif elapsed_time < 0.011:
                            r = random.randint(1, 10)
                            r /= 1000
                            elapsed_time = r
                        elif elapsed_time < 0.031:
                            r = random.randint(11, 31)
                            r /= 1000
                            elapsed_time = r
                        elif elapsed_time < 0.131:
                            r = random.randint(31, 131)
                            r /= 1000
                            elapsed_time = r
                        else:
                            # e1 = elapsed_time - 0.01
                            # e2 = elapsed_time + 0.01
                            # e1 = round(e1, -int(floor(log10(abs(e1)))) + (2))
                            # e2 = round(e2, -int(floor(log10(abs(e2)))) + (2))
                            r = random.randint(0, 11)
                            if r % 2 == 0:
                                r /= 1000
                                elapsed_time += r
                            else:
                                r /= 1000
                                elapsed_time -= r
                    # print(f'sleep={elapsed_time=}')
                    await sleep(elapsed_time)

                    # here onwards are equivalent to post_perform_action()
                    if action['type'] == 'keyUp' and index%10<=3: # don't do checking for all key input. do every 10 key input
                        now=perf_counter()
                        # runetimer=now-runetimer0
                        # if runetimer>900:
                        #     # rune=True
                        #     gotrune=self.runesolver.runechecker(self.g)
                        #     if gotrune:
                        #         keyupall()
                        #         await self.runesolver.gotorune(self.g) # gotoruneandsolverune
                        #         await random.choice([self.character.ac.goleftattack,self.character.ac.gorightattack])(); time.sleep(.5) # move away to unblock rune purple dot
                        #         if self.runesolver.runechecker(self.g): # if rune not solved for some reason
                        #             pass # attempt solve rune again in the next loop
                        #         else:
                        #             runetimer0=perf_counter() # reset
                        cctimer=now-cctimer0
                        if cctimer>3000: # 60sec * 50min = 3000sec
                            # cc=True
                            keyupall()
                            await self.changechannel()
                            cctimer0=perf_counter() # reset
                            self.cc=False
                        if self.cc:
                            keyupall()
                            await self.changechannel_zakum() # this version of changing channel is from reddotdetector. 
                            self.cc=False                            
                        runetimer=now-runetimer0
                        if runetimer > self.runecd:
                            if not await self.FindRuneCDIcon():
                                await self.character.gotorune() # and solve rune.
                            runetimer0=now
                print(f'script finished. {self.script} ..')

    async def adjustcharacter(self,a=10,b=10):
        xynotfound=0
        while True:
            if self.scriptpausesignal:
                keyupall()
                return
            g_variable = self.g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            if x == None or y == None:
                xynotfound+=1
                if xynotfound > 50:
                    t = time.localtime()
                    currenttime = time.strftime("%H:%M:%S", t)
                    print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                    return
                print(f'x==None, pass ..')
                time.sleep(.1)      
            else:
                xynotfound=0
                if x >=a-2 and x<=a+2:
                    pass
                    if y>=b-2 and y<=b+2:
                        return
                    else:                        
                        if y > b:
                            await self.character.ac.goupattack()
                        elif y < b:
                            await self.character.ac.godownattack()
                else:
                    if x > a+30:
                        await self.character.ac.goleftattack()
                    elif x < a-30:
                        await self.character.ac.gorightattack()
                    elif x > a:
                        await self.character.ac.leftwalk(int((abs(x-a)*40)-30),int((abs(x-a)*40)))
                    elif x < a:
                        await self.character.ac.rightwalk(int((abs(x-a)*40)-30),int((abs(x-a)*40)))

    def realrecord(self):
        self.unreleased_keys=[]
        self.input_events=[]
        def on_press(key):
            if key in self.unreleased_keys: 
                print(f'unreleased: {key=} {self.unreleased_keys=}')
                return
            else:
                self.unreleased_keys.append(key)
            try:
                print(f'{key=}')
                record_event('keyDown', elapsed_time(), key.char)
            except AttributeError:
                record_event('keyDown', elapsed_time(), key)
        def on_release(key):
            try:
                self.unreleased_keys.remove(key)
            except ValueError:
                print('ERROR: {} not in unreleased_keys'.format(key))
            try:
                record_event('keyUp', elapsed_time(), key.char)
            except AttributeError:
                record_event('keyUp', elapsed_time(), key)
            if key == keyboard.Key.esc:
                self.recordstatus=not self.recordstatus
                self.record_button.configure(fg_color='#55eecc', text='Record',state='normal')
                self.signature=''
                for value in self.input_events:
                    print(value)
                    if value['type']=='keyUp':
                        if 'Key' in value['button']:
                            self.signature+=value['button'].replace('Key','')
                        else:
                            self.signature+='.'+value['button']
                length=round(self.input_events[-1]['time'],4)
                self.labelscript.configure(text=f'script duration: {length}')
                new_array_temp=[]
                for index, action in enumerate(self.input_events):
                    button = action['button']
                    key = self.convertKey(button)
                    if key is not None:
                        self.input_events[index]['button'] = key
                        if key == 'esc':
                            pass
                        else:
                            new_array_temp.append(action)
                self.input_events=new_array_temp            
                raise keyboard.Listener.StopException
        def record_event(event_type, event_time, button, pos=None):
            self.input_events.append({
                'time': event_time,
                'type': event_type,
                'button': str(button),
                'pos': pos
            })            
        def elapsed_time():
            return perf_counter() - self.start_time
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            self.start_time = perf_counter()
            listener.join()

    def convertKey(self,button=None):
        PYNPUT_SPECIAL_CASE_MAP = {
            'alt_l': 'altleft',
            'alt_r': 'altright',
            'alt_gr': 'altright',
            'caps_lock': 'capslock',
            'ctrl_l': 'ctrlleft',
            'ctrl_r': 'ctrlright',
            'page_down': 'pagedown',
            'page_up': 'pageup',
            'shift_l': 'shiftleft',
            'shift_r': 'shiftright',
            'num_lock': 'numlock',
            'print_screen': 'printscreen',
            'scroll_lock': 'scrolllock',
        }
        # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
        cleaned_key = button.replace('Key.', '')
        if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
            return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]
        return cleaned_key

    def setup_tab3(self):
        input_fields = []
        def on_entry_click1(event):
            entry = event.widget
            if entry.get() == 'x1':
                entry.delete(0, tk.END)
                entry.config(fg='black')
        def on_entry_leave1(event):
            entry = event.widget
            if not entry.get():
                entry.insert(0, 'x1')
                entry.config(fg='gray')
        def on_entry_click2(event):
            entry = event.widget
            if entry.get() == 'x2':
                entry.delete(0, tk.END)
                entry.config(fg='black')
        def on_entry_leave2(event):
            entry = event.widget
            if not entry.get():
                entry.insert(0, 'x2')
                entry.config(fg='gray')
        def on_entry_click3(event):
            entry = event.widget
            if entry.get() == 'y':
                entry.delete(0, tk.END)
                entry.config(fg='black')
        def on_entry_leave3(event):
            entry = event.widget
            if not entry.get():
                entry.insert(0, 'y')
                entry.config(fg='gray')
        def bind_entry_events(entry, placeholder_text,on_entry_click, on_entry_leave, loader=False):
            entry.insert(0, placeholder_text)
            entry.bind('<FocusIn>', on_entry_click)
            entry.bind('<FocusOut>', on_entry_leave)            
            entry.config(fg='black') if loader else entry.config(fg='gray')
        def add_input_field(loader=False, data=None):
            new_label = tk.Label(self.framedesign2, anchor='w', justify='left', text=f"platform {len(input_fields)+1}: ")
            new_label.grid(row=len(input_fields), column=0, padx=1, pady=1, sticky='w')
            new_entry = tk.Entry(self.framedesign2, width=5, justify='right')
            new_entry.grid(row=len(input_fields), column=1, padx=1, pady=1)
            bind_entry_events(new_entry, data[0] if data else 'x1', on_entry_click1, on_entry_leave1, loader)
            new_entry2 = tk.Entry(self.framedesign2, width=5, justify='right')
            new_entry2.grid(row=len(input_fields), column=2, padx=1, pady=1)
            bind_entry_events(new_entry2, data[1] if data else 'x2', on_entry_click2, on_entry_leave2, loader)
            new_entry3 = tk.Entry(self.framedesign2, width=5, justify='right')
            new_entry3.grid(row=len(input_fields), column=3, padx=(10,1), pady=1)
            bind_entry_events(new_entry3, data[2] if data else 'y', on_entry_click3, on_entry_leave3, loader)
            input_fields.append([new_label,new_entry,new_entry2,new_entry3])
        def minus_input_field():
            if input_fields:
                last_row = input_fields.pop()
                for widget in last_row:
                    widget.destroy()
        def get_current_position():
            g_variable = self.g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            self.labelcurrentpos.config(text=f'{x,y}')
        self.frameprofile = tk.Frame(self.tab3, bg='#71f243', bd=0)
        self.frameprofile.pack(padx=1, pady=1)
        def new_profile():
            profile_name = simpledialog.askstring("New Profile", "Enter the name for the new profile:")
            if profile_name:
                json_file_names.append(profile_name)
                comboboxclasstype.set(json_file_names[len(json_file_names)-1])
                comboboxclasstype['values'] = json_file_names                
                for i in range(len(input_fields)):
                    minus_input_field()
        buttonnewprofile = tk.Button(self.frameprofile, text="new", command=new_profile, anchor='w')
        buttonnewprofile.pack(side=tk.LEFT, padx=1, pady=1)
        def on_select(event):
            self.profile = comboboxclasstype.get()
        folder_path = "json"
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith(".json")]
        json_file_names = [os.path.splitext(file)[0] for file in json_files]
        comboboxclasstype = ttk.Combobox(self.frameprofile, values=json_file_names, state="readonly", width=17)
        comboboxclasstype.pack(side=tk.LEFT, padx=1, pady=1)
        comboboxclasstype.set(json_file_names[json_file_names.index(self.profile)])
        comboboxclasstype.bind("<<ComboboxSelected>>", on_select)
        def load_profile():
            for i in range(len(input_fields)):
                minus_input_field()
            self.profile = comboboxclasstype.get()
            try:
                with open(f'json/{self.profile}.json', 'r') as json_file:
                    arrays = json.load(json_file)
                for array in arrays:
                    add_input_field(loader=True,data=array)
            except Exception as e:
                print(f'reading json2: {e=}')
        buttonnewprofile = tk.Button(self.frameprofile, text="load", command=load_profile, anchor='w')
        buttonnewprofile.pack(side=tk.LEFT, padx=1, pady=1)
        self.framebuttonxy = tk.Frame(self.tab3, bg='#71f243', bd=0)
        self.framebuttonxy.pack(padx=1, pady=1)
        self.buttoncurrentpos = tk.Button(self.framebuttonxy, text="get current position", command=get_current_position, anchor='w')
        self.buttoncurrentpos.pack(side=tk.LEFT, padx=1, pady=1)
        self.labelcurrentpos = tk.Label(self.framebuttonxy, anchor='w', justify='left', text=f"(0,0)")
        self.labelcurrentpos.pack(side=tk.LEFT, padx=1, pady=1)
        self.framebuttonadd = tk.Frame(self.tab3, bg='#71f243', bd=0)
        self.framebuttonadd.pack(padx=1, pady=1)
        self.buttondesign = tk.Button(self.framebuttonadd, text="new platform", command=add_input_field)
        self.buttondesign.pack(side=tk.LEFT, padx=1, pady=1)
        self.buttondesign2 = tk.Button(self.framebuttonadd, text="minus platform", command=minus_input_field)
        self.buttondesign2.pack(side=tk.LEFT, padx=1, pady=1)
        self.framedesign2 = tk.Frame(self.tab3, bg='#f132b3', bd=0)
        self.framedesign2.pack(padx=0, pady=0)
        self.framedesign3 = tk.Frame(self.tab3, bg='#a16213', bd=0)
        self.framedesign3.pack(padx=0, pady=0)
        def saveprofile():
            platforms = []
            for input_field in input_fields:
                entry, entry2, entry3 = input_field[1].get(), input_field[2].get(), input_field[3].get()
                platforms.append([entry, entry2, entry3])
            self.profile = comboboxclasstype.get()
            with open(f'json/{self.profile}.json', 'w') as json_file:
                json.dump(platforms, json_file, indent=4)
            # print(f'saved platform. ')
        self.buttonsaveprofile = tk.Button(self.framedesign3, text="Save", command=saveprofile, state=tk.NORMAL)
        self.buttonsaveprofile.grid(row=0, column=0, pady=2, padx=2, sticky='nsew')
        load_profile()




    def setup_tab4(self):
        # frametelegram = tk.Frame(tab4, bg='#a1b2c3', bd=0)
        self.frametelegram = tk.Frame(self.tab4, bg='#f1f2f3', bd=0)
        self.frametelegram.pack(padx=0, pady=0)
        self.labeltoken = tk.Label(self.frametelegram, anchor='w', justify='left', text="Token: ")
        self.labeltoken.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        self.entrytoken = tk.Entry(self.frametelegram, width=50)
        self.entrytoken.insert(0, self.TOKEN)
        self.entrytoken.grid(row=0, column=1, padx=1, pady=1)
        self.labelchatid = tk.Label(self.frametelegram, anchor='w', justify='left', text="Chat ID: ")
        self.labelchatid.grid(row=1, column=0, padx=1, pady=1)
        self.labelchatid2 = tk.Label(self.frametelegram, anchor='w', justify='left', text=self.chat_id)
        self.labelchatid2.grid(row=1, column=1, padx=1, pady=1, sticky='w')
        message = ""
        buttondisabled=False
        if not self.acc_not_bind:
        # if self.TOKEN != '0' and self.chat_id != '0':
            # message += f"Your bot token is: {TOKEN} \n Your telegram chat_id is {chat_id} \n Account is binded with this program. If you can't receive bot message, "
            message += f"Account is binded with this program. \nIf you can't receive bot message, \n"
            buttondisabled=True
        else:
            # if self.TOKEN == '0':
            #     message += f"Bot TOKEN not found. \n"
            # if self.chat_id == '0':
            #     message += f'Telegram account not binded. \n'
            message += f'Telegram account not binded, \n'
            pass
        message += "kindly rebind your account. \n1. Create your telegram bot at BotFather. \n2. Paste your telegram bot token here. \n3. Search your telegram bot name on telegram. \
            \n4. Type something in that telegram bot. \n5. Press bind button below. "
        self.labelmessage = tk.Label(self.frametelegram, anchor='w', justify='left', text=message)
        self.labelmessage.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
        self.labelmessage2 = tk.Label(self.frametelegram, anchor='w', justify='left', text="")
        self.labelmessage2.grid(row=3, column=0, columnspan=2, padx=1, pady=1)
        self.framebutton = tk.Frame(self.frametelegram, bg='#f1f2f3', bd=0)
        self.framebutton.grid(row=4, column=0, columnspan=2, pady=1)
        self.buttonbind = tk.Button(self.framebutton, text="bind", command=self.get_token, anchor='w')
        self.buttonbind.grid(row=0, column=0, pady=1, padx=1)
        self.buttonrebind = tk.Button(self.framebutton, text="rebind", command=self.rebind)
        self.buttonrebind.grid(row=0, column=1, pady=1, padx=1)
        if buttondisabled:
            self.buttonbind.config(state=tk.DISABLED)
        else:
            self.buttonrebind.config(state=tk.DISABLED)

        # stucked alert
        # white text alert
        # red dot alert
        # framecommands = tk.Frame(tab4, bg='#91a2b3', bd=0)
        self.framecommands = tk.Frame(self.tab4, bg='#f1f2f3', bd=0)
        self.framecommands.pack(padx=0, pady=(20,20))
        self.labelcommands = tk.Label(self.framecommands, text='below you can test each telegram bot command')
        self.labelcommands.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.buttonpause = tk.Button(self.framecommands, text="Pause", height=2, bg='#a1f2f3', command=self.telegrampause, state=tk.DISABLED)
        self.buttonpause.grid(row=1, column=0, pady=2, padx=2, sticky='nsew')
        self.buttontown = tk.Button(self.framecommands, text="Town", height=2, bg='#91f2f3', command=self.telegramtown, state=tk.DISABLED)
        self.buttontown.grid(row=1, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonmessage = tk.Button(self.framecommands, text="Message", height=2, bg='#81f2f3', command=self.telegrammessage, state=tk.NORMAL)
        self.buttonmessage.grid(row=2, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonstatus = tk.Button(self.framecommands, text="Status", height=2, bg='#71f2f3', command=self.telegramstatus)
        self.buttonstatus.grid(row=2, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonstop = tk.Button(self.framecommands, text="Stop", height=2, bg='#61f2f3', command=self.telegramstop, state=tk.DISABLED)
        self.buttonstop.grid(row=3, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonresume = tk.Button(self.framecommands, text="Resume", height=2, bg='#51f2f3', command=self.telegramresume, state=tk.DISABLED)
        self.buttonresume.grid(row=3, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonenable = tk.Button(self.framecommands, text="Enable", height=2, bg='#41f2f3', command=self.telegramenable, state=tk.DISABLED)
        self.buttonenable.grid(row=4, column=0, pady=2, padx=2, sticky='nsew')
        self.buttondisable = tk.Button(self.framecommands, text="Disable", height=2, bg='#31f2f3', command=self.telegramdisable, state=tk.DISABLED)
        self.buttondisable.grid(row=4, column=1, pady=2, padx=2, sticky='nsew')
        self.buttoncc = tk.Button(self.framecommands, text="CC", height=2, bg='#21f2f3', command=self.telegramcc, state=tk.DISABLED)
        self.buttoncc.grid(row=5, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonshutdown = tk.Button(self.framecommands, text="Shut Down", height=2, bg='#11f2f3', command=self.telegramshutdown, state=tk.DISABLED)
        self.buttonshutdown.grid(row=5, column=1, pady=2, padx=2, sticky='nsew')


    def setup_tab5(self):
        frametab41 = customtkinter.CTkFrame(self.tab5)
        frametab41.pack(padx=1, pady=(1,1))
        position = win32gui.GetWindowRect(self.maplehwnd)
        x0, y0, w, h = position
        self.autoclickerstop=False
        # self.monsternumber=20
        # self.repeatcount=floor(100/self.monsternumber)
        # self.cboxslot=199
        # self.monsterslot=539
        def autoclicker():
            self.autoclickerstop=False
            self.thread10 = threading.Thread(target=self.run_thread10)
            self.thread10.start()
            while True:
                if self.autoclickerstop:
                    print(f'{self.autoclickerstop=}')
                    self.thread10.join()
                    return
                self.helper.movetoandclick(x0+878,y0+760) # click shop 878,760
                for j in range(14):
                    for i in range(14):
                        if self.autoclickerstop:
                            print(f'{self.autoclickerstop=}')
                            self.thread10.join()
                            return
                        else:
                            self.helper.movetoandclick(x0+697,y0+418) # click buy --> enter --> enter 697,418                            
                            self.character.ac.enterpr_special(3,11)
                            time.sleep(.005)
                            self.character.ac.enterpr_special(3,11)
                            time.sleep(.005)
                time.sleep(.1)
                self.character.ac.enterpr_special(3,11)
                time.sleep(.1) # just to be safe. 
                self.character.ac.enterpr_special(3,11)
                time.sleep(.1)
                self.helper.movetoandclick(x0+996,y0+754) # click return to farm 996,754
                for j in range(self.repeatcount):
                    self.helper.movetoandclick(x0+154,y0+669) # click decorate farm 154,669
                    time.sleep(.1) # double click to ensure it click
                    self.helper.movetoandclick(x0+154,y0+669) # click decorate farm 154,669
                    for i in range(round(self.monsternumber+self.monsternumber*1.7)):
                        if self.autoclickerstop:
                            print(f'{self.autoclickerstop=}')
                            self.thread10.join()
                            return
                        else:
                            self.helper.movetoandclick(x0+self.cboxslot,y0+719) # click c box --> enter --> enter 136 199 277 350 419,719
                            self.character.ac.enterpr_special(3,11)
                            self.character.ac.enterpr_special(3,11)
                    self.helper.movetoandclick(x0+77,y0+292) # click auto take care  --> enter 77,292
                    time.sleep(.033)
                    self.helper.movetoandclick(x0+77,y0+292) # click auto take care  --> enter 77,292 # double click to ensure
                    time.sleep(.033)
                    self.character.ac.enterpr_special()
                    time.sleep(.013)
                    self.character.ac.enterpr_special()
                    time.sleep(.033)
                    self.character.ac.enterpr_special() # triple enter to ensure
                    time.sleep(.033)
                    self.helper.movetoandclick(x0+69,y0+665) # click my monster 69,665
                    for i in range(self.monsternumber):
                        if self.autoclickerstop:
                            print(f'{self.autoclickerstop=}')
                            self.thread10.join()
                            return
                        else:
                            self.helper.movetoandrclick(x0+self.monsterslot,y0+726,duration=.05) # right click monster 155 243 312 377 456 539,726                            
                            self.character.ac.enterpr_special(3,11)
                            time.sleep(.050)
                            self.character.ac.enterpr_special(3,11)
                            time.sleep(.100)
                            right_click()
                            time.sleep(.150)
                            self.helper.movetoandclick(x0+self.monsterslot,y0+597,duration=.1,sleep=.1) # click discharge 155 243 312 377 456 539,597
                            self.helper.movetoandclick(x0+492,y0+453,duration=.1,sleep=.1) # click the tick --> enter 492,453
                            time.sleep(.08) # server lag
                        self.character.ac.enterpr_special(3,11)
                        time.sleep(.08) # server lag
                    self.character.ac.enterpr_special(3,11)
                    time.sleep(.08) # server lag
                    self.character.ac.enterpr_special(3,11)
                    time.sleep(.08) # server lag
        autoclickerbutton = customtkinter.CTkButton(frametab41, text="autoclicker GO!", command=autoclicker)
        autoclickerbutton.pack(padx=(1,1),pady=(1,1))
        frametab42 = customtkinter.CTkFrame(self.tab5)
        frametab42.pack(padx=1, pady=(1,1))
        labelmonsternumber = customtkinter.CTkLabel(frametab42,text='how many monster slot?')
        labelmonsternumber.pack(padx=(1,1),pady=(1,1))
        inputmonsternumber = customtkinter.CTkEntry(frametab42, placeholder_text='20')
        inputmonsternumber.pack(padx=(1,1),pady=(1,1))
        labelcboxslot = customtkinter.CTkLabel(frametab42,text='CGrade Mob Box slot (1/2/3/4/5):')
        labelcboxslot.pack(padx=(1,1),pady=(1,1))
        inputcboxslot = customtkinter.CTkEntry(frametab42, placeholder_text='2')
        inputcboxslot.pack(padx=(1,1),pady=(1,1))
        labelmonsterslot = customtkinter.CTkLabel(frametab42,text='which monster slot to discharge (2/3/4/5/6/7)?')
        labelmonsterslot.pack(padx=(1,1),pady=(1,1))
        inputmonsterslot = customtkinter.CTkEntry(frametab42, placeholder_text='7')
        inputmonsterslot.pack(padx=(1,1),pady=(1,1))
        def resetmaple():
            position = win32gui.GetWindowRect(self.maplehwnd)
            x0, y0, w, h = position
            tempmonsternumber=inputmonsternumber.get()
            if tempmonsternumber.isnumeric():
                self.monsternumber=int(tempmonsternumber)
                self.repeatcount=floor(100/self.monsternumber)
            tempcboxslot=inputcboxslot.get()
            if tempcboxslot.isnumeric():
                tempcboxslot=int(tempcboxslot)
                if tempcboxslot >= 1 and tempcboxslot <= 5:
                    if tempcboxslot==1:
                        self.cboxslot=136 # 136 199 277 350 419,
                    elif tempcboxslot==2:
                        self.cboxslot=199 # 136 199 277 350 419,
                    elif tempcboxslot==3:
                        self.cboxslot=277 # 136 199 277 350 419,
                    elif tempcboxslot==4:
                        self.cboxslot=350 # 136 199 277 350 419,
                    elif tempcboxslot==5:
                        self.cboxslot=419 # 136 199 277 350 419,
            tempinputmonsterslot=inputmonsterslot.get()
            if tempinputmonsterslot.isnumeric():
                tempinputmonsterslot=int(tempinputmonsterslot)
                if tempinputmonsterslot >= 2 and tempinputmonsterslot <= 7:
                    if tempinputmonsterslot == 2:
                        self.monsterslot=155 # 155 243 312 377 456 539
                    elif tempinputmonsterslot == 3:
                        self.monsterslot=243 # 155 243 312 377 456 539
                    elif tempinputmonsterslot == 4:
                        self.monsterslot=312 # 155 243 312 377 456 539
                    elif tempinputmonsterslot == 5:
                        self.monsterslot=377 # 155 243 312 377 456 539
                    elif tempinputmonsterslot == 6:
                        self.monsterslot=456 # 155 243 312 377 456 539
                    elif tempinputmonsterslot == 7:
                        self.monsterslot=539 # 155 243 312 377 456 539
            print(f'number={self.monsternumber} cslot={tempcboxslot} mslot={tempinputmonsterslot}')
        self.monsternumber=20
        self.repeatcount=floor(100/self.monsternumber)
        self.cboxslot=199
        self.monsterslot=456
        resetmaplebutton = customtkinter.CTkButton(frametab42, text="set all variable to current value", command=resetmaple)
        resetmaplebutton.pack(padx=(1,1),pady=(10,1))


    async def autoclicker(self):
        def on_press(key):
            pass
        def on_release(key):
            if key == keyboard.Key.esc:
                print(f'esc {self.autoclickerstop=}')
                self.autoclickerstop=True
                raise keyboard.Listener.StopException
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            listener.join()

    def setup_tab6(self):
        self.framesettings = tk.Frame(self.tab6, bg='#f1f2f3', bd=0)
        self.framesettings.pack(padx=0, pady=0)
        self.labelipaddress = tk.Label(self.framesettings, anchor='w', justify='left', text="runesolver ip address: ")
        self.labelipaddress.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        self.entryipaddress = tk.Entry(self.framesettings)
        self.entryipaddress.insert(0, self.ipaddress)
        self.entryipaddress.grid(row=0, column=1, padx=1, pady=1)
        self.labelatt = tk.Label(self.framesettings, anchor='w', justify='left', text="main att key: ")
        self.labelatt.grid(row=1, column=0, padx=1, pady=1, sticky='w')
        self.entryatt = tk.Entry(self.framesettings)
        self.entryatt.insert(0, self.att)
        self.entryatt.grid(row=1, column=1, padx=1, pady=1)
        self.labeljump = tk.Label(self.framesettings, anchor='w', justify='left', text="jump key: ")
        self.labeljump.grid(row=2, column=0, padx=1, pady=1, sticky='w')
        self.entryjump = tk.Entry(self.framesettings)
        self.entryjump.insert(0, self.jump)
        self.entryjump.grid(row=2, column=1, padx=1, pady=1)
        self.labelteleport = tk.Label(self.framesettings, anchor='w', justify='left', text="teleport key: ")
        self.labelteleport.grid(row=3, column=0, padx=1, pady=1, sticky='w')
        self.entryteleport = tk.Entry(self.framesettings)
        self.entryteleport.insert(0, self.teleport)
        self.entryteleport.grid(row=3, column=1, padx=1, pady=1)
        self.labelropeconnect = tk.Label(self.framesettings, anchor='w', justify='left', text="ropeconnect key: ")
        self.labelropeconnect.grid(row=4, column=0, padx=1, pady=1, sticky='w')
        self.entryropeconnect = tk.Entry(self.framesettings)
        self.entryropeconnect.insert(0, self.ropeconnect)
        self.entryropeconnect.grid(row=4, column=1, padx=1, pady=1)
        self.labelnpc = tk.Label(self.framesettings, anchor='w', justify='left', text="npc key: ")
        self.labelnpc.grid(row=5, column=0, padx=1, pady=1, sticky='w')
        self.entrynpc = tk.Entry(self.framesettings)
        self.entrynpc.insert(0, self.npc)
        self.entrynpc.grid(row=5, column=1, padx=1, pady=1)
        self.labelfountainkey = tk.Label(self.framesettings, anchor='w', justify='left', text="fountainkey: ")
        self.labelfountainkey.grid(row=6, column=0, padx=1, pady=1, sticky='w')
        self.entryfountainkey = tk.Entry(self.framesettings)
        self.entryfountainkey.insert(0, self.fountainkey)
        self.entryfountainkey.grid(row=6, column=1, padx=1, pady=1)
        self.labelclasstype = tk.Label(self.framesettings, anchor='w', justify='left', text="classtype: ")
        self.labelclasstype.grid(row=7, column=0, padx=1, pady=1, sticky='w')        
        def on_select(event):
            self.classtype = self.comboboxclasstype.get()       
        folder_path = "classtype"
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith(".py")]
        json_file_names = [os.path.splitext(file)[0] for file in json_files]
        self.comboboxclasstype = ttk.Combobox(self.framesettings, values=json_file_names, state="readonly", width=17)
        self.comboboxclasstype.grid(row=7, column=1, padx=1, pady=1)
        self.comboboxclasstype.set(json_file_names[json_file_names.index(self.classtype)])
        self.comboboxclasstype.bind("<<ComboboxSelected>>", on_select)
        self.labelportal = tk.Label(self.framesettings, anchor='w', justify='left', text="portal: (ignore this)")
        self.labelportal.grid(row=8, column=0, padx=1, pady=1, sticky='w')
        def on_checkbox_clicked():
            self.portaldisabled=False if checkboxvar.get() else True
        checkboxvar = tk.BooleanVar(value=False) if self.portaldisabled else tk.BooleanVar(value=True)
        self.checkboxportal = tk.Checkbutton(self.framesettings, text="", variable=checkboxvar, command=on_checkbox_clicked, font=('Arial', 10)) ## not sure bout this
        self.checkboxportal.grid(row=8, column=1, padx=0, pady=0, sticky='w')

        framesettings3 = customtkinter.CTkFrame(self.tab6)
        framesettings3.pack(padx=2, pady=(2,2))
        labelbroid = customtkinter.CTkLabel(framesettings3, anchor='w', justify='left', text='battle-roid: ')
        labelbroid.grid(row=0,column=0,padx=1,pady=1,sticky='w')
        def cbbroidclicked():
            self.broiddisabled=False if cbbroidvar.get() else True
        cbbroidvar=tk.BooleanVar(value=False) if self.broiddisabled else tk.BooleanVar(value=True)
        checkboxbroid = customtkinter.CTkCheckBox(framesettings3, text='', variable=cbbroidvar, command=cbbroidclicked, font=('Arial', 10))
        checkboxbroid.grid(row=0, column=1, padx=0, pady=0, sticky='w')

        self.labelrunecd = tk.Label(framesettings3, anchor='w', justify='left', text="check rune every: ")
        self.labelrunecd.grid(row=1, column=0, padx=1, pady=1, sticky='w')
        self.entryrunecd = tk.Entry(framesettings3)
        self.entryrunecd.insert(0, self.runecd)
        self.entryrunecd.grid(row=1, column=1, padx=1, pady=1)


        self.framesettings2 = tk.Frame(self.tab6, bg='#f1f2f3', bd=0)
        self.framesettings2.pack(padx=0, pady=(20,20))
        self.buttonsave = tk.Button(self.framesettings2, text="Save", command=self.settingssave, state=tk.NORMAL)
        self.buttonsave.grid(row=0, column=0, pady=2, padx=2, sticky='nsew')

    def settingssave(self):
        self.config.set('main', 'ipaddress', str(self.entryipaddress.get()))
        self.config.set('keybind', 'attack', str(self.entryatt.get()))
        self.config.set('keybind', 'jump', str(self.entryjump.get()))
        self.config.set('keybind', 'teleport', str(self.entryteleport.get()))
        self.config.set('keybind', 'ropeconnect', str(self.entryropeconnect.get()))
        self.config.set('keybind', 'npc', str(self.entrynpc.get()))
        self.config.set('keybind', 'fountainkey', str(self.entryfountainkey.get()))
        self.config.set('keybind', 'classtype', str(self.comboboxclasstype.get()))
        self.config.set('main', 'portaldisabled', str(self.portaldisabled))
        self.config.set('main', 'broiddisabled', str(self.broiddisabled))
        self.config.set('main', 'runecd', str(self.entryrunecd.get()))
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        self.character.setup(
            left=self.line_position_slider.get()/2,
            right=self.line_position_slider2.get()/2,
            top=self.line_position_slider3.get()/2,
            btm=self.line_position_slider4.get()/2,
            classtype=self.classtype,
            runesolver=self.runesolver,
            g=self.g,
            rotation=self.rotation,
            maplehwnd=self.maplehwnd
        )
        self.character.refreshkeybind()
        self.runecd=int(self.entryrunecd.get())
        self.rotation='default'
        rotation_list = self.character.get_rotation_list()
        self.comboboxrotation.configure(values=rotation_list)
        self.comboboxrotation.set(rotation_list[rotation_list.index(self.rotation)])

    def rebind(self):
        self.entrytoken.delete(0,tk.END)
        self.labelchatid2.config(text='')
        self.labelmessage.config(text='telegram bot resetted. \nkindly rebind your telegram bot. \n1. Create your telegram bot at BotFather. \n2. Paste your telegram bot token here. \n3. Search your telegram bot name on telegram. \
        \n4. Type something in that telegram bot. \n5. Press bind button below. ')
        self.buttonbind.config(state=tk.NORMAL)
        self.buttonrebind.config(state=tk.DISABLED)
    
    def get_token(self):
        token = self.entrytoken.get()
        # print("Token:", token)
        if token == '0':
            return
        response = requests.get('https://api.telegram.org/bot'+token+'/getUpdates')
        if response.status_code == 200:
            # Parse and print the JSON content
            json_data = response.json()
            # print(f'{json_data=}')
            # formated = json.dumps(json_data, indent=2)
            # print("Returned JSON:")
            # print(formated)
            if json_data['result']:
                chat_id = json_data['result'][0]['message']['chat']['id']
                # print(f'{chat_id = }')
                # 6871179594:AAH6ZiIEPyfmGQhgGp1bsCy3PvhA42rtyfk
                img = self.g.get_screenshot()
                # print(f'{type(img)}')
                payload = {
                    'chat_id': chat_id,
                    'photo': 'https://picsum.photos/200/300',
                    'caption': 'dummy photo'
                }
                response = requests.post('https://api.telegram.org/bot'+token+'/sendPhoto', data=payload)
                if response.status_code == 200:
                    msg = 'telegram bot binded with account successfully. \nnow you can use various functions available to your bot. \nstay safe. enjoy.'
                    self.labelchatid2.config(text=chat_id)
                    self.labelmessage.config(text=msg)
                    self.labelmessage2.config(text='')
                    self.buttonbind.config(state=tk.DISABLED)
                    self.buttonrebind.config(state=tk.NORMAL)
                    self.TOKEN = token
                    self.chat_id = chat_id
                else:
                    print(f"Request failed with status code_: {response.status_code}")
            else:
                msg = "type something or press /start in the telegram bot to start binding. "
                self.labelmessage2.config(text=msg)
                # labelmessage.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                print(f'type something or press /start in the telegram bot to start binding. ')
        else:
            print(f"Request failed with status code: {response.status_code}")

    def telegrampause(self):
        print(f'telegrampause')
        pass

    def telegramtown(self):
        print(f'telegramtown')
        pass

    def telegrammessage(self):
        print(f'telegrammessage')
        if not self.chathwnd:
            print(f'chat window not found')
            if not self.rebindchathwnd():
                return
            print(f'chat window found')
        now = perf_counter()
        photo0 = self.g.get_screenshot()
        position = win32gui.GetWindowRect(self.chathwnd)
        x, y, w, h = position
        # print(f'{x} {y} {w} {h}')
        screenshot = ImageGrab.grab(position)
        screenshot2 = np.array(screenshot)
        img = cv2.cvtColor(screenshot2, cv2.COLOR_RGB2BGR)
        imgchat=img[530:777,:400]
        imgmega=img[220:369,:400]
        # print(f'{imgchat.shape[0]=} {imgchat.shape[1]=} {photo0.shape=} {img.shape=}')
        # print(f'{imgmega.shape[0]=} {imgmega.shape[1]=} {y=} {h=}')
        photo0 = photo0[:,:,:3]
        photo0[photo0.shape[0]-imgchat.shape[0]:photo0.shape[0],:imgchat.shape[1]] = imgchat
        photo0[photo0.shape[0]-imgmega.shape[0]:photo0.shape[0],photo0.shape[1]-imgmega.shape[1]:photo0.shape[1]] = imgmega
        # cv2.imshow('photo0', photo0)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imshow('imgchat', imgchat)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imshow('imgmega', imgmega)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # chatposition2 = (x,y+200,w-15,h-400)
        # screenshot = ImageGrab.grab(chatposition2)
        # screenshot2 = np.array(screenshot)
        # img = cv2.cvtColor(screenshot2, cv2.COLOR_RGB2BGR)
        # photo0[photo0.shape[0]-img.shape[0]:photo0.shape[0],photo0.shape[1]-img.shape[1]:photo0.shape[1]] = img
        # cv2.imshow('photo0', photo0)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        height, width = img.shape[0], img.shape[1]
        success, photo0_encoded = cv2.imencode('.png', photo0)
        photo0_bytes = photo0_encoded.tobytes()
        files = {'photo': photo0_bytes}
        payload = {
            'chat_id': self.chat_id,
            # 'photo': 'https://picsum.photos/200/300',
            'caption': 'dummy photo test'
        }
        response = requests.post('https://api.telegram.org/bot'+self.TOKEN+'/sendPhoto', data=payload, files=files)
        if response.status_code == 200:
            print(f'{perf_counter()-now =}')
            print(f"success {response.json().get('description')}")
            print(f"success {response.json()}")
        else:
            print(f"Request failed with status code_: {response.status_code}")
            print(f"{response.json().get('description')}")

    def telegramstatus(self):
        print(f'telegramstatus')
        now = perf_counter()
        photo0 = self.g.get_screenshot()
        # photo = g.get_screenshot_bytes()        
        # photo3 = Image.open('minimap.PNG')
        # photo2 = ''
        # with open('minimap.png', 'rb') as f:
        #     photo2 = f.read()
        # photo4 = cv2.imread('minimap.png')
        # success, photo4_encoded = cv2.imencode('.png', photo4)
        # photo4_bytes = photo4_encoded.tobytes()
        success, photo0_encoded = cv2.imencode('.png', photo0)
        photo0_bytes = photo0_encoded.tobytes()
        # print(f'{type(photo)=} {sys.getsizeof(photo)}')
        # print(f'{type(photo2)=}')
        # print(f'{type(photo3)=}')
        # print(f'{type(photo0)=}')
        # print(f'{photo0=}')
        # print(f'{type(photo4)=}')
        # print(f'{photo4=}')
        # print(f'{type(photo4_encoded)=}')
        # print(f'{type(photo4_bytes)=}')
        # print(f'telegrampause')
        # print(f'{photo=}')
        # print(f'{photo2=}')
        # photo_encode = photo.encode('utf-8')
        # photo2_encode = photo2.encode('utf-8')
        # binary_data = b'\x48\x65\x6C\x6C\x6F\x2C\x20\x57\x6F\x72\x6C\x64\x21'
        # with open('photo.bin', 'wb') as file:
        #     file.write(binary_data)
        # with open('photo2.txt', 'wb') as file:
        #     file.write(binary_data)
        # image2 = Image.open(BytesIO(photo2))
        # image2.show()
        # image = Image.open(BytesIO(photo))
        # image.show()
        # image0 = Image.fromarray(photo0)
        # image0.show()
        files = {'photo': photo0_bytes}
        payload = {
            'chat_id': self.chat_id,
            # 'photo': 'https://picsum.photos/200/300',
            'caption': 'dummy photo test'
        }
        response = requests.post('https://api.telegram.org/bot'+self.TOKEN+'/sendPhoto', data=payload, files=files)
        # response = requests.post('https://api.telegram.org/bot'+TOKEN+'/sendPhoto', params=payload, files=files)
        if response.status_code == 200:
            print(f'{perf_counter()-now =}')
            print(f"success {response.json().get('description')}")
            print(f"success {response.json()}")
        else:
            print(f"Request failed with status code_: {response.status_code}")
            print(f"{response.json().get('description')}")
        pass

    def telegramstop(self):
        print(f'telegramstop')
        pass

    def telegramresume(self):
        print(f'telegramresume')
        pass

    def telegramenable(self):
        print(f'telegramenable')
        pass

    def telegramdisable(self):
        print(f'telegramdisable')
        pass

    def telegramcc(self):
        print(f'telegramcc')
        pass

    def telegramshutdown(self):
        print(f'telegramshutdown')
        pass
    
    def on_close(self):
        print("\nBumblebee Bot window is closing .. waiting threads to join ..")
        self.pause=True
        self.scriptpausesignal=True
        self.config.set('main', 'profile', str(self.profile))
        self.config.set('main', 'preset', str(self.preset))
        self.config.set('main', 'script', str(self.script))
        self.config.set('main', 'rotation', str(self.rotation))
        self.config2.set('telegram', 'token', str(self.TOKEN))
        self.config2.set('telegram', 'chat_id', str(self.chat_id))
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        with open('secret/secret.ini', 'w') as f:
            self.config2.write(f)
        self.stop_event.set()
        self.telegram_keep_alive = False
        self.destroy()
        self.thread1.join()
        self.thread3.join()
        self.thread6.join()

async def main2():
    mytkinter = TkinterBot()
    mytkinter.start_threads()
    mytkinter.init_tkinter()
    mytkinter.mainloop()

    print('\nThank you for using Bumblebee Bot .. \nWe hope our service has been helpful to you. \
        \nIf you ever need anything else, dont hesitate to reach out: \
        \n\nhttps://github.com/agumonlyt/maplestorybot \
        \nhttps://discord.gg/dbsKm2jE27  \
        \n\nWishing you a fantastic day ahead!')

if __name__ == "__main__":
    asyncio.run(main2())
    # # time.sleep(10) #????????
    pass
