# import socket
# import pyautogui
# import signal
import win32gui
# import win32api
# import win32con
from io import BytesIO
import requests
import json
import os
import sys
# import uuid
import random
import cv2
import time
from math import log10, floor
from time import perf_counter
import numpy as np
import threading
import pygetwindow
from pynput import keyboard, mouse
from pynput.keyboard import Listener as KeyListener  # type: ignore[import]
from pynput.mouse import Listener as MouseListener  # type: ignore[import]
from PIL import ImageGrab
from datetime import datetime
from game import Game
import asyncio
import tkinter as tk
from tkinter import messagebox
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
from attack import leftp, leftr, rightp, rightr, sleep, npcp, npcr, refreshkeybind, goleftattack, gorightattack, goleftattackk, gorightattackk, \
    goupattack, upjumpattack, godownattack, rightjumpjumpattack, \
    stormwingrotation, castlewallrotation, bountyhuntrotation, send2, send3, goupattackv3, goupattackv2, \
    goattackleft, goattackkleft, goattackright, goattackkright
from action import Action
# from runesolver import runechecker, gotorune, enablerune, disablerune, gotopoloportal, set_hwnd
from runesolver import RuneSolver

from initinterception import interception, move_to, move_relative, left_click, mouse_position, mousedown, mouseup, hold_mouse, custommoveto, initiate_move, \
    auto_capture_devices2, keydown, keyup

# from humancursor import SystemCursor
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
        self.config2.read('secret.ini')
        self.minimapX = int(self.config.get('main', 'minimapX'))
        self.minimapY = int(self.config.get('main', 'minimapY'))
        self.initial_line_position = float(self.config.get('main', 'initial_line_position'))
        self.initial_line_position2 = float(self.config.get('main', 'initial_line_position2'))
        self.initial_line_position3 = float(self.config.get('main', 'initial_line_position3'))
        self.initial_line_position4 = float(self.config.get('main', 'initial_line_position4'))
        self.ipaddress = self.config.get('main', 'ipaddress')
        # self.flashjump = self.config.getboolean('main', 'flashjump')
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

        self.runesolver = RuneSolver()
        # self.ac = Action()        
        # if self.flashjump:
        # if self.classtype=='teleport':
        #     self.ac = Flashjump()
        # else:        
        #     self.ac = Teleport()
        # self.ac=Teleport() if self.classtype=='teleport' else Flashjump()
        self.ac=None
        # self.hc = SystemCursor()
        self.he = Helper()
        # self.character = None
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
        
        self.loop1 = asyncio.new_event_loop()
        self.loop2 = asyncio.new_event_loop()
        self.loop3 = asyncio.new_event_loop()
        self.loop4 = asyncio.new_event_loop()
        self.loop5 = asyncio.new_event_loop()
        self.loop6 = asyncio.new_event_loop()
        self.loop7 = asyncio.new_event_loop()
        self.loop8 = asyncio.new_event_loop()
        self.loop9 = asyncio.new_event_loop()
        self.thread1 = threading.Thread(target=self.run_thread1)
        self.thread2 = threading.Thread(target=self.run_thread2)
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
        print(f'setup_tab')
        self.setup_tab()
        print(f'setup_tab1')
        self.setup_tab1()
        print(f'setup_tab2')
        self.setup_tab2()
        print(f'setup_tab3')
        self.setup_tab3()
        print(f'setup_tab4')
        self.setup_tab4()
        print(f'setup_tab6')
        self.setup_tab6()
        print(f'setup_tabs_done')
        # self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.tkinter_started=True
        # self.root.mainloop()
        
    def init_tkinter2(self):
        # self.root = tk.Tk()
        self.root = customtkinter.CTk()
        self.root.title("chrome")
        # photo=PhotoImage(file='icon.ico')
        # self.root.iconphoto(False,photo)
        self.root.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
        self.root.wm_iconbitmap()
        self.root.iconphoto(False, self.root.iconpath)
        # self.root.iconbitmap(default="icon.ico")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 800
        window_x = self.screen_width - window_width
        window_y = 0
        self.root.geometry(f"{window_width}x{window_height}+{window_x-10}+{window_y}")
        # self.root.grid_rowconfigure(0, weight=1) # not sure bout this
        # self.root.grid_columnconfigure(0, weight=1) # not sure bout this
        # self.root.resizable(False,False)
        # # background_image = tk.PhotoImage(file="bumblebee.gif")
        # background_image = Image.open("bumblebee.gif")
        # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_label = tk.Label(root, image=background_photo)
        # background_label.place(relwidth=1, relheight=1)
        # background_label.image = background_photo
        print(f'setup_tab')
        self.setup_tab()
        print(f'setup_tab1')
        self.setup_tab1()
        # print(f'setup_tab2')
        # self.setup_tab2()
        print(f'setup_tab3')
        self.setup_tab3()
        print(f'setup_tab4')
        self.setup_tab4()
        # print(f'setup_tab5')
        # self.setup_tab5()
        print(f'setup_tab6')
        self.setup_tab6()
        print(f'setup_tabs_done')
        # self.root.rowconfigure(0, weight=1) # not sure bout this
        # self.root.columnconfigure(0, weight=1) # not sure bout this
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # self.threads = []
        # self.stop_event = threading.Event()
        # self.thread = threading.Thread(target=self.start_the_main, args=(self.stop_event,))
        # self.thread.start()
        # self.threads.append((self.thread, self.stop_event))
        # self.thread2 = threading.Thread(target=self.start_the_main2, args=(self.stop_event,))
        # self.thread2.start()
        # self.threads.append((self.thread, self.stop_event), (self.thread2, self.stop_event))
        self.tkinter_started=True
        self.root.mainloop()
        

    async def async_function(self, thread_name, iterations):
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
            print(f'finished telegram_run1')
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            print(f'finished telegram_run2')
        except Exception as e:
            print(f'telegram {e=}')
            self.acc_not_bind = True
            self.telegram_started = True
        finally:
            print(f'exiting telegram thread ..')
            
    async def async_function2(self, thread_name, iterations):
        while not self.telegram_started:
            time.sleep(1)
        self.init_tkinter()
        try:
            # self.init_tkinter()
            pass
        except Exception as e:
            print(f'init_tkinter {e=}')
            return
        # for i in range(iterations):
        #     print(f"{thread_name} - Iteration {i}")
        #     await asyncio.sleep(1)  # Simulating asynchronous work

    def run_thread1(self):
        asyncio.set_event_loop(self.loop1)
        self.loop1.run_until_complete(self.async_function("Thread 1", 5)) # telegram thread

    def run_thread2(self):
        asyncio.set_event_loop(self.loop2)
        self.loop2.run_until_complete(self.async_function2("Thread 2", 5)) # tkinter init thread

    def run_thread3(self):
        asyncio.set_event_loop(self.loop3)
        self.loop3.run_until_complete(self.async_function3("Thread 3", 5)) # main thread

    def run_thread4(self):
        print(f'run_thread4 started')
        asyncio.set_event_loop(self.loop4)
        self.loop4.run_until_complete(self.async_function4()) # checker thread
        print(f'run_thread4 endeded')

    def run_thread5(self):
        print(f'run_thread5 started')
        asyncio.set_event_loop(self.loop5)
        self.loop5.run_until_complete(self.async_function5()) # gma thread
        print(f'run_thread5 endeded')
    
    def run_thread6(self):
        asyncio.set_event_loop(self.loop6)
        self.loop6.run_until_complete(self.async_function6()) # just a button loop
    
    def run_thread7(self):
        asyncio.set_event_loop(self.loop7)
        self.loop7.run_until_complete(self.async_function7()) # script recording
        print(f'run_thread7 ended. ')
    
    def run_thread8(self):
        asyncio.set_event_loop(self.loop8)
        self.loop8.run_until_complete(self.async_function8()) # script playback
        print(f'run_thread8 ended. ')

    def run_thread9(self):
        asyncio.set_event_loop(self.loop9)
        self.loop9.run_until_complete(self.async_function9()) # script playback
        print(f'run_thread9 ended. ')

    def start_threads(self):
        # Start both threads
        self.thread1.start()
        # self.thread2.start()
        self.thread3.start()
        self.thread6.start()

    def wait_for_threads(self):
        # Wait for both threads to finish
        self.thread1.join()
        print(f'thread1 joined. ')
        # self.thread2.join()
        # print(f'thread2 joined. ')
        self.thread3.join()
        print(f'thread3 joined. ')
        self.thread6.join()
        print(f'thread6 joined. ')

    async def async_function3(self, thread_name, iterations):
        print(f'bot has started ..')
        while not self.tkinter_started:
            time.sleep(1.01)
        # while True: # testing purpose
        #     if self.pause:
        #         print(f'script is paused .. click resume to resume. ')
        #         while self.pause:
        #             # do nothing
        #             time.sleep(1)
        #             if self.stop_event.is_set():
        #                 # self.thread4.join()
        #                 return
        #         print(f'script resumed ..')
        #     # # whitedot = self.g.white_dot_checker()
        #     hwnd = win32gui.FindWindow(None, "MapleStory")
        #     position = win32gui.GetWindowRect(hwnd)
        #     x, y, w, h = position
        #     # # print(f'{x=} {y=} {w=} {h=}') # 8 left right 5 up down 29 title bar | minus left 8 | minus top 34
        #     # # print(f'{x=} {y=} {w=} {h=}') # 8 left right 1 up 8 down 30 title bar | minus left 8 | minus top 31
        #     # # # x+222, y+410 
        #     # # # move_to(x+self.position5[0],y+self.position5[1])
        #     # move_to(x+self.portaldialogueX,y+self.portaldialogueY)
        #     # move_relative(100)
        #     # time.sleep(.5)
        #     targetx=500
        #     targety=600
        #     # with hold_mouse('left'):
        #     #     for i in range(10):
        #     #         print(f'{i=}')
        #     #         move_relative(20,0)
        #     #         move_relative(0,20)
        #     #         time.sleep(.5)
        #     # await custommoveto(targetx,targety)
        #     # left_click()
        #     # time.sleep(2.411) # when testing ..
        #     x,y=mouse_position()
        #     print(f'{x=} {y=}')
        #     move_relative(50,10)
        #     time.sleep(2)
        #     #
        #     # await rightjumpjumpattack()
        #     # time.sleep(1.011) # when testing ..                 
        #     #
        #     # # huntingmapcheckerlocations = self.g.hunting_map_timer_checker() # check if is hidden street bounty hunt
        #     # huntingmapcheckerlocations = self.g.hunting_map2_checker()
        #     # # huntingmapcheckerlocations = self.g.gma_detector() # 
        #     # # huntingmapcheckerlocations = self.seperate_gma_detector() # 
        #     # if huntingmapcheckerlocations is not None:
        #     #     print(f'{huntingmapcheckerlocations=}')
        #     #

        #     #
        #     time.sleep(1.011) # when testing ..
        self.thread4 = threading.Thread(target=self.run_thread4)
        self.thread4.start() # all the detector goes here
        self.thread5 = threading.Thread(target=self.run_thread5)
        self.thread5.start() # gma detector goes here
        self.thread9 = threading.Thread(target=self.run_thread9)
        self.thread9.start() # rock detector
        # left1=self.line_position_slider.get()
        # right1=self.line_position_slider2.get()
        # top1=self.line_position_slider3.get()
        # btm1=self.line_position_slider4.get()
        # self.left=self.line_position_slider.get()/2+0
        # self.right=self.line_position_slider2.get()/2+0
        # self.top=self.line_position_slider3.get()/2-2
        # self.btm=self.line_position_slider4.get()/2-2
        # self.g = Game((8, 63, self.minimapX, self.minimapY))
        # self.character = Character()
        # self.character.setup(self.left,self.right,self.top,self.btm,self.classtype,self.runesolver,self.g)
        self.ac=self.character.ac
        randomlist = ['z', 'x', 'c', 'space', '2', '3', '0', 'f9', 'w', 'e', 'r', 't', 's', 'd', 'f', 'v']
        offsetx=10
        offsety=10
        randommtimer0=0
        randommtimer=0
        replaceropeconnecttimer0=0
        replaceropeconnecttimer=0
        runonce=True
        self.polocheckertimer0=0
        polocheckertimer=0
        runetimer0=0
        runetimer=0
        checkrune=True
        solverune=False
        self.now=0
        xynotfound=0
        await initiate_move()
        # self.g.init_maple_windows()
        rockcounter=0        
        now=perf_counter()        
        fourth=False
        thirdtimer0=now
        thirdtimer=now
        third=False
        secondtimer0=now
        secondtimer=now
        second=False
        while True:
            if self.pause:
                self.rocklockcounter=0
                self.rocklockcounter2=0                
                await self.character.ac.jumpr() # release all key # by right
                await self.character.ac.downr() # release all key # by right
                print(f'script is paused .. click resume to resume. ')
                while self.pause:
                    # do nothing
                    time.sleep(1)
                    if self.stop_event.is_set():
                        self.thread4.join()
                        self.thread5.join()
                        self.thread9.join()
                        return
                print(f'script resumed ..')
                fourth=third=second=False
                thirdtimer0=perf_counter()
                secondtimer0=perf_counter()
            #
            # time.sleep(.411) # when testing ..
            # time.sleep(.011) # when real botting ..
            # time.sleep(.001) # when idk maybe you gone insane ..
            # g_variable = self.g.get_player_location()
            # x, y = (None, None) if g_variable is None else g_variable
            x, y = (None, None)
            if x == None or y == None:
                # rockloc = self.g.rock_checker()
                # if rockloc is not None:
                #     pass
                # print(f'main: {(perf_counter()-now):.10f}')
                if self.rockduck:
                    self.rockduck=False
                    # print(f'rock on 2nd incoming, should release jump and duck instead. {(perf_counter()-now):.10f} {rockcounter=}')
                    # print(f'duck')
                    await self.character.ac.downp(3,11)
                    while not self.rockduck and not self.rockduck2:
                        if self.fourth or self.pause:
                            break
                    await self.character.ac.downr(3,11)
                    # print(f'stand')
                elif self.rockduck2:
                    self.rockduck2=False
                    # print(f'rock on 3rd row incoming, should jump. {(perf_counter()-now):.10f}')
                    await self.character.ac.jumpp(151,181)
                    await self.character.ac.jumpr(3,11)
                now=perf_counter()
                if not fourth:        
                    thirdtimer = now-thirdtimer0                
                    if thirdtimer >= 47:
                        fourth=True
                    elif thirdtimer >= 30:
                        third=True
                        second=False
                    elif thirdtimer >= 15:
                        second=True
                elif fourth:
                    print('fourth')
                    self.rockduck=False
                    self.rockduck2=False
                    await self.character.ac.downr(3,11)
                    while perf_counter()-now < 11:
                        await self.character.ac.jumpp(101,171)
                        await self.character.ac.jumpr(3,151)
                    print('fourth  end')
                    fourth = False
                    self.resumebutton()

                # xynotfound+=1
                # if xynotfound > 70:
                #     t = time.localtime()
                #     currenttime = time.strftime("%H:%M:%S", t)
                #     print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                #     # stop_flag = True
                #     # randompicker_thread.join()
                #     self.pause=True
                #     # return
                # print(f'x==None, pass ..')
                # time.sleep(.1)
                # pass
            else: # 111.5 27.5
                xynotfound=0
                await self.character.perform_next_attack(x,y)
                # print(f'character_next_move')
                
                # self.now = perf_counter()
                # randommtimer = self.now - randommtimer0
                # if randommtimer > 15:
                #     randommtimer0 = self.now
                #     p = random.randint(0, len(randomlist)-1)
                #     code = random.choice(randomlist)
                #     if code is not None:
                #         print(f'randomiser {code=}')
                #         await send2(code)
                #         await send3(code)
                # if self.replaceropeconnect==True:
                #     if runonce:
                #         replaceropeconnecttimer0=self.now
                #         runonce=False
                #     replaceropeconnecttimer = self.now - replaceropeconnecttimer0
                #     if replaceropeconnecttimer > 90:
                #         self.replaceropeconnect=False
                #         runonce=True
                # polocheckertimer = self.now - self.polocheckertimer0
                # if polocheckertimer > 90:
                #     self.pausepolochecker=False
                # runetimer = self.now - runetimer0
                # # if runetimer > 600: # change to 600 when haste
                # if runetimer > 900: # change to 600 when haste
                #     # checkrune = True
                #     checkrune = False
                # if checkrune:
                #     solverune = self.runesolver.runechecker(self.g)
                # # print(f'{x=} {y=} {statuetimer=} {fountaintimer=}, {runetimer=}, {cctimer=}')
                # print(f'{x=} {y=} {runetimer=} {solverune=} | {left=}, {top=}, {right=}, {btm=} | {left1=}, {top1=}, {right1=}, {btm1=}')
                # # print(f'{x=}, {y=} | {left=}, {top=}, {right=}, {btm=} | {left1=}, {top1=}, {right1=}, {btm1=}')

                # if solverune:
                #     await self.runesolver.gotorune(self.g)
                # elif self.polochecker:
                #     if self.whitedotoccur:
                #         if not await self.polocheckerfunc(self.gotoportal):
                #             self.replaceropeconnect=True
                #         self.whitedotoccur=False
                #     else:
                #         await self.polocheckerfunc(self.gotoportal)
                # else:
                #     pass
            
            # print(f'{x=}, {y=} | {left=}, {top=}, {right=}, {btm=} | {left1=}, {top1=}, {right1=}, {btm1=}')

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

    async def async_function4(self):
        whitedotcounter=0
        while True:
            while self.pause:
                time.sleep(1)
                if self.stop_event.is_set():
                    return
            # print(f'new checking cycle ..')
            diedcheckerlocations = self.g.died_checker()
            if diedcheckerlocations is not None:
                print(f'{diedcheckerlocations=}')
                # hwnd = win32gui.FindWindow(None, "MapleStory")
                position = win32gui.GetWindowRect(self.maplehwnd)
                x, y, w, h = position
                print(f'moving to x, y')
                # await custommoveto(x+self.position6[0],y+self.position6[1])
                # self.hc.move_to((x+self.position6[0],y+self.position6[1]))
                await self.he.move_to(x+self.position6[0],y+self.position6[1])
                time.sleep(.1)
                print(f'clicking x, y')
                left_click()
                print(f'done clicking')
                move_relative(10,0)
                time.sleep(.1)
            if not self.pausepolochecker and not self.portaldisabled:
                polocheckerlocations = self.g.polo_checker() # check for portal on minimap
                if polocheckerlocations is not None:
                    print(f'{polocheckerlocations=}')
                    self.polochecker = True
                    self.gotoportal=True
            whitedotlocations = self.g.white_dot_checker()
            if whitedotlocations is not None:
                whitedotcounter+=1
                if whitedotcounter>1:
                    self.whitedotoccur=True
                    self.polochecker=True
                    self.gotoportal=False
                    # if not await self.polocheckerfunc(False):
                    #     self.replaceropeconnect=True
                    # position = win32gui.GetWindowRect(self.maplehwnd)
                    # x, y, w, h = position
                    # print(f'moving to x, y')
                    # await custommoveto(x+self.portaldialogueX,y+self.wolfdialogueY)
                    # time.sleep(.1)
                    # print(f'clicking x, y')
                    # left_click()
                    # print(f'done clicking')
                    # move_relative(10,0)
                    # time.sleep(.1)
            elif whitedotlocations is None:
                whitedotcounter=0
            
            time.sleep(2)
            
    async def async_function5(self): # gma_checker
        while True:
            while self.pause:
                time.sleep(1)
                if self.stop_event.is_set():
                    return
            if self.chathwnd:
                pass
                # gmacheckerlocations = self.seperate_gma_detector()
                # if gmacheckerlocations:
                #     print(f'got GM')
                # else:
                #     print(f'no GM')
            else:
                pass
                # print(f'async_function5: chat window not found. ')

            time.sleep(5)

    async def async_function6(self): # just a button loop
        while True:
            time.sleep(1)
            if self.stop_event.is_set():
                print(f'async_function6 return. ')
                return
            if self.triggermousetest:
                await initiate_move()
                self.triggermousetest=False

    async def async_function7(self): # script recording thread (keyboard listener)
        self.realrecord()
        print(f'async_function7 complete')

    async def async_function8(self): # script playback thread
        await self.playback()
        print(f'async_function8 complete')

    # def find_maplestory_windows(self, hwnd, lParam):
    #     title = win32gui.GetWindowText(hwnd)
    #     if 'MapleStory' in title:
    #         print(f"Window Title: {title}, Handle: {hwnd}")

    def init_maple_windows(self):
        windows=[]
        winlist=[]
        winlist = pygetwindow.getWindowsWithTitle('MapleStory')
        for w in winlist:
            windows.append(w._hWnd)
        print(f'{winlist=} {windows}')
        for windowhwnd in windows:
            position = win32gui.GetWindowRect(windowhwnd)
            x, y, w, h = position
            print(f'{windowhwnd=} {w-x=}')
            if w-x == 410:
                self.chathwnd=windowhwnd
                print(f'{x=} {y=} {w=} {h=} {windowhwnd=}')
            # elif w-x == 816:
            # elif w-x == 1040:
            # elif w-x == 1296:
            # elif w-x == 1382: # 1366x768
            elif w-x == 1382 or w-x == 1296 or w-x == 1040 or w-x == 816:
                self.maplehwnd=windowhwnd
                self.runesolver.set_maplehwnd(self.maplehwnd)

    def init_maple_windows_old(self):
        # win32gui.EnumWindows(self.find_maplestory_windows, 0)
        # hwnd = win32gui.FindWindow(None, "MapleStory")
        hwnd = 0
        windows=[]
        while True:
            print(f'{hwnd}')
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
                print(f'{self.maplehwnd}')
            print(f'{x} {y} {w} {h}')
            # screenshot = ImageGrab.grab(position)
            # screenshot = np.array(screenshot)
            # img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        #     cv2.imshow(f'{windowhwnd}', img)
        #     cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def rebindchathwnd(self):
        hwnd = 0
        windows=[]
        while True:
            print(f'{hwnd}')
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
            # print(f'{self.chathwnd=}')
            position = win32gui.GetWindowRect(self.chathwnd)
            x, y, w, h = position
            # print(f'{x} {y} {w} {h}')
            chatposition = (x,y+385,w-15,h-25)
            screenshot = ImageGrab.grab(chatposition)
            screenshot = np.array(screenshot)
            img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            # cv2.imshow('img', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            height, width = img.shape[0], img.shape[1]
            # print(f'{img=}')
            # img_reshaped = np.reshape(img, ((width * height), 4), order="C")
            img_reshaped = np.reshape(img, ((width * height), 3), order="C")
            # print(f'{img_reshaped=}')
            # print(f'{img_reshaped[:,0]=}')
            locations = []
            sum_x, sum_y, count = 0, 0, 0
            matches = np.where(
                (img_reshaped[:,0] >= 201) & (img_reshaped[:,0] <= 225) &
                (img_reshaped[:,1] >= 201) & (img_reshaped[:,1] <= 225) &
                (img_reshaped[:,2] >= 201) & (img_reshaped[:,2] <= 225) 
                )[0]
            # print(f'{matches=}')
            for idx in matches:
                # Calculate the original (x, y) position of each matching index.
                sum_x += idx % width
                sum_y += idx // width
                count += 1
                # print(f'{idx % width=} {idx // width=} {width=} {img_reshaped[idx]} {count=}')
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
            # do bountyhunt rotation for maybe 30sec
            for i in range(6):
                if not self.pause:
                    # await bountyhuntrotation()
                    await self.character.bountyhuntrotation()
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    # do bountyhunt rotation
                    print(f'stillinportal')
                    # if not self.pause:
                    #     # await bountyhuntrotation()
                    #     await self.character.bountyhuntrotation()
                    # else:
                    #     time.sleep(1)
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
            # press npc button 5 times to exit
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
            # do guardingthecastlewall rotation
            for i in range(10):
                # await castlewallrotation()                
                await self.character.castlewallrotation()
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    # do guardingthecastlewall rotation
                    print(f'stillinportal')
                    # await castlewallrotation()   
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
            # press npc button 5 times to exit
            await leftp()
            time.sleep(.8)
            await leftr()
            for i in range(8):
                await npcp()
                await npcr()
                await sleep(.1)
        elif portaltype == 'd':
            print(f'dostormwingrotation')
            # do stormwing rotation
            # for i in range(7):
                # await stormwingrotation()
            await self.stormwing(100)
            while True:
                huntingmaptimerchecker = self.g.hunting_map_timer_checker()
                if huntingmaptimerchecker is not None:
                    # do stormwing rotation
                    print(f'stillinportal')
                    # await stormwingrotation()
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
            # press npc button 5 times to exit
            await leftp()
            time.sleep(.8)
            await leftr()
            for i in range(7):
                await npcp()
                await npcr()
                time.sleep(.1)
        elif portaltype == 'e':
            print(f'doespeciaspam')
            # do especia spam
            for i in range(5):
            #     await npcp()
            #     await npcr()
            #     r = random.randint(500,1000)
            #     r /= 1000
            #     await sleep(r)
                await self.especia()
            # check if timer still there
            # if timer no longer there, press npc x4 to get out. 
            for count in range(100): # for testing
            # while True:
                huntingmaptimerchecker = self.g.especia_dot_checker()
                if huntingmaptimerchecker is not None:
                    # do especia spam
                    print(f'stillinportal, {count=}')
                    # await npcp()
                    # await npcr()
                    # r = random.randint(500,1000)
                    # r /= 1000
                    # await sleep(r)
                    await self.especia()
                    pass
                else:
                    print(f'notinportal')
                    while self.g.dark_checker() is not None:
                        print(f'map transitioning ..')
                        time.sleep(1)
                    time.sleep(1.5)
                    break
            # press npc button 5 times to exit
            for i in range(7):
                await npcp()
                await npcr()
                time.sleep(.1)
        elif portaltype == 'r':
            print(f'fritoportalendchat')
            # hwnd = win32gui.FindWindow(None, "MapleStory")
            position = win32gui.GetWindowRect(self.maplehwnd)
            x, y, w, h = position
            time.sleep(.1)
            # await custommoveto(x+self.portaldialogueX,y+self.portaldialogueY)
            # self.hc.move_to((x+self.portaldialogueX,y+self.portaldialogueY))
            await self.he.move_to(x+self.portaldialogueX,y+self.portaldialogueY)
            time.sleep(.1)
            left_click()
            self.pausepolochecker=True
            self.polocheckertimer0 = self.now
            truefalse=False
        elif portaltype == 'f':
            print(f'clickendchat')
            # click end chat cause flamewolf
            # hwnd = win32gui.FindWindow(None, "MapleStory")
            position = win32gui.GetWindowRect(self.maplehwnd)
            x, y, w, h = position
            time.sleep(.1)
            # await custommoveto(x+self.portaldialogueX,y+self.wolfdialogueY)
            # self.hc.move_to((x+self.portaldialogueX,y+self.wolfdialogueY))
            await self.he.move_to(x+self.portaldialogueX,y+self.wolfdialogueY)
            time.sleep(.1)
            left_click()
            self.pausepolochecker=True
            self.polocheckertimer0 = self.now
            truefalse=False
        else:
            print(f'enterportalfailedorerror')
            # means enter portal failed, or error, back to training. 
        self.polochecker=False
        return truefalse
    
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
        print(f'{update.message=}')
        print(f'{self.chat_id=}')
        print(f'{type(self.chat_id)=}')
        print(f'{type(update.message.chat.id)=}')
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
                    # do nothing
                    time.sleep(1)
                    if self.stop_event.is_set():
                        # self.thread4.join()
                        return
                print(f'script resumed ..')

    async def stormwing(self, count):
        goleft=False
        goright=True
        ## 1.8 165.2 (top=24.5?) (btm=62.5) (right=138.5?)
        top=29.0
        left=35.0 # 18.0 # 27.0
        right=130 # 125.0 # 135.0 140.0 132.5
        btm=58.0 # 54.5
        for i in range(count):            
            huntingmaptimerchecker = self.g.hunting_map_timer_checker()
            if huntingmaptimerchecker is None:
                return
            # time.sleep(.4) # running test
            time.sleep(.3) # running real
            # time.sleep(.2) # running real
            g_variable = self.g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            if x == None or y == None:
                xynotfound+=1
                if xynotfound > 50:
                    t = time.localtime()
                    currenttime = time.strftime("%H:%M:%S", t)
                    print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                    # stop_flag = True
                    # randompicker_thread.join()
                    return
                print(f'x==None, pass ..')
                time.sleep(.1)
                pass
            else:
                xynotfound=0
                print(f'{x=} {y=} {goleft=} {goright=}')
                goleft,goright = await self.character.stormwing(x,y,goleft,goright)
                # # time.sleep(.1)
                # if goright:
                #     if x > right:
                #         if y < btm:
                #             await godownattack()
                #             time.sleep(.3)
                #             await random.choice([self.ac.goleftattack,self.ac.goattackleft,self.ac.goleftattackk,self.ac.goattackkleft])()
                #             time.sleep(.1)
                #         elif y > top:
                #             await upjumpattack()
                #             time.sleep(.3)
                #         goright=False
                #         goleft=True
                #     else:
                #         await random.choice([self.ac.gorightattack,self.ac.goattackright,self.ac.gorightattackk,self.ac.goattackkright])()
                #         time.sleep(.3)
                #     if x < left: # only if x < left
                #         if y < btm:
                #             await godownattack()
                #             time.sleep(.3)
                # elif goleft:
                #     if x < left: # only if x < left
                #         if y > top:
                #             time.sleep(.1)
                #             await upjumpattack()
                #             time.sleep(.3)
                #         elif y < top:
                #             await godownattack()
                #             time.sleep(.3)
                #             await random.choice([self.ac.gorightattack,self.ac.goattackright,self.ac.gorightattackk,self.ac.goattackkright])()
                #             time.sleep(.3)
                #         goright=True
                #         goleft=False
                #     else:
                #         await random.choice([self.ac.goleftattack,self.ac.goattackleft,self.ac.goleftattackk,self.ac.goattackkleft])()
                #         time.sleep(.3)
                #     if x > right: # only if x > right
                #         if y < btm:
                #             await godownattack()
                #             time.sleep(.3)


    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(f'{update.message}')
        # global chat_id
        # print(f'{chat_id =}')
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
        # if message_type == 'group':
        #     if BOT_USERNAME in text:
        #         new_text: str = text.replace(BOT_USERNAME, '').strip()
        #         response: str = handle_response(new_text)
        #     else:
        #         return
        # else:
        #     response: str = handle_response(text)    
        await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')


        # # very cool title bar
        # root.overrideredirect(True)  # Remove the title bar
        # # Create a frame for a custom title bar
        # title_bar = tk.Frame(root, bg="blue", height=30, relief="raised", bd=0)
        # title_bar.pack(fill="x")
        # # Create a custom font for title text
        # title_font = ("Helvetica", 14)
        # # Set the width and height of the button
        # button_width = 15
        # button_height = 3
        # # Choose a brighter green color
        # button_color = "lime"
        # # Create a button with the custom font, width, height, and color
        # button = tk.Button(title_bar, text="Click me!", command=on_button_click, font=title_font, width=button_width, height=button_height, bg=button_color)
        # button.pack(side="left", padx=10)
        # # Close button
        # close_button = tk.Button(title_bar, text="X", command=root.destroy, font=title_font, width=2, height=1, bg="red", relief="flat")
        # close_button.pack(side="right", padx=10)
        # # Make the window draggable
        # def start_drag(event):
        #     root.x = event.x
        #     root.y = event.y
        # def drag(event):
        #     deltax = event.x - root.x
        #     deltay = event.y - root.y
        #     x = root.winfo_x() + deltax
        #     y = root.winfo_y() + deltay
        #     root.geometry(f"+{x}+{y}")
        # title_bar.bind("<ButtonPress-1>", start_drag)
        # title_bar.bind("<B1-Motion>", drag)

    def setup_tab(self):
        # self.mytab = customtkinter.CTkTabview(self.root,width=600,height=800,corner_radius=5, fg_color="#123456")
        # self.mytab = customtkinter.CTkTabview(self.root,width=600,height=800,corner_radius=5)
        self.mytab = customtkinter.CTkTabview(self,width=600,height=800,corner_radius=5)
            # segmented_button_fg_color="#1a4b6c", segmented_button_selected_color="#45ab65", , fg_color="#123456", 
            # segmented_button_selected_hover_color="#fc31ab", segmented_button_unselected_color="#1b5fcf", 
            # segmented_button_unselected_hover_color="#0abf45",text_color="#4cff4f",
            # state='normal',command=None)
        self.mytab.pack(padx=(1,1),pady=(1,1))
        self.tab1 = self.mytab.add("Rotation")
        self.tab2 = self.mytab.add("Script")
        self.tab3 = self.mytab.add("Design")
        self.tab4 = self.mytab.add("Telegram")
        self.tab5 = self.mytab.add("Autoclicker")
        self.tab6 = self.mytab.add("Settings")

        # self.notebook = ttk.Notebook(self.root)
        # # Create tabs (frames) to be added to the Notebook
        # self.tab1 = ttk.Frame(self.notebook)
        # self.tab2 = ttk.Frame(self.notebook)
        # self.tab3 = ttk.Frame(self.notebook)
        # self.tab4 = ttk.Frame(self.notebook)
        # self.tab5 = ttk.Frame(self.notebook)
        # self.tab6 = ttk.Frame(self.notebook)
        # # Add tabs to the Notebook
        # self.notebook.add(self.tab1, text="Rotation")
        # self.notebook.add(self.tab2, text="Tab 2")
        # self.notebook.add(self.tab3, text="Design")
        # self.notebook.add(self.tab4, text="Telegram")
        # self.notebook.add(self.tab5, text="Tab 5")
        # self.notebook.add(self.tab6, text="Settings")
        # # Bind the tab change event
        # self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # # Pack the Notebook widget
        # self.notebook.pack(expand=1, fill="both")
        # # Add content to each tab
        # label1 = tk.Label(self.tab1, text="Main Rotation")
        # label1.pack(padx=10, pady=10)
        # label2 = tk.Label(self.tab2, text="Script Recording Method (Coming Soon .. )")
        # label2.pack(padx=10, pady=10)
        # label3 = tk.Label(self.tab3, text="Rotation Design")
        # label3.pack(padx=10, pady=10)
        # label4 = tk.Label(self.tab4, text="Telegram Setup")
        # label4.pack(padx=10, pady=10)
        # label5 = tk.Label(self.tab5, text="Autoclicker (Monster Life)")
        # label5.pack(padx=10, pady=10)
        # label6 = tk.Label(self.tab6, text="Settings")
        # label6.pack(padx=10, pady=10)

    def setup_tab1(self):
        # framebase = tk.Frame(self.tab1, bg='#3f5b79', bd=0)
        framebase = customtkinter.CTkFrame(self.tab1)
        # framebase.pack(padx=0, pady=0, fill='both', expand=True)
        framebase.pack(padx=0, pady=(0,2), fill='x', expand=False)
        framebase.columnconfigure(0,weight=1)
        framebase.columnconfigure(1,weight=1)
        framebase.columnconfigure(2,weight=1)
        # framebase.grid_columnconfigure(0,weight=1)
        # framebase.grid_columnconfigure(1,weight=1)
        # framebase.grid_columnconfigure(2,weight=1)
        # framebase.grid_propagate(False)
        # frameleft = tk.Frame(framebase, bg='#9eaa15', bd=0, width=170, height=110)
        frameleft = customtkinter.CTkFrame(framebase, width=195, height=120, fg_color='transparent')
        frameleft.grid_propagate(0)
        # frameleft.pack(padx=(1,1),pady=(1,1), fill='both', expand=True, side='left')
        frameleft.grid(row=0,column=0,padx=(1,1),pady=(1,1))
        # framecenter = tk.Frame(framebase, bg='#1eaaf5', bd=0, width=170, height=110)
        framecenter = customtkinter.CTkFrame(framebase, width=195, height=120)
        framecenter.grid_propagate(0)
        framecenter.grid_rowconfigure(0,weight=1)
        framecenter.grid_columnconfigure(0,weight=1)
        # framecenter.pack(padx=(1,1),pady=(1,1), fill='both', expand=True, side='left')
        framecenter.grid(row=0,column=1,padx=(1,1),pady=(1,1))
        # frameright = tk.Frame(framebase, bg='#3e3aa4', bd=0, width=170, height=110)
        frameright = customtkinter.CTkFrame(framebase, width=195, height=120, fg_color='transparent')
        frameright.grid_propagate(0)
        # frameright.grid_rowconfigure(0,weight=1)
        # frameright.grid_rowconfigure(1,weight=1)
        frameright.grid_columnconfigure(0,weight=1)
        # frameright.pack(padx=(1,1),pady=(1,1), fill='both', expand=True, side='left')
        frameright.grid(row=0,column=2,padx=(1,1),pady=(1,1))
        self.button = customtkinter.CTkButton(framecenter, text="Resume", command=self.resumebutton, fg_color='tomato', font=('Helvetica', 16), text_color='black',hover=False)
        # self.button = tk.Button(framecenter, text="Resume", command=self.resumebutton, width=8, height=4, bg='tomato', font=('Helvetica', 16))
        # self.button = tk.Button(framecenter, text="Resume", command=self.resumebutton, bg='tomato')
        # self.button.pack(pady=(1,1), fill='both', expand=True)
        # self.button.pack(pady=(1,1))
        self.button.grid(row=0,column=0,pady=(1,1), sticky=tk.N+tk.S+tk.E+tk.W)
        self.presettemp=self.preset
        def on_select(event):
            # self.preset = comboboxpreset.get()
            self.presettemp = comboboxpreset.get()
            print(f'{self.preset=} {self.presettemp=}')
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
            print(f'{self.preset=} {self.presettemp=}')
            self.preset=self.presettemp
            print(f'{self.preset=} {self.presettemp=}')
            self.button_adjustminimap()
            allpresets=[]
            allpresets.append([self.minimapX,self.minimapY,self.line_position_slider.get(),self.line_position_slider2.get()
            ,self.line_position_slider3.get(),self.line_position_slider4.get()])
            with open(f'preset/{self.preset}.json', 'w') as json_file:
                json.dump(allpresets, json_file, indent=4)
            self.canvasimageholdertemp.save(f'image/{self.preset}.png')
            print(f'saved preset. ')
            saved_window = customtkinter.CTkToplevel(frameleft, fg_color='#abcdef')
            saved_window.title('chrome')
            saved_window.resizable(False,False)#width,height
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
            print(f'{width=} {height=}')
            # saved_window.geometry(f'400x100+{width-100}+{height-200}')
            saved_window.geometry(f'{width-300}+{height-200}')
        buttonsave = customtkinter.CTkButton(frameleft, text="save all", command=save, width=100)
        buttonsave.grid(row=3,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        ## ------------------------------------------------------------------------------------------------------------- ##
        # def on_select_rotation(event): # tag UI placement order
        #     rotation = comboboxrotation.get()
        #     self.character.set_rotation(rotation)
        # # folder_path = "preset"
        # # file_list = os.listdir(folder_path)
        # # json_files = [file for file in file_list if file.endswith(".json")]
        # # json_file_names = [os.path.splitext(file)[0] for file in json_files]
        # rotation_list = self.character.get_rotation_list()
        # # comboboxpreset = ttk.Combobox(frameright, values=json_file_names, state="readonly", width=17)
        # # comboboxpreset = ttk.Combobox(frameright, values=json_file_names, state="readonly", width=10)
        # # comboboxpreset.pack(padx=1, pady=1, side='top', anchor='ne', fill='both', expand=True)
        # # comboboxpreset.pack(padx=1, pady=1, side='top', anchor='ne')
        # # comboboxpreset.bind("<<ComboboxSelected>>", on_select)
        # comboboxrotation = customtkinter.CTkComboBox(frameright, values=rotation_list, state="readonly",command=on_select_rotation,justify='left', width=120)
        # comboboxrotation.grid(row=0,column=0,padx=(1,1), pady=(1,1), sticky=tk.NE)
        # comboboxrotation.set(json_file_names[json_file_names.index(self.preset)])
        # buttonchange = customtkinter.CTkButton(frameright, text="change rotation", command=self.reload, width=100)
        # buttonchange.grid(row=1,column=0,padx=(1,1),pady=(1,1), sticky=tk.NE)
        # def new():
        #     profile_name = simpledialog.askstring("New Profile", "Enter the name for the new profile:")
        #     if profile_name:
        #         json_file_names.append(profile_name)
        #         comboboxpreset.set(json_file_names[len(json_file_names)-1])
        #         comboboxpreset.configure(values=json_file_names)
        #         self.widthentry.delete(0,tk.END)
        #         self.widthentry.insert(0,200)
        #         self.heightentry.delete(0,tk.END)
        #         self.heightentry.insert(0,150)
        #         self.button_adjustminimap_fake()
        #         # self.update_four_lines(50,350,50,150)
        #         self.update_four_lines(180,220,60,90)
        # buttonnew = customtkinter.CTkButton(frameright, text="new preset", command=new, width=100)
        # buttonnew.grid(row=2,column=0,padx=(1,1),pady=(1,1), sticky=tk.NE)        
        # def save():
        #     allpresets=[]
        #     allpresets.append([self.minimapX,self.minimapY,self.line_position_slider.get(),self.line_position_slider2.get()
        #     ,self.line_position_slider3.get(),self.line_position_slider4.get()])
        #     with open(f'preset/{self.preset}.json', 'w') as json_file:
        #         json.dump(allpresets, json_file, indent=4)
        #     self.canvasimageholdertemp.save(f'image/{self.preset}.png')
        #     print(f'saved preset. ')
        #     saved_window = customtkinter.CTkToplevel(frameright, fg_color='#abcdef')
        #     saved_window.title('chrome')
        #     saved_window.resizable(False,False)#width,height
        #     def close():
        #         saved_window.destroy()
        #         saved_window.update()
        #     label=customtkinter.CTkLabel(saved_window,text=f'saved. {self.preset}: {allpresets}', text_color='#123321')
        #     label.pack(padx=1,pady=(10,1), fill='none', expand=True)
        #     button=customtkinter.CTkButton(saved_window,text='ok',command=close)
        #     button.pack(padx=1,pady=1, fill='none', expand=True)
        #     # saved_window.focus()
        #     saved_window.iconpath = ImageTk.PhotoImage(file=os.path.join("icon.ico"))
        #     saved_window.wm_iconbitmap()
        #     saved_window.iconphoto(False, saved_window.iconpath)
        #     # saved_window.after(1000,lambda: saved_window.iconbitmap(os.path.join("icon.ico")))
        #     saved_window.after(200,lambda: saved_window.iconphoto(False, saved_window.iconpath))
        #     width=int(self.root.winfo_screenwidth()/2)
        #     height=int(self.root.winfo_screenheight()/2)
        #     print(f'{width=} {height=}')
        #     saved_window.geometry(f'400x100+{width-100}+{height-200}')
        # buttonsave = customtkinter.CTkButton(frameright, text="save preset", command=save, width=100)
        # buttonsave.grid(row=3,column=0,padx=(1,1),pady=(1,1), sticky=tk.NE)

        # self.button.grid(row=0,column=1,padx=(1,1),pady=(10,20))
        # label1 = tk.Label(frame3, text="x:", fg="black", bg='#ffbb29')
        # label1.pack(padx=(0,0), pady=0)
        # label1.grid(row=0, column=0, padx=(5,0), pady=0)
        # label2 = tk.Label(frame2, text="x:", fg="black", bg='#ffbb29')
        # label2.grid(row=0, column=2, padx=(5,0), pady=0)
        # frame = tk.Frame(self.tab1, bg='', bd=0)
        # frame = tk.Frame(root, bg='#ffbb29')
        # frame = tk.Frame(self.tab1)
        # frame.pack(padx=0, pady=0)
        # # # label1 = tk.Label(frame, text="x:", fg="black", bg='#ffbb29')
        # # # label1.grid(row=0, column=0, padx=(5,0), pady=0, sticky=tk.E)
        # # entry1 = tk.Entry(frame, width=10, fg='Gray')
        # # entry1.insert(0, 'Enter x...')
        # # entry1.bind("<FocusIn>", entry_focus_in)
        # # entry1.bind("<FocusOut>", entry_focus_out)
        # # entry1.grid(row=0, column=0, padx=(0,1), pady=(0,1))
        # # # label2 = tk.Label(frame, text="y:", fg="black", bg='#ffbb29')
        # # # label2.grid(row=1, column=0, padx=(5,0), pady=0, sticky=tk.E)
        # # entry2 = tk.Entry(frame, width=10, fg='Gray')
        # # entry2.insert(0, 'Enter y...')
        # # entry2.bind("<FocusIn>", entry2_focus_in)
        # # entry2.bind("<FocusOut>", entry2_focus_out)
        # # entry2.grid(row=0, column=1, padx=(1,0), pady=(0,1))
        # self.entry1 = Spinbox(frame, from_=100, to=400, font=("Helvetica", 16), width=5, increment=10)
        # self.entry1.delete(0,tk.END)
        # self.entry1.insert(0,self.minimapX)
        # self.entry1.grid(row=0,column=0, padx=(0,0), pady=(0,0))
        # self.entry2 = Spinbox(frame, from_=100, to=300, font=("Helvetica", 16), width=5, increment=10)
        # self.entry2.delete(0,tk.END)
        # self.entry2.insert(0,self.minimapY)
        # self.entry2.grid(row=0,column=1, padx=(0,0), pady=(0,0))
        # self.button2 = customtkinter.CTkButton(frame, text="adjust minimap", command=self.button_adjustminimap)
        # self.button2.grid(row=0, column=2, padx=(1,0), pady=(0,1))
        
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
        
        # self.widthentry.delete(0,tk.END)
        # self.widthentry.insert(0,self.minimapX)
        # self.heightentry.delete(0,tk.END)
        # self.heightentry.insert(0,self.minimapY)

        # self.frame2 = tk.Frame(self.tab1, bg='orange', bd=0)
        # self.frame2 = tk.Frame(self.tab1, bg='', bd=0)
        self.frame2 = customtkinter.CTkFrame(self.tab1)
        self.frame2.pack(padx=0, pady=0)
        # self.frame2.grid_rowconfigure((1,2),weight=0)
        # self.frame2.grid_columnconfigure((1,2),weight=0)
        image_path = "minimap.png"  # Replace with the actual path to your image
        img = PhotoImage(file=image_path)
        # self.canvas = tk.Canvas(self.frame2, width=self.minimapX-8, height=self.minimapY-63, bg='#fabb29')
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
            # initial_line_position = self.canvas_width / 2
        else:
            hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
            top, left, bottom, right = 8, 63, self.minimapX, self.minimapY
            with gdi_capture.CaptureWindow(hwnd) as gdiimg:
                img_cropped = gdiimg[left:right, top:bottom]
                img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
                height, width = img_cropped.shape[:2]
                width = width*2
                height = height*2
                # width = (right-left)*2
                # height = (bottom-top)*2
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
                # canvas_width=minimapX-8
                # canvas_height=minimapY-63
        


        # def tempunused(self):
        if True:
            print(f'{height=} {self.minimapY=} {self.initial_line_position=} {self.canvas_height=}')
            print(f'setuptab1: {self.initial_line_position} {self.initial_line_position2} {self.initial_line_position3} {self.initial_line_position4}')
            # self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, self.minimapY-63, fill="red", width=2)    
            self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, height, fill="red", width=2)    
            # # slider_label = tk.Label(frame, text="left threshold:", bg='#ffbb29')
            # # slider_label.grid(row=3, column=1, pady=5, padx=5)
            # self.line_position_slider = tk.Scale(self.frame2, from_=2, to=self.canvas_width, orient=tk.HORIZONTAL, length=self.canvas_width, resolution=1, command=self.update_line_position)
            self.line_position_slider = customtkinter.CTkSlider(self.frame2,from_=2,to=self.canvas_width,orientation='horizontal',number_of_steps=self.canvas_width-2, width=self.canvas_width, command=self.update_line_position)
            # self.line_position_slider.set(self.initial_line_position)
            self.line_position_slider.grid(row=1, column=0, pady=0, padx=0, sticky='we')
            
            self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, height, fill="yellow", width=2)    
            # slider_label2 = tk.Label(frame, text="right threshold:", bg='#ffbb29')
            # slider_label2.grid(row=4, column=1, pady=5, padx=5)
            # self.line_position_slider2 = tk.Scale(self.frame2, from_=2, to=self.canvas_width, orient=tk.HORIZONTAL, length=self.canvas_width, resolution=1, command=self.update_line_position2)
            self.line_position_slider2 = customtkinter.CTkSlider(self.frame2,from_=2,to=self.canvas_width,orientation='horizontal',number_of_steps=self.canvas_width-2, width=self.canvas_width, command=self.update_line_position2)
            # self.line_position_slider2.set(self.initial_line_position2)
            self.line_position_slider2.grid(row=2, column=0, pady=(0,2), padx=0, sticky='we')

            self.vertical_line3 = self.canvas.create_line(self.canvas_width, self.initial_line_position3, 2, self.initial_line_position3, fill="lime", width=2)
            # self.line_position_slider3 = tk.Scale(self.frame2, from_=2, to=self.canvas_height, orient=tk.VERTICAL, length=self.canvas_height*2, resolution=1, command=self.update_line_position3)
            self.line_position_slider3 = customtkinter.CTkSlider(self.frame2,to=2,from_=self.canvas_height,orientation='vertical',number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3, command=self.update_line_position3)
            # self.line_position_slider3.set(self.initial_line_position3)
            self.line_position_slider3.grid(row=0, column=1, rowspan=3, pady=(0,0), padx=(2,1), sticky='ns')

            self.vertical_line4 = self.canvas.create_line(self.canvas_width, self.initial_line_position4, 2, self.initial_line_position4, fill="lightblue", width=2)
            # self.line_position_slider4 = tk.Scale(self.frame2, from_=2, to=self.canvas_height, orient=tk.VERTICAL, length=self.canvas_height*2, resolution=1, command=self.update_line_position4)
            self.line_position_slider4 = customtkinter.CTkSlider(self.frame2,to=2,from_=self.canvas_height,orientation='vertical',number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3, command=self.update_line_position4)
            # self.line_position_slider4.set(self.initial_line_position4)
            self.line_position_slider4.grid(row=0, column=2, rowspan=3, pady=(0,0), padx=(0,0), sticky='ns')
            
            self.reload()
            print(f'reloaded after UI initiated. {self.classtype}')
            def on_select_rotation(event): # tag UI placement order # can only initializd after reload() # todo: organize code nicer
                self.rotation = self.comboboxrotation.get()
                self.character.set_rotation(self.rotation)
            rotation_list = self.character.get_rotation_list()
            self.comboboxrotation = customtkinter.CTkComboBox(frameright, values=rotation_list, state="readonly",command=on_select_rotation,justify='left', width=140)
            self.comboboxrotation.grid(row=0,column=0,padx=(1,1), pady=(1,1), sticky=tk.NE)
            self.comboboxrotation.set(rotation_list[rotation_list.index(self.rotation)])
            # self.frame3 = tk.Frame(self.tab1, bg='', bd=0)
            # self.frame3.pack(padx=0, pady=0)
            # self.label_currentleft = tk.Label(self.frame3, text=f"current left: {self.line_position_slider.get()}")
            # self.label_currentleft.grid(row=0, column=0, pady=0, padx=5)  
            # self.label_currenttop = tk.Label(self.frame3, text=f"current top: {self.line_position_slider3.get()}")
            # self.label_currenttop.grid(row=0, column=1, pady=0, padx=5)  
            # self.label_currentright = tk.Label(self.frame3, text=f"current right: {self.line_position_slider2.get()}")
            # self.label_currentright.grid(row=1, column=0, pady=0, padx=5)  
            # self.label_currentbtm = tk.Label(self.frame3, text=f"current btm: {self.line_position_slider4.get()}")
            # self.label_currentbtm.grid(row=1, column=1, pady=0, padx=5)  
            # self.button3 = tk.Button(self.frame3, text="  Confirm New Threshold  ", command=self.reset, bg='yellow', font=('Helvetica', 8))
            # self.button3.grid(row=2, column=0, columnspan=2, pady=(10,10), padx=(20,20))

            self.frame4 = customtkinter.CTkFrame(self.tab1, height=50, width=100)
            # self.frame4 = tk.Frame(self.tab1, bg='yellow', bd=0, height=50, width=100)
            self.frame4.pack(padx=0, pady=0, side='bottom', fill='x')
            # self.button4 = tk.Button(self.frame4, text="Test Mouse", command=self.testmouse, font=('Helvetica', 8))
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


    def resumebutton(self):
        self.pause = not self.pause
        print(f'resumebutton pressed .. {self.pause}')
        if self.pause:
            self.button.configure(text='Resume', fg_color='tomato')
            self.runesolver.disablerune()
        else:
            self.button.configure(text='Pause', fg_color='lime')
            self.runesolver.enablerune()

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
                # canvas_width=minimapX-8
                # canvas_height=minimapY-63
                initial_line_position = self.canvas_width / 2

        print(f'adjustbutton: {self.canvas_width=} {self.canvas_height=}')
        # self.vertical_line = self.canvas.create_line(initial_line_position, 2, initial_line_position, self.canvas_height, fill="red", width=2)
        self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, height, fill="red", width=2)    
        self.line_position_slider.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position(self.line_position_slider.get())
        
        # self.vertical_line2 = self.canvas.create_line(initial_line_position, 2, initial_line_position, self.canvas_height, fill="yellow", width=2)
        self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, height, fill="yellow", width=2)    
        self.line_position_slider2.configure(to=self.canvas_width, width=self.canvas_width)
        self.update_line_position2(self.line_position_slider2.get())
        
        # self.vertical_line3 = self.canvas.create_line(2, initial_line_position, self.canvas_height, initial_line_position, fill="lime", width=2)
        self.vertical_line3 = self.canvas.create_line(self.canvas_width, self.initial_line_position3, 2, self.initial_line_position3, fill="lime", width=2)
        self.line_position_slider3.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position3(self.line_position_slider3.get())

        # self.vertical_line4 = self.canvas.create_line(2, initial_line_position, self.canvas_height, initial_line_position, fill="lightblue", width=2)
        self.vertical_line4 = self.canvas.create_line(self.canvas_width, self.initial_line_position4, 2, self.initial_line_position4, fill="lightblue", width=2)
        self.line_position_slider4.configure(from_=self.canvas_height, height=self.canvas_height*1.2)
        self.update_line_position4(self.line_position_slider4.get())
        
        # self.update_line_position(allpresets[2])
        # self.update_line_position2(allpresets[3])
        # self.update_line_position3(allpresets[4])
        # self.update_line_position4(allpresets[5])
        self.line_position_slider.set(self.line_position_slider.get())
        self.line_position_slider2.set(self.line_position_slider2.get())
        self.line_position_slider3.set(self.line_position_slider3.get())
        self.line_position_slider4.set(self.line_position_slider4.get())
        # button_adjustminimap
        # print(f'{self.rotation=}')
        print(f'{self.line_position_slider=} {self.line_position_slider2=} {self.line_position_slider3=} {self.line_position_slider4=}')
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
        )

        # background_image = Image.open("bumblebee.gif")
        # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_label = tk.Label(root, image=background_photo)
        # background_label.place(relwidth=1, relheight=1)
        # background_label.image = background_photo
        # root.configure(bg='orange')
        # frame2.config(bg='', bd=0)
        # self.root.resizable(False,False)

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
        # print(value)
    
    def update_line_position2(self, value):
        self.canvas.coords(self.vertical_line2, float(value), 0, float(value), self.canvas_height)
        # print(value)

    def update_line_position3(self, value):
        self.canvas.coords(self.vertical_line3, 0, float(value), self.canvas_width, float(value))
        # print(value)
    
    def update_line_position4(self, value):
        self.canvas.coords(self.vertical_line4, 0, float(value), self.canvas_width, float(value))
        # print(value)

    def reload(self):
        self.pause=True
        # self.stop_event.set()
        # time.sleep(.1)
        print(f'reload: {self.preset=} {self.presettemp=}')
        self.preset=self.presettemp
        print(f'reload: {self.preset=} {self.presettemp=}')
        try:
            allpresets=[]
            with open(f'preset/{self.preset}.json', 'r') as json_file:
                arrays = json.load(json_file)
                print(f'{arrays=}')
            for array in arrays:
                for item in array:
                    print(f'{item=} {type(item)}')
                    allpresets.append(item)
            # allpresets.append(self.minimapX,self.minimapY,self.line_position_slider.get(),self.line_position_slider2.get()
            # ,self.line_position_slider3.get(),self.line_position_slider4.get())
            print(f'{allpresets=}')
            self.minimapX=allpresets[0]
            self.minimapY=allpresets[1]
            self.widthentry.delete(0,tk.END)
            self.widthentry.insert(0,self.minimapX)
            self.heightentry.delete(0,tk.END)
            self.heightentry.insert(0,self.minimapY)
            print(f'reload1: {self.canvas_width=} {self.canvas_height=}')
            self.button_adjustminimap(setimage=True)
            print(f'reload2: {self.canvas_width=} {self.canvas_height=}')
            self.update_line_position(allpresets[2])
            self.update_line_position2(allpresets[3])
            self.update_line_position3(allpresets[4])
            self.update_line_position4(allpresets[5])
            self.line_position_slider.set(allpresets[2])
            self.line_position_slider2.set(allpresets[3])
            self.line_position_slider3.set(allpresets[4])
            self.line_position_slider4.set(allpresets[5])
  

            # self.line_position_slider.configure(to=self.canvas_width,number_of_steps=self.canvas_width-2, width=self.canvas_width)
            # self.line_position_slider2.configure(to=self.canvas_width,number_of_steps=self.canvas_width-2, width=self.canvas_width)
            # self.line_position_slider3.configure(from_=self.canvas_height,number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3)
            # self.line_position_slider4.configure(from_=self.canvas_height,number_of_steps=self.canvas_height-2, height=self.canvas_height*1.3)
            
            # self.label_currentleft.config(text=f"current left: {self.line_position_slider.get()}")
            # self.label_currenttop.config(text=f"current left: {self.line_position_slider3.get()}")
            # self.label_currentright.config(text=f"current left: {self.line_position_slider2.get()}")
            # self.label_currentbtm.config(text=f"current left: {self.line_position_slider4.get()}")
            print(f'done reload. ')
        except Exception as e:
            print(f'reading json: {e=}')
        self.left=self.line_position_slider.get()/2
        self.right=self.line_position_slider2.get()/2
        self.top=self.line_position_slider3.get()/2
        self.btm=self.line_position_slider4.get()/2
        # self.g=Game((6,83,self.minimapX,self.minimapY))
        self.character.setup(left=self.left,right=self.right,top=self.top,btm=self.btm)
        # self.character.setup(left=self.left,right=self.right,top=self.top,btm=self.btm,classtype=self.classtype,runesolver=self.runesolver,g=self.g)

        # print(f'thread3 joining. ')
        # self.thread3.join()
        # print(f'thread3 joined. (reload function)')
        # self.thread3 = threading.Thread(target=self.run_thread3)
        # self.stop_event.clear()
        # self.thread3.start()
        # print(f'thread3 started. ')

    def reset(self):
        # global pause
        # pause=True
        self.pause=True
        # for _, stop_event in self.threads:
        #     stop_event.set()
        self.stop_event.set()
        time.sleep(.1)
        # for thread, _ in self.threads:
        #     thread.join()
        # stop_event = threading.Event()
        # thread = threading.Thread(target=self.start_the_main, args=(stop_event,))
        # thread.start()
        # self.threads.append((thread, stop_event))
        self.label_currentleft.config(text=f"current left: {self.line_position_slider.get()}")
        self.label_currentright.config(text=f"current right: {self.line_position_slider2.get()}")
        self.label_currenttop.config(text=f"current top: {self.line_position_slider3.get()}")
        self.label_currentbtm.config(text=f"current btm: {self.line_position_slider4.get()}")
        print(f'thread3 joining. ')
        self.thread3.join()
        print(f'thread3 joined. ')
        self.thread3 = threading.Thread(target=self.run_thread3)
        self.stop_event.clear()
        self.thread3.start()
        print(f'thread3 started. ')
            
    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        print("Selected Tab:", selected_tab)

    def setup_tab2(self):
        framerecord = customtkinter.CTkFrame(self.tab2, fg_color='#81b253')
        framerecord.pack(padx=1, pady=1)
        def new():
            script_name = simpledialog.askstring("New Script", "Enter the name for the new script:")
            # dialog = customtkinter.CTkInputDialog(title="New Script",text="Enter the name for the new script:")
            # script_name = dialog.get_input()
            if script_name:
                script_name=script_name+'.json'
                json_file_names.append(script_name)
                comboboxpreset.set(json_file_names[len(json_file_names)-1])
                comboboxpreset.configure(values=json_file_names)
                self.scripttemp = comboboxpreset.get()
            length=0
            signature=''
            self.labelscript.configure(text=f'script duration: {length}')
            self.labelscript2.configure(text=f'script signature: {signature}')
        buttonnew = customtkinter.CTkButton(framerecord, text="new script", command=new)
        buttonnew.grid(row=2,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        buttonnew.pack(padx=(1,1),pady=(1,1))
        def on_select(event):
            self.scripttemp = comboboxpreset.get()
            print(f'{self.script=} {self.scripttemp=}')
            try:
                with open(f'point/{self.scripttemp}', 'r') as jsonfile:
                    data = json.load(jsonfile)
                    print(f'{data=}')
                    self.pointx=data[0]
                    self.pointy=data[1]
                    labelpointa.configure(text=f'({self.pointx}, {self.pointy})')            
                length=0
                signature=''
                with open(f'script/{self.scripttemp}', 'r') as jsonfile:
                    data = json.load(jsonfile)            
                    for index, action in enumerate(data):
                        if action['type']=='keyUp':
                            signature+=action['button']
                    length=round(data[-1]['time'],4)
                self.labelscript.configure(text=f'script duration: {length}')
                self.labelscript2.configure(text=f'script signature: {signature}')
            except Exception as e:
                self.labelscript.configure(text=f'script duration: ')
                self.labelscript2.configure(text=f'script signature: ')
        folder_path = "script"
        file_list = os.listdir(folder_path)
        json_file_names = [file for file in file_list if file.endswith(".json")]
        # json_file_names = [os.path.splitext(file)[0] for file in json_files]
        comboboxpreset = customtkinter.CTkComboBox(framerecord, values=json_file_names, state="readonly",command=on_select,justify='center')
        # comboboxpreset.grid(row=0,column=0,padx=(1,1), pady=(1,1), sticky=tk.NW)
        comboboxpreset.pack(padx=(1,1), pady=(1,1))
        comboboxpreset.set(json_file_names[json_file_names.index(self.script)])
        def clock():
            if self.recordstatus:
                return
            else:
                # hour2=time.strftime('%H')
                # hour=time.strftime('%I')
                # minute=time.strftime('%M')
                # second=time.strftime('%S')
                # day=time.strftime('%A')
                # am_pm=time.strftime('%p')
                # time_label.configure(text=hour+':'+minute+':'+second)
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
                # self.recordstatus=not self.recordstatus
                # record_button.configure(fg_color='#55eecc', text='Record',state='normal')
                # for value in self.input_events:
                #     print(f'{value=}')
                # self.thread7.join()
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
        # buttonsave.grid(row=3,column=0,padx=(1,1),pady=(1,1), sticky=tk.NW)
        buttonsave.pack(padx=(1,1),pady=(1,1))
        framescript = customtkinter.CTkFrame(self.tab2, fg_color='#81b253')
        framescript.pack(padx=1, pady=1)
        length=0
        signature=''
        with open(f'script/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)            
            for index, action in enumerate(data):
                if action['type']=='keyUp':
                    signature+=action['button']
            length=round(data[-1]['time'],4)
        self.labelscript=customtkinter.CTkLabel(framescript,text=f'script duration: {length}', text_color="#010101",wraplength=550,justify='left')
        self.labelscript.pack(padx=1,pady=1)
        self.labelscript2=customtkinter.CTkLabel(framescript,text=f'script signature: {signature}', text_color="#010101",wraplength=550,justify='left')
        self.labelscript2.pack(padx=1,pady=1)
        def setpointa():
            g_variable = self.g.get_player_location()
            self.pointx, self.pointy = (None, None) if g_variable is None else g_variable
            labelpointa.configure(text=f'({self.pointx}, {self.pointy})')
        buttonsetpointa = customtkinter.CTkButton(framescript, text="set point A", command=setpointa)
        buttonsetpointa.pack(padx=1, pady=1)
        labelpointa=customtkinter.CTkLabel(framescript,text=f'', text_color="#010101",wraplength=550,justify='left')
        labelpointa.pack(padx=1,pady=1)
        with open(f'point/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)
            print(f'{data=}')
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
            buttonstop.configure(state='disabled')       
        self.scriptstopsignal=False
        imageknuckles = customtkinter.CTkImage(Image.open("assets/knuckles1.png"),size=(140,140))
        buttonstop = customtkinter.CTkButton(framesonic, text="", command=stop, fg_color='#ea511f', text_color='black',image=imageknuckles,state='disabled')
        # buttonstop = customtkinter.CTkButton(framesonic, text="", command=stop, fg_color='#ff1400', text_color='black',image=imageknuckles)
        buttonstop.pack(padx=(1,1),pady=(1,1))
        def pause():
            self.scriptpausesignal=not self.scriptpausesignal
            buttonstop.configure(state='normal') if self.scriptpausesignal else buttonstop.configure(state='disabled')
        self.scriptpausesignal=False
        imagetails = customtkinter.CTkImage(Image.open("assets/tails1.png"),size=(140,140))
        buttonpause = customtkinter.CTkButton(framesonic, text="", command=pause, fg_color='#f1bf1f', text_color='black',image=imagetails,state='disabled')
        # buttonpause = customtkinter.CTkButton(framesonic, text="", command=pause, fg_color='#f1b000', text_color='black',image=imagetails)
        buttonpause.pack(padx=(1,1),pady=(1,1))
        def playback():
            self.thread8 = threading.Thread(target=self.run_thread8)
            self.thread8.start()
            buttonplayback.configure(state='disabled')
            buttonpause.configure(state='normal')
            buttonstop.configure(state='disabled')
        imagesonic = customtkinter.CTkImage(Image.open("assets/sonic1.png"),size=(140,140))
        buttonplayback = customtkinter.CTkButton(framesonic, text="", command=playback, fg_color='#0d7adf', text_color='black',image=imagesonic)
        buttonplayback.pack(padx=(1,1),pady=(1,1))


    def realrecord(self):
        self.unreleased_keys=[]
        self.input_events=[]
        def on_press(key):
            if key in self.unreleased_keys:
                return
            else:
                self.unreleased_keys.append(key)
            try:
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
                # Stop keyboard listener                
                self.recordstatus=not self.recordstatus
                self.record_button.configure(fg_color='#55eecc', text='Record',state='normal')
                signature=''
                for value in self.input_events:
                    print(f'{value=}')
                    if value['type']=='keyUp':
                        if 'Key' in value['button']:
                            signature+=value['button'].replace('Key','')
                        else:
                            signature+='.'+value['button']
                length=round(self.input_events[-1]['time'],4)
                self.labelscript.configure(text=f'script duration: {length}')
                self.labelscript2.configure(text=f'script signature: {signature}')
                new_array_temp=[]
                for index, action in enumerate(self.input_events):
                    button = action['button']
                    key = self.convertKey(button)
                    if key is not None:
                        self.input_events[index]['button'] = key
                        # print(f'{key=} {index=}')
                        if key == 'esc':
                            pass
                        else:
                            new_array_temp.append(action)
                self.input_events=new_array_temp
                # for index, action in enumerate(self.input_events):
                #     print(f"{action['button']}")                
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
            print(f'finish after raise1')
        print(f'finish after raise2')

    async def playback(self):
        print(f'starting script {self.script} in 1 ..')
        time.sleep(1)
        with open(f'script/{self.script}', 'r') as jsonfile:
            data = json.load(jsonfile)
            while True:
                time.sleep(1) # testing 
                for index, action in enumerate(data):
                    print(f'running: {index=} {action=}')
                    if self.scriptpausesignal:                        
                        print(f'script is paused .. ')
                        while self.scriptpausesignal:
                            if self.scriptstopsignal:
                                return
                            # do nothing
                            time.sleep(1)
                            if self.stop_event.is_set():
                                return
                        print(f'script resumed ..')

                    # if perf_counter()-nowtime>60000:
                        # checkrune=True
                    # if index%50==0 and checkrune==True:
                    #     self.runesolver.runechecker(self.g)
                    # if allowed:
                        # pass
                    # else:
                        # if changechannel:
                            # await change_channel2(g)
                            # time.sleep(2)
                            # while still_in_zakum_map2(g):
                                # await adjustportal2(g,spot=21,distx=10.5,docorrection=True)
                                # await upp()
                                # await upr()
                                # time.sleep(1)
                            # time.sleep(1)
                            # print(f'checking red dot ..')
                            # await red_dot()
                            # print(f'checking red dot finished ..')
                            # time.sleep(1)
                            # changechannel = False
                        # elif liedetector:
                        #     myvariable = True
                        #     t = time.localtime()
                        #     currenttime = time.strftime("%H:%M:%S", t)
                        #     print(f'oskillsigtermpos2 {currenttime}')            
                        #     # os.kill(os.getpid(), signal.SIGTERM)
                        # else:
                            # await self.runesolver.gotorune(self.g)
                            # await random.choice([rightjumpjumpattack, leftjumpjumpattack])()
                            # time.sleep(1.5)
                            # rune = runechecker(g)
                            # print(f'here shows previous rune solver success or missed. True means still got rune. False means rune is solved. {rune = }')
                            # nowtime = perf_counter()
                            # checkrune=rune
                        # allowed = True
                        # reset = True
                        # unlock()
                        # pass
                    # with lock:
                    # for i in range(1):
                        # if self.myvariable:
                            # send5('00')
                            # while (myvariable):
                                # time.sleep(2)
                                # print('playactions == blocked: (new feature: sleeping(2))')
                                # os.system("pause")
                                # r = random.randint(500,1500)
                                # r /= 1000
                                # sleep(r)
                                # print('playactions == released: (new feature: sleeping(2))')
                                # print('playactions == released: (new feature: sleeping(2))', r)
                                # if stop_event.is_set():
                                    # sendnclose()
                                    # global stop_flag
                                    # stop_flag = True
                                    # return
                            # pass
                        # else:
                        #     pass
                    if action['type'] == 'keyDown':
                        if action['button'] == 'f9':
                            print('is_f9_bruh')   
                            # await adjustportallimen2(g, spot=12.5, distx=103.5, docorrection=False, test=False)  #
                            await self.adjustcharacter(self.pointx,self.pointy)
                        if action['button'] == 'f10':
                            print('is_f10_bruh')
                            # await self.adjustcharacter()
                        key = action['button']
                        print(f'press {key=}')
                        keydown(key)
                        # presskey(key)
                    elif action['type'] == 'keyUp':
                        key = action['button']
                        print(f'release {key=}')
                        keyup(key)
                        # await sleep(1.)
                        # releasekey(key)
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
                    print(f'sleep={elapsed_time=}')
                    await sleep(elapsed_time)

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

    async def adjustcharacter(self,a=10,b=10):
        while True:
            if self.scriptpausesignal:
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

    def setup_tab3(self):
        # welcome to the ultimate tab3.. 
        # self.framedesign = tk.Frame(self.tab3, bg='#a132f3', bd=0)
        # self.framedesign = tk.Frame(self.tab3, bg='#f1f2f3', bd=0)
        # self.framedesign.pack(padx=0, pady=0)
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
        # num_json_files = len(json_files)
        # print("Number of JSON files:", num_json_files)
        # print("File names:", json_file_names)
        # print("json_files:", json_files)
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
                    print(f'{arrays=}')
                for array in arrays:
                    print(f'{array=}')
                    add_input_field(loader=True,data=array)
            except Exception as e:
                print(f'reading json: {e=}')
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
        # self.framedesign2 = tk.Frame(self.tab3, bg='#f1f2f3', bd=0)
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
            print(f'saved platform. ')
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
        # framebutton = tk.Frame(frametelegram, bg='#e47ac3', bd=0)
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
        pass

    def setup_tab6(self):        
        # self.framesettings = tk.Frame(self.tab6, bg='#a1b2c3', bd=0)
        self.framesettings = tk.Frame(self.tab6, bg='#f1f2f3', bd=0)
        self.framesettings.pack(padx=0, pady=0)
        # self.framesettings.columnconfigure(0, weight='1') # not sure bout this
        # self.framesettings.rowconfigure(0, weight='1') # not sure bout this
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
        # options = ['flashjump', 'teleport', 'nightlord']        
        folder_path = "classtype"
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith(".py")]
        json_file_names = [os.path.splitext(file)[0] for file in json_files]
        self.comboboxclasstype = ttk.Combobox(self.framesettings, values=json_file_names, state="readonly", width=17)
        self.comboboxclasstype.grid(row=7, column=1, padx=1, pady=1)
        # self.comboboxclasstype.set(options[1]) if self.classtype=='teleport' else self.comboboxclasstype.set(options[0])
        self.comboboxclasstype.set(json_file_names[json_file_names.index(self.classtype)])
        self.comboboxclasstype.bind("<<ComboboxSelected>>", on_select)
        self.labelportal = tk.Label(self.framesettings, anchor='w', justify='left', text="portal: ")
        self.labelportal.grid(row=8, column=0, padx=1, pady=1, sticky='w')
        def on_checkbox_clicked():
            self.portaldisabled=False if checkbox_var.get() else True
            print(f"Checkbox is checked {checkbox_var=} {self.portaldisabled=} {checkbox_var.get()=}")
        checkbox_var = tk.BooleanVar(value=False) if self.portaldisabled else tk.BooleanVar(value=True)
        self.checkboxportal = tk.Checkbutton(self.framesettings, text="", variable=checkbox_var, command=on_checkbox_clicked, font=('Arial', 10)) ## not sure bout this
        self.checkboxportal.grid(row=8, column=1, padx=0, pady=0, sticky='w')


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
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        # refreshkeybind()
        # self.character.change_ac_type(Teleport()) if self.classtype=='teleport' else self.character.change_ac_type(Flashjump())
        # self.character.change_ac_type(self.classtype)
        self.character.setup(
            left=self.line_position_slider.get()/2,
            right=self.line_position_slider2.get()/2,
            top=self.line_position_slider3.get()/2,
            btm=self.line_position_slider4.get()/2,
            classtype=self.classtype,
            runesolver=self.runesolver,
            g=self.g,
            rotation=self.rotation,
        )
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
        print("Token:", token)
        if token == '0':
            return
        response = requests.get('https://api.telegram.org/bot'+token+'/getUpdates')
        if response.status_code == 200:
            # Parse and print the JSON content
            json_data = response.json()
            print(f'{json_data=}')
            # formated = json.dumps(json_data, indent=2)
            # print("Returned JSON:")
            # print(formated)
            if json_data['result']:
                chat_id = json_data['result'][0]['message']['chat']['id']
                print(f'{chat_id = }')
                # 6871179594:AAH6ZiIEPyfmGQhgGp1bsCy3PvhA42rtyfk
                img = self.g.get_screenshot()
                print(f'{type(img)}')
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
        print(f'{x} {y} {w} {h}')
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
        print("Closing the window")
        #
        self.pause=True
        self.scriptpausesignal=True
        # # Add your code here to run before closing the window
        # # config.add_section('main')
        # self.config.set('main', 'key1', 'value1')
        # self.config.set('main', 'key2', 'value2')
        # self.config.set('main', 'key3', 'value3')
        # self.config.set('main', 'minimapX', str(self.minimapX))
        # self.config.set('main', 'minimapY', str(self.minimapY))
        # self.config.set('main', 'initial_line_position', str(self.line_position_slider.get()))
        # self.config.set('main', 'initial_line_position2', str(self.line_position_slider2.get()))
        # self.config.set('main', 'initial_line_position3', str(self.line_position_slider3.get()))
        # self.config.set('main', 'initial_line_position4', str(self.line_position_slider4.get()))
        # self.config.set('main', 'initial_line_position', str(self.left))
        # self.config.set('main', 'initial_line_position2', str(self.right))
        # self.config.set('main', 'initial_line_position3', str(self.top))
        # self.config.set('main', 'initial_line_position4', str(self.btm))
        self.config.set('main', 'profile', str(self.profile))
        self.config.set('main', 'preset', str(self.preset))
        self.config.set('main', 'script', str(self.script))
        self.config.set('main', 'rotation', str(self.rotation))
        # self.config.set('main', 'portaldisabled', str(self.portaldisabled))
        self.config2.set('telegram', 'token', str(self.TOKEN))
        self.config2.set('telegram', 'chat_id', str(self.chat_id))
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        with open('secret.ini', 'w') as f:
            self.config2.write(f)            
        # # for input_field in input_fields:
        # #     entry, entry2, entry3 = input_field[1].get(), input_field[2].get(), input_field[3].get()
        # #     platforms.append([entry, entry2, entry3])
        # # self.profile = comboboxclasstype.get()
        
        # allpresets=[]
        # allpresets.append([self.minimapX,self.minimapY,self.line_position_slider.get(),self.line_position_slider2.get()
        # ,self.line_position_slider3.get(),self.line_position_slider4.get()])
        # with open(f'preset/{self.preset}.json', 'w') as json_file:
        #     json.dump(allpresets, json_file, indent=4)
        # self.canvasimageholdertemp.save(f'image/{self.preset}.png')
        # print(f'saved preset. ') 
        #
        self.stop_event.set()
        # for _, stop_event in self.threads:
        #     stop_event.set()
        # for thread, _ in self.threads:
        #     thread.join()
        self.telegram_keep_alive = False
        # self.root.destroy()
        self.destroy()
        self.thread1.join()
        print(f'thread1 joined. ')
        # self.thread2.join()
        # print(f'thread2 joined. ')
        self.thread3.join()
        print(f'thread3 joined. ')
        self.thread6.join()
        print(f'thread6 joined. ')
        # self.thread7.join()
        # print(f'thread7 joined. ')
        # self.thread8.join()
        # print(f'thread8 joined. ')



    # def on_button_click():
    #     stop_event = threading.Event()
    #     thread = threading.Thread(target=start_the_main, args=(stop_event,))
    #     thread.start()
    #     threads.append((thread, stop_event))


    # async def start_telegram():
    #     application = Application.builder().token(TOKEN).build()
    #     application.add_handler(CommandHandler('start', start_command))
    #     # app.add_handler(CommandHandler('help', help_command))
    #     # app.add_handler(CommandHandler('custom', custom_command))
    #     # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #     application.add_error_handler(error)
    #     async with application:
    #         await application.initialize() # inits bot, update, persistence
    #         await application.start()
    #         await application.updater.start_polling()
    

    # def start_the_main(stop_event):
    #     g = Game((8, 63, minimapX, minimapY)) # 
    #     loop = asyncio.new_event_loop()
    #     # loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     # loop.create_task(start_telegram())
    #     # loop.run_until_complete(start_telegram())
    #     # loop.run_until_complete(main(

    #     loop.create_task(main(
    #         stop_event, 
    #         float(line_position_slider.get()), 
    #         float(line_position_slider2.get()), 
    #         float(line_position_slider3.get()), 
    #         float(line_position_slider4.get()), 
    #         g
    #     ))
    #     loop.run_forever()
    #     # await application.updater.stop()
    #     # await application.stop()
    #     # await application.shutdown()
    #     loop.close()

    # def entry_focus_in(event):
    #     if entry1.get()=="Enter x...":
    #         entry1.delete(0,'end')
    #         entry1.config(fg='Black')

    # def entry_focus_out(event):
    #     if entry1.get()=="":
    #         entry1.insert(0,'Enter x...')
    #         entry1.config(fg='gray')

    # def entry2_focus_in(event):
    #     if entry2.get()=="Enter y...":
    #         entry2.delete(0,'end')
    #         entry2.config(fg='Black')

    # def entry2_focus_out(event):
    #     if entry2.get()=="":
    #         entry2.insert(0,'Enter y...')
    #         entry2.config(fg='gray')





    

    # def start_the_main2(stop_event):
    #     # loop = asyncio.new_event_loop()
    #     loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(telegrammain(
    #         stop_event,
    #     ))
    #     loop.create_task(telegrammain(stop_event))
    #     # loop.close()



async def main2():
    # mytkinter = TkinterBot()
    # await mytkinter.telegram_run()
    # asyncio.run(mytkinter.telegram_run())
    # mytkinter.tkinter_run()

    # TOKEN = '6871179594:AAH6ZiIEPyfmGQhgGp1bsCy3PvhA42rtyfk'
    # application = Application.builder().token(TOKEN).build()
    # application.add_handler(CommandHandler('start', start_command))
    # # app.add_handler(CommandHandler('help', help_command))
    # # app.add_handler(CommandHandler('custom', custom_command))
    # # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # application.add_error_handler(error)    

    # Run application and other_application() within the same event loop
    # async with application:
    #     await application.initialize() # inits bot, update, persistence
    #     await application.start()
    #     await application.updater.start_polling()
    #     await asyncio.sleep(60)
    
    mytkinter = TkinterBot()
    mytkinter.start_threads()
    mytkinter.init_tkinter()
    mytkinter.mainloop()

    print('done!')


if __name__ == "__main__":    
    # loop = asyncio.get_event_loop()
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main2())
    
    # mytkinter = TkinterBot()
    # # await mytkinter.telegram_run()
    # # asyncio.run(mytkinter.telegram_run())    
    # mytkinter.start_threads()
    # mytkinter.wait_for_threads()
    asyncio.run(main2())
    # # time.sleep(10) #????????
    pass
