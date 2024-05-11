import random
import time
from time import perf_counter
from configparser import ConfigParser
# from initinterception import interception, move_to, move_relative, left_click, keydown, keyup, sleep
from initinterception import keydown, keyup, keyupall, sleep
import win32gui
from PIL import ImageGrab
import json
import numpy as np
import requests














class Action:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.atk = self.config.get('keybind', 'attack')
        self.jump = self.config.get('keybind', 'jump')
        self.teleport = self.config.get('keybind', 'teleport')
        self.ropeconnect = self.config.get('keybind', 'ropeconnect')
        self.npc = self.config.get('keybind', 'npc')
        self.fountainkey = self.config.get('keybind', 'fountainkey')
        self.ccbutton = self.config.get('keybind', 'ccbutton')
        self.bossui = self.config.get('keybind', 'bossui')
        self.ardent = self.config.get('keybind', 'ardent')
        self.ipaddress = self.config.get('main', 'ipaddress')
        self.offsety=10
        self.offsetx=10
        ## for main rotation
        self.top=10.0
        self.left=10.0
        self.right=10.0
        self.btm=10.0 
        ## for stormwing map
        self.stop=29.0
        self.sleft=35.0 # 18.0 # 27.0
        self.sright=130 # 125.0 # 135.0 140.0 132.5
        self.sbtm=58.0 # 54.5
        self.runesolver=None
        self.g=None
        ## timer variables goes here        
        self.randomlist = ['z', 'x', 'c', 'space', '2', '3', '0', 'f9', 'w', 'e', 'r', 't', 's', 'd', 'f', 'v']
        # self.randomlist = []
        self.cosmicshowerplanttimer0=0
        self.cosmicshowerplanttimer=0
        self.cosmicshowerplant=True
        self.fountaintimer0=0
        self.fountaintimer=0
        self.fountain=True
        self.randommtimer0=0
        self.randommtimer=0
        self.runetimer0=0
        self.runetimer=0
        self.checkrune=True
        self.solverune=True
        self.now=0
        ## misc. others. 
        self.replaceropeconnect=False
        self.stoprune=False
        self.maplehwnd=None # somehow only using in runesolver3()
        ## enter portal algorithm variable goes here
        self.goingtoportal=False
        self.gotoportal1=False
        self.gotoportal2=False
        self.gotoportal3=False
        self.gotoportal4=False
        self.tries=0
        self.plb=73.5 # portal left boundary
        self.prb=74.5 # portal right boundary
        self.plbm2=self.plb-2 # portal left boundary minus two, 71.5
        self.prbp2=self.prb+2 # portal right boundary plus two, 76.5
        self.successthreshold=180.5 # what will be the coordinate of your character if successfully entered portal. 
        self.preventgotonextmap=56.5 # if there is a goto next map portal, put here
        ## all the entry goes here
        self.rotation_list = ['default']
        self.rotation='default'
        self.rotation_mapping = {
            'default': self.clockwise,
        }  
        self.rotation='default'

    def setup(self,runesolver,g,rotation,maplehwnd):
        if runesolver is not None:
            self.runesolver=runesolver
        if rotation is not None:
            self.rotation=rotation
        if g is not None:
            self.g=g
        if maplehwnd is not None:
            self.maplehwnd=maplehwnd
        
    async def perform_next_attack(self, x, y):
        # await self.limen1_7(x,y)
        # await self.clockwise(x,y)
        print(f'{self.rotation=}')
        await self.rotation_mapping[self.rotation](x,y)
        
    def get_rotation_list(self):
        return self.rotation_list
        
    def set_rotation(self, rotation):
        self.rotation = rotation
        print(f'{self.rotation=}')
    
    def refreshkeybind(self):
        self.config.read('settings.ini')
        self.atk = self.config.get('keybind', 'attack')
        self.jump = self.config.get('keybind', 'jump')
        self.teleport = self.config.get('keybind', 'teleport')
        self.ropeconnect = self.config.get('keybind', 'ropeconnect')
        self.npc = self.config.get('keybind', 'npc')
        
    def disablerune(self):
        self.stoprune=True

    def enablerune(self):
        self.stoprune=False

    async def sleeprandom(self,x=31,y=101):
        r = random.randint(x, y)
        r /= 1000
        await sleep()

    async def escp(self,x=31,y=101):
        keydown('esc')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def escr(self,x=31,y=101):
        keyup('esc')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def escpr(self,x=31,y=101):
        await self.escp()
        await self.escr()

    async def enterp(self,x=31,y=101):
        keydown('enter')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def enterr(self,x=31,y=101):
        keyup('enter')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def enterpr(self,x=31,y=101):
        await self.enterp()
        await self.enterr()

    def enterp_special(self,x=31,y=101):
        keydown('enter')
        r = random.randint(x, y)
        r /= 1000
        time.sleep(r)

    def enterr_special(self,x=31,y=101):
        keyup('enter')
        r = random.randint(x, y)
        r /= 1000
        time.sleep(r)

    def enterpr_special(self,x=31,y=101):
        self.enterp_special(x,y)
        self.enterr_special(x,y)

    async def ccbuttonp(self,x=31,y=101):
        keydown(self.ccbutton)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ccbuttonr(self,x=31,y=101):
        keyup(self.ccbutton)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def ccbuttonpr(self,x=31,y=101):
        await self.ccbuttonp()
        await self.ccbuttonr()

    async def bossuip(self,x=31,y=101):
        keydown(self.bossui)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def bossuir(self,x=31,y=101):
        keyup(self.bossui)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def bossuipr(self,x=31,y=101):
        await self.bossuip()
        await self.bossuir()

    async def ardentp(self,x=31,y=101):
        keydown(self.ardent)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ardentr(self,x=31,y=101):
        keyup(self.ardent)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def ardentpr(self,x=31,y=101):
        await self.ardentp()
        await self.ardentr()

    async def leftp(self,x=31,y=101):
        keydown('left')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def leftr(self,x=31,y=101):
        keyup('left')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def leftpr(self,x=31,y=101):
        await self.leftp()
        await self.leftr()

    async def rightp(self,x=31,y=101):
        keydown('right')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def rightr(self,x=31,y=101):
        keyup('right')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def rightpr(self,x=31,y=101):
        await self.rightp()
        await self.rightr()

    async def upp(self,x=31,y=101):
        keydown('up')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def upr(self,x=31,y=101):
        keyup('up')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def uppr(self,x=31,y=101):
        await self.upp()
        await self.upr()

    async def downp(self,x=31,y=101):
        keydown('down')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def downr(self,x=31,y=101):
        keyup('down')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def downpr(self,x=31,y=101):
        await self.downp()
        await self.downr()

    async def jumpp(self,x=31,y=101):
        keydown(self.jump)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def jumpr(self,x=31,y=101):
        keyup(self.jump)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def jumppr(self,x=31,y=101):
        await self.jumpp()
        await self.jumpr()

    ## additional patch for extra key buttons. 

    async def ctrlp(self,x=31,y=101):
        keydown('ctrl')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ctrlr(self,x=31,y=101):
        keyup('ctrl')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ctrlpr(self,x=31,y=101):
        await self.ctrlp()
        await self.ctrlr()

    async def bp(self,x=31,y=101):
        keydown('b')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def br(self,x=31,y=101):
        keyup('b')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def zp(self,x=31,y=101):
        keydown('z')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def zr(self,x=31,y=101):
        keyup('z')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def xp(self,x=31,y=101):
        keydown('x')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def xr(self,x=31,y=101):
        keyup('x')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def cp(self,x=31,y=101):
        keydown('c')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def cr(self,x=31,y=101):
        keyup('c')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def vp(self,x=31,y=101):
        keydown('v')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def vr(self,x=31,y=101):
        keyup('v')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def ap(self,x=31,y=101):
        keydown('a')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ar(self,x=31,y=101):
        keyup('a')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def sp(self,x=31,y=101):
        keydown('s')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def sr(self,x=31,y=101):
        keyup('s')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def dp(self,x=31,y=101):
        keydown('d')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def dr(self,x=31,y=101):
        keyup('d')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
        
    async def fp(self,x=31,y=101):
        keydown('f')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def fr(self,x=31,y=101):
        keyup('f')
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def teleportp(self,x=31,y=101):
        keydown(self.teleport)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def teleportr(self,x=31,y=101):
        keyup(self.teleport)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def attackp(self,x=31,y=101):
        keydown(self.atk)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def attackr(self,x=31,y=101):
        keyup(self.atk)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ropeconnectp(self,x=31,y=101):
        keydown(self.ropeconnect)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ropeconnectr(self,x=31,y=101):
        keyup(self.ropeconnect)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def ropeconnectpr(self,x=111,y=222,x2=111,y2=222):
        await self.ropeconnectp()
        await self.ropeconnectr()

    async def npcp(self,x=31,y=101):
        keydown(self.npc)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def npcr(self,x=31,y=101):
        keyup(self.npc)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def fountainp(self,x=31,y=101):
        # print(f'{self.fountainkey=}')
        keydown(self.fountainkey)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)

    async def fountainr(self,x=31,y=101):
        keyup(self.fountainkey)
        r = random.randint(x, y)
        r /= 1000
        await sleep(r)
    
    async def leftattack(self):
        print(f'leftattack')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def rightattack(self):
        print(f'rightattack')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def leftattackk(self):
        print(f'leftattackk')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def rightattackk(self):
        print(f'rightattackk')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def goleftattack(self):
        print(f'self.goleftattack')
        await self.leftp()
        await self.teleportp()
        await self.teleportr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def goleftattackk(self):
        print(f'self.goleftattackk')
        await self.leftp()
        await self.teleportp()
        await self.teleportr()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def goattackleft(self):
        print(f'self.goattackleft')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await self.teleportp()
        await self.teleportr()
        await self.leftr()

    async def goattackkleft(self):
        print(f'self.goattackkleft')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.teleportp()
        await self.teleportr()
        await self.leftr()

    async def gorightattack(self):
        print(f'self.gorightattack')
        await self.rightp()
        await self.teleportp()
        await self.teleportr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def gorightattackk(self):
        print(f'self.gorightattackk')
        await self.rightp()
        await self.teleportp()
        await self.teleportr()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def goattackright(self):
        print(f'self.goattackright')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await self.teleportp()
        await self.teleportr()
        await self.rightr()

    async def goattackkright(self):
        print(f'self.goattackkright')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.teleportp()
        await self.teleportr()
        await self.rightr()

    async def goupattack(self):
        print(f'goupattack')
        await sleep(.1)
        await self.upp()
        await self.teleportp()
        await self.teleportr()
        await self.upr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def goupattack_v2(self):
        print(f'goupattack_v2')
        await self.rightp()
        await self.ropeconnectp()
        await self.ropeconnectr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def goupattack_v3(self):
        print(f'goupattack_v3')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        await sleep(.333)
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def upjumpattack(self):
        print(f'upjumpattack')
        await sleep(.1)
        await self.upp()
        await self.teleportp()
        await self.teleportr()
        await self.upr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def godownattack(self):
        print(f'godownattack')
        await self.downp()
        await self.teleportp()
        await self.teleportr()
        await self.downr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)




    async def goleftattack_fjump(self):
        print(f'self.goleftattack_fjump')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def gorightattack_fjump(self):
        print(f'self.gorightattack_fjump')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def goupattack_fjump(self): # adele upjump
        print(f'goupattack_fjump')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def godownattack_fjump(self):
        print(f'godownattack_fjump')
        await self.downp()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.downr()
        
    async def leftwalk(self,x=222,y=333):
        print(f'leftwalk')
        await self.leftp(x,y)
        await self.leftr()

    async def rightwalk(self,x=222,y=333):
        print(f'rightwalk')
        await self.rightp(x,y)
        await self.rightr()
        
    async def downjump(self):
        await self.downp()
        await self.jumpp()
        await self.jumpr()
        await self.downr()

    # polo portal hunting map rotation patch

    async def upjumpup(self):
        print(f'upjumpup')
        await self.jumpp()
        await self.jumpr()
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()

    async def bountyhuntrotation(self):
        print(f'bountyhuntrotation')
        for i in range(5):
            await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft])()
            time.sleep(.502)
        for i in range(5):
            await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright])()
            time.sleep(.502)

    async def bountyhuntrotationv2(self): # adele flash jump
        print(f'bountyhuntrotationv2')
        for i in range(4):
            await self.goleftattack()
            time.sleep(.502)
        for i in range(4):
            await self.gorightattack()
            time.sleep(.502)

    async def castlewallrotation(self):
        print(f'castlewallrotation') 
        await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft, self.leftattack, self.rightattack, self.leftattackk, self.rightattackk])()
        time.sleep(.5)
        await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright, self.leftattack, self.rightattack, self.leftattackk, self.rightattackk])()
        time.sleep(.5)
        # await self.goleftattack()
        # time.sleep(.502)
        await self.upjumpup()
        time.sleep(.802)
        await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft, self.leftattack, self.rightattack, self.leftattackk, self.rightattackk])()
        time.sleep(.5)
        await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright, self.leftattack, self.rightattack, self.leftattackk, self.rightattackk])()
        time.sleep(.5)
        # await self.gorightattack()
        # time.sleep(.502)
        await self.downjump()
        time.sleep(.702)

    async def castlewallrotationv3(self):
        print(f'castlewallrotationv3')
        await self.leftattack()
        time.sleep(.5)
        await self.rightattack()
        time.sleep(.5)
        # await self.goleftattack()
        # time.sleep(.502)
        await self.ropeconnectpr()
        time.sleep(.802)
        await self.leftattack()
        time.sleep(.5)
        await self.rightattack()
        time.sleep(.5)
        # await self.gorightattack()
        # time.sleep(.502)
        await self.downjump()
        time.sleep(.702)

    async def castlewallrotationv2(self):
        print(f'castlewallrotationv2')
        for i in range(2):
            await self.goleftattack()
            time.sleep(.502)
        await self.ropeconnectpr()
        time.sleep(.802)
        for i in range(2):
            await self.gorightattack()
            time.sleep(.502)
        await self.downjump()
        time.sleep(.702)
        await self.attackp()
        await self.attackr()
        time.sleep(.502)

    async def stormwingrotation(self):
        print(f'stormwingrotation')
        for i in range(5):
            await self.goleftattack()
            time.sleep(.502)
        await self.ropeconnectpr()
        time.sleep(.602)
        for i in range(5):
            await self.gorightattack()
            time.sleep(.502)
        for i in range(5):
            await self.downjump()
            time.sleep(.302)

    async def stormwing(self,x,y,goleft,goright):
        if goright:
            if x > self.sright:
                if y < self.sbtm:
                    await self.godownattack()
                    time.sleep(.3)
                    await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft])()
                    time.sleep(.1)
                elif y > self.stop:
                    await self.upjumpattack()
                    time.sleep(.3)
                goright=False
                goleft=True
            else:
                await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright])()
                time.sleep(.3)
            if x < self.sleft: # only if x < left
                if y < self.sbtm:
                    await self.godownattack()
                    time.sleep(.3)
        elif goleft:
            if x < self.sleft: # only if x < left
                if y > self.stop:
                    time.sleep(.1)
                    await self.upjumpattack()
                    time.sleep(.3)
                elif y < self.stop:
                    await self.godownattack()
                    time.sleep(.3)
                    await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright])()
                    time.sleep(.3)
                goright=True
                goleft=False
            else:
                await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft])()
                time.sleep(.3)
            if x > self.sright: # only if x > right
                if y < self.sbtm:
                    await self.godownattack()
                    time.sleep(.3)
        return goleft,goright


    # main rotation
    #     
    async def perform_next_attack(self,x,y):
        if y > self.top and (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x > self.left+self.offsetx:
                if x < self.left+self.offsetx+5:
                    await random.choice([self.leftwalk])()
                else:
                    await random.choice([self.goleftattack, self.goleftattackk])()
            elif x < self.left-self.offsetx:
                if x > self.left-self.offsetx-5:
                    await random.choice([self.rightwalk])()
                else:
                    await random.choice([self.gorightattack, self.gorightattackk])()
            elif x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattack_v3])()
                else:
                    await random.choice([self.goupattack])()
        elif y <= self.top+self.offsety and y > self.top-self.offsety:
            if x < self.right-self.offsetx:
                await random.choice([self.gorightattack, self.gorightattackk])()
            elif x > self.right+self.offsetx:
                await random.choice([self.goleftattack, self.goleftattackk])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.godownattack])()
        elif y > self.top and not (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattack_v3])()
                else:
                    await random.choice([self.goupattack])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.godownattack])()
            else:
                if x < ((self.right-self.left)/2):
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack_v3])()
                    else:
                        await random.choice([self.goupattack])()
                elif x >= ((self.right-self.left)/2):
                    await random.choice([self.godownattack])()
        else:
            await random.choice([self.godownattack])()

    # should this be remove

    

    async def default(self,x,y):
        if y > self.top and (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x > self.left+self.offsetx:
                if x < self.left+self.offsetx+5:
                    await random.choice([self.leftwalk])()
                else:
                    await random.choice([self.goleftattack, self.goleftattackk])()
            elif x < self.left-self.offsetx:
                if x > self.left-self.offsetx-5:
                    await random.choice([self.rightwalk])()
                else:
                    await random.choice([self.gorightattack, self.gorightattackk])()
            elif x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattack_v3])()
                else:
                    await random.choice([self.goupattack])()
        elif y <= self.top+self.offsety and y > self.top-self.offsety:
            if x < self.right-self.offsetx:
                await random.choice([self.gorightattack, self.gorightattackk])()
            elif x > self.right+self.offsetx:
                await random.choice([self.goleftattack, self.goleftattackk])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.godownattack])()
        elif y > self.top and not (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattack_v3])()
                else:
                    await random.choice([self.goupattack])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.godownattack])()
            else:
                if x < ((self.right-self.left)/2):
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack_v3])()
                    else:
                        await random.choice([self.goupattack])()
                elif x >= ((self.right-self.left)/2):
                    await random.choice([self.godownattack])()
        else:
            await random.choice([self.godownattack])()

        await self.post_perform_action(x,y)




            
    async def leftright(self,x,y):
        if self.goleft:
            if x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                await random.choice([self.goupattack])()
                if y > self.top-self.offsety and y <= self.top+self.offsety:
                    self.goright=True
                    self.goleft=False
                print(f'testing: heightdiff={y-self.top}')
            else:
                await random.choice([self.goleftattack, self.goleftattackk])()
        elif self.goright:
            if x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.godownattack])()
                if y > self.btm-self.offsety and y <= self.btm+self.offsety:
                    self.goleft=True
                    self.goright=False
            else:
                await random.choice([self.gorightattack, self.gorightattackk])()
        else:
            print(f'exception coordinates .. please fix asap .. {x=} {y=}')

        await self.post_perform_action(x,y)
        


    ############ TODO: FINISH THIS CHANGE CHANNEL ALGORITHM ############

    async def changechannelthingtemp(self,x,y):
        
        # clocktimer = now - clocktimer0
        # if clocktimer > 1800:
        #     clocktimer0 = now
        #     current_time = datetime.now().time()
        #     if current_time.hour <= 2:
        #         minutechecker=True
        # if minutechecker:
        #     minutetimer = now - minutetimer0
        #     if minutetimer > 60:
        #         minutetimer0 = now
        #         current_time = datetime.now().time()
        #         if current_time.hour == 1:
        #             if current_time.minute >= 55 and current_time.minute <= 59:
        #                 allowed=False
        #                 changechannel=True
        #         if current_time.hour == 2:
        #                 allowed=False
        #                 changechannel=True
        
        # cctimer = now - cctimer0
        # if cctimer > 3000:
        #     cc = True
        #     cctimer0=now
        # if cc:
        #     cc = False
        #     allowed=False
        #     changechannel=True

        # if allowed:
        #     pass
        # else:
        #     send5('00')
        #     goingtoportal, gotoportal1, gotoportal2, gotoportal3, gotoportal4=False,False,False,False,False
        #     if changechannel:
        #         lockit()
        #         setconfirm(False)
        #         print(f'changing channel ..')
        #         await change_channel2(g)
        #         # await change_channel(d)
        #         print(f'changing channel finished ..')
        #         time.sleep(2)
        #         while still_in_zakum_map2(g):
        #         # while still_in_zakum_map(d):
        #             # await adjustportal(d,spot=21,distx=10,docorrection=True)
        #             # await adjustportal2(g,spot=21,distx=10,docorrection=True)
        #             await adjustportal2(g,spot=21,distx=10.5,docorrection=True)
        #             await upp()
        #             await upr()
        #             time.sleep(1)
        #         time.sleep(1)
        #         print(f'checking red dot ..')
        #         await red_dot()
        #         print(f'checking red dot finished ..')
        #         # send3('00')
        #         time.sleep(1)
        #         changechannel = False
        #     elif liedetector:
        #         lockit()
        #         t = time.localtime()
        #         currenttime = time.strftime("%H:%M:%S", t)
        #         print(f'oskillsigtermpos2 {currenttime}')
        #         time.sleep(.1)
        #         send5('00')
        #         time.sleep(1)
        #         os.kill(os.getpid(), signal.SIGTERM)
        #     else:
        #         lockit()
        #         await solve_rune_please2(g)
        #         # await solve_rune_please(d)
        #         await random.choice([rightjumpshikigamitengushift, leftjumpshikigamitengushift])()
        #         time.sleep(1.5)
        #         rune = runechecker(g)
        #         print(f'here shows previous rune solver success or missed. True means still got rune. False means rune is solved. {rune = }')
        #         runetimer0 = perf_counter()
        #     allowed = True
        #     reset = True
        #     unlock()
        #     pass


        pass

    ############### ENTER PORTAL ALGORITHM ###################

    async def portalenterorskip(self,x,y):
        if self.gotoportal1:
            print(f'first {x=}')
            if not self.goingtoportal and not (x >= self.plbm2 and x <= self.prbp2):
                print(f'not goingtoportal ..')
                if x>=46.5 and x<=48.5:
                    await self.rightp()
                    pass
                elif x < self.plb:
                    await self.rightp()
                    await self.upp()
                elif x > self.prb:
                    await self.leftp()
                    await self.upp()
                self.goingtoportal=True
                # continue
                return
            elif x >= self.plbm2 and x <= self.prbp2:
                print(f'goingtoportal equals true ..')
                self.goingtoportal = True
            if self.goingtoportal:
                print(f'start goingtoportal .. ')
                if x < self.preventgotonextmap: # got a portal to other map, prevent that
                    keyupall()
                    print(f'dangerous portal soon. stopping. ')
                    self.gotoportal1=False
                    self.goingtoportal=False
                    self.tries=0
                if x >= self.plbm2 and x <= self.prbp2:
                    print(f'send300 gotoportal1')
                    keyupall()
                    self.gotoportal1=False
                    self.goingtoportal=False
                    self.tries=0
                    await sleep(.1)
                    # while True:
                    for i in range(15): # hopefully don't stucked forever
                        g_variable = self.g.get_player_location() # double checking
                        x, y = (None, None) if g_variable is None else g_variable
                        if x == None:
                            pass
                        else:
                            # if x > 129.5:
                            # if x > 180.5:
                            if x > self.successthreshold:
                                await sleep(.1)
                                print(f'successfully use portal. ')                      
                                break
                            else:
                                print(f'uppr saves, x, {x}')                                        
                                if x < self.plb:
                                    await self.rightp(71,111)
                                    await self.rightr(71,131)
                                elif x > self.prb:
                                    await self.leftp(71,111)
                                    await self.leftr(71,131)
                                await self.uppr()
                                await sleep(.05)
                        # if self.pause:
                        #     keyupall()
                        #     while (self.pause):
                        #         time.sleep(2)
                        #         print('playactions == blocked: (new feature: sleeping(2))')
                        #         print('playactions == released: (new feature: sleeping(2))')
                        #         # if stop_event.is_set():
                        #         #     sendnclose()
                        #         #     stop_flag = True
                        #         #     return
                    # time.sleep(5)
                    # gotoportal2=True
                    # continue
                else:
                    self.tries+=1
                    if self.tries > 90:
                        print(f'tries finished. ')
                        keyupall()
                        self.gotoportal1=False
                        self.goingtoportal=False
                        self.tries=0
        # if gotoportal2:
        #     if not goingtoportal and not (x >= 177.5 and x <= 182.5):
        #         lockit()
        #         if x >= 207.5 and x <=209.5: # right hand side next map portal
        #             await leftp()
        #         elif x < 179.5:
        #             await rightp()
        #             await upp()
        #         elif x > 180.5:
        #             await leftp()
        #             await upp()
        #         goingtoportal=True
        #         continue
        #     elif x >= 177.5 and x <= 182.5:
        #         goingtoportal = True
        #     if goingtoportal:
        #         if x <= 167.5 or x >= 200.5:
        #             await shiftpr()
        #             print(f'tries finished. ')
        #             send5('00')
        #             gotoportal2=False
        #             goingtoportal=False
        #             tries=0
        #         if x >= 177.5 and x <= 182.5:
        #             print(f'send300 gotoportal2')
        #             send5('00')
        #             send5('00')
        #             gotoportal2=False
        #             goingtoportal=False
        #             tries=0
        #             unlock()
        #             await sleep(.1)
        #             # while True:
        #             for i in range(15):
        #                 g_variable = g.get_player_location() # double checking
        #                 x, y = (None, None) if g_variable is None else g_variable
        #                 if x == None:
        #                     pass
        #                 else:
        #                     if x < 68.5:
        #                         await sleep(.1)
        #                         break
        #                     else:                                        
        #                         print(f'uppr saves, x, {x}')
        #                         if x < 179.5:
        #                             await rightp(71,111)
        #                             await rightr(71,131)
        #                         elif x > 180.5:
        #                             await leftp(71,111)
        #                             await leftr(71,131)
        #                         await uppr()
        #                         await sleep(.05)
        #                 if myvariable:
        #                     send5('00')
        #                     while (myvariable):
        #                         time.sleep(2)
        #                         print('playactions == blocked: (new feature: sleeping(2))')
        #                         print('playactions == released: (new feature: sleeping(2))')
        #                         if stop_event.is_set():
        #                             sendnclose()
        #                             stop_flag = True
        #                             return
        #             # time.sleep(5)
        #             # gotoportal1=True
        #             continue
        #         else:
        #             tries+=1
        #             if tries > 90:
        #                 print(f'tries finished. ')
        #                 send5('00')
        #                 gotoportal2=False
        #                 goingtoportal=False
        #                 tries=0
        # if gotoportal3:
        #     if not goingtoportal and not (x >= 188.5 and x <= 193.5):
        #         lockit()
        #         if x < 190.5:
        #             await rightp()
        #             await upp()
        #         elif x > 191.5:
        #             await leftp()
        #             await upp()
        #         goingtoportal=True
        #         continue
        #     elif x >= 188.5 and x <= 193.5:
        #         goingtoportal = True
        #     if goingtoportal:
        #         if x >= 188.5 and x <= 193.5:
        #             print(f'send300 gotoportal3')
        #             send5('00')
        #             send5('00')
        #             gotoportal3=False
        #             goingtoportal=False
        #             tries=0
        #             unlock()
        #             await sleep(.1)
        #             # while True:
        #             for i in range(15):
        #                 g_variable = g.get_player_location() # double checking
        #                 x, y = (None, None) if g_variable is None else g_variable
        #                 if x == None:
        #                     pass
        #                 else:
        #                     # if x < 68.5:
        #                     if y > 60.5: # 70.5
        #                         await sleep(.1)
        #                         break
        #                     else:                                        
        #                         print(f'uppr saves, x, {x}')
        #                         if x < 190.5:
        #                             await rightp(71,111)
        #                             await rightr(71,131)
        #                         elif x > 191.5:
        #                             await leftp(71,111)
        #                             await leftr(71,131)
        #                         await uppr()
        #                         await sleep(.05)
        #                 if myvariable:
        #                     send5('00')
        #                     while (myvariable):
        #                         time.sleep(2)
        #                         print('playactions == blocked: (new feature: sleeping(2))')
        #                         print('playactions == released: (new feature: sleeping(2))')
        #                         if stop_event.is_set():
        #                             sendnclose()
        #                             stop_flag = True
        #                             return
        #             # time.sleep(5)
        #             # gotoportal1=True
        #             continue
        #         else:
        #             tries+=1
        #             if tries > 90:
        #                 print(f'tries finished. ')
        #                 send5('00')
        #                 gotoportal3=False
        #                 goingtoportal=False
        #                 tries=0
        # if gotoportal4:
        #     if not goingtoportal and not (x >= 55.5 and x <= 60.5):
        #         lockit()
        #         if x < 57.5:
        #             await rightp()
        #             await upp()
        #         elif x > 58.5:
        #             await leftp()
        #             await upp()
        #         goingtoportal=True
        #         continue
        #     elif x >= 55.5 and x <= 60.5:
        #         goingtoportal = True
        #     if goingtoportal:
        #         if x >= 55.5 and x <= 60.5:
        #             print(f'send300 gotoportal4')
        #             send5('00')
        #             send5('00')
        #             gotoportal4=False
        #             goingtoportal=False
        #             tries=0
        #             unlock()
        #             await sleep(.1)
        #             # while True:
        #             for i in range(15):
        #                 g_variable = g.get_player_location() # double checking
        #                 x, y = (None, None) if g_variable is None else g_variable
        #                 if x == None:
        #                     pass
        #                 else:
        #                     # if x < 68.5:
        #                     if y > 60.5: # 70.5
        #                         await sleep(.1)
        #                         break
        #                     else:                                        
        #                         print(f'uppr saves, x, {x}')
        #                         if x < 57.5:
        #                             await rightp(71,111)
        #                             await rightr(71,131)
        #                         elif x > 58.5:
        #                             await leftp(71,111)
        #                             await leftr(71,131)
        #                         await uppr()
        #                         await sleep(.05)
        #                 if myvariable:
        #                     send5('00')
        #                     while (myvariable):
        #                         time.sleep(2)
        #                         print('playactions == blocked: (new feature: sleeping(2))')
        #                         print('playactions == released: (new feature: sleeping(2))')
        #                         if stop_event.is_set():
        #                             sendnclose()
        #                             stop_flag = True
        #                             return
        #             # time.sleep(5)
        #             # gotoportal1=True
        #             continue
        #         else:
        #             tries+=1
        #             if tries > 90:
        #                 print(f'tries finished. ')
        #                 send5('00')
        #                 gotoportal4=False
        #                 goingtoportal=False
        #                 tries=0






    ################## REFACTOR GOTORUNE PATCH ###################

    async def runegoupmovement(self,x=31,y=101):
        print(f'runegoupmovement')
        await self.ropeconnectpr()
        # time.sleep(1.7) already sleep in gotorune function

    async def runegodownmovement(self,x=31,y=101):
        print(f'runegodownmovement')
        await self.downjump()
        # time.sleep(1.7) # already sleep in gotorune function

    async def runegoleftmovement(self,x=31,y=101):
        print(f'runegoleftmovement')
        await self.goleftattack_fjump()
        time.sleep(.7)

    async def runegorightmovement(self,x=31,y=101):
        print(f'runegorightmovement')
        await self.gorightattack_fjump()
        time.sleep(.7)

    async def gotorune(self):
        g_variable = self.g.get_rune_location()
        x, y = (None, None) if g_variable is None else g_variable
        if x == None:
            print(f'x==None..continue..means..no..rune..')
            return     
        else:
            print(f'rune location: {x=} {y=}')
            purpdist = x
            lowdist = x - 2
            highdist = x + 2
            height = y + 1  # LOL
        prevhigh = 0
        prevhighcount = 0
        counter = 0
        lastdistance = 0
        lastheight = 0
        theI = 0
        keyupall()
        while (True):
            if self.stoprune:
                return
            while (True):
                print(f'theI {theI}')
                theI += 1
                if theI > 24:
                    print(f'{theI} tries already! are you stucked!? returning .. ')
                    return
                r = random.randint(1, 4)
                r /= 1000
                await sleep(r)
                g_variable = self.g.get_player_location()
                x, y = (None, None) if g_variable is None else g_variable
                if x == None:
                    print(f'x==None..continue..means..no..player..something blocking bruh ..f')
                    r = random.randint(900, 1100)
                    r /= 1000
                    await sleep(r)
                else:
                    break
            print(f'solving rune? 1 ..')
            if (x >= lowdist and x <= highdist):
                print(f'playerx: {x}, playery: {y}, height: {height}, {purpdist =}')
                h1 = 3
                if y >= height-h1 and y <= height+h1:
                    print('already at rune position')
                    r = random.randint(770, 920)
                    r /= 1000
                    await sleep(r)
                    print(f'pressing npc ..')
                    await self.npcp(3,11)
                    await self.npcr()
                    print(f'done pressing npc ..')
                    r = random.randint(1000, 1700)
                    r /= 1000
                    await sleep(r)
                    await self.runesolver3()
                    # runesolver(d)
                    return
                    # break
                else:
                    if y == prevhigh:
                        prevhighcount += 1
                        if prevhighcount > 6:
                            await self.leftp()
                            await self.jumpp()
                            await self.jumpr()
                            await self.leftr()
                    if abs(y - prevhigh) < 15:
                        yinyang=False
                    prevhigh = y
                    if y > height:
                        print(y)
                        print(height)
                        if abs(y-height) < 15:
                            await self.runegoupmovement() # await self.jumpupjumpattack()
                        else:
                            await self.runegoupmovement() # await self.ropeconnectpr()
                        r = random.randint(1000, 1700)
                        r /= 1000
                        await sleep(r)
                    else:
                        print(y)
                        print(height)
                        if abs(y-height<15):
                            await self.runegodownmovement() # await self.downjump()
                        else:
                            await self.runegodownmovement() # await self.downjumpv2()
                        r = random.randint(1000, 1500)
                        r /= 1000
                        await sleep(r)
                    r = random.randint(500, 900)
                    r /= 1000
                    await sleep(r)
            else:
                distance = x - purpdist
                theight = y - height
                print(f'distance: {distance}, {lastdistance}, {purpdist=}, {x=}, ')
                if lastdistance - distance == 0:
                    if lastheight - theight == 0:
                        counter += 1
                        if counter > 55:
                            await self.leftp()
                            await self.jumpp()
                            await self.jumpr()
                            await self.leftr()
                else:
                    counter = 0
                lastdistance = distance
                lastheight = theight
                if distance > 30 or distance < -30:
                    if distance > 30:
                        print('hey distance > 30', distance)
                        # jumpjumpleft()
                        # await adjustportalll(distance)
                        await self.runegoleftmovement() # await self.leftjumpjumpattack()
                    if distance < -30:
                        await self.runegorightmovement() # await self.rightjumpjumpattack()
                elif distance > 0:
                    distances = int(distance * 100 / 2.0)
                    print(f'> 0 {distances}')
                    await self.leftp(distances-50, distances+50)
                    await self.leftr(100, 300)
                    print(f'height: {height}')
                    if height == 32:
                        time.sleep(.6)
                    pass
                elif distance < 0:
                    distances = int(abs(distance) * 100 / 2.0)
                    print(f'< 0 {distances}')
                    await self.rightp(distances-50, distances+50)
                    await self.rightr(100, 300)
                    if height == 32:
                        time.sleep(.6)
                    pass
                elif distance == 0:
                    pass

    async def runesolver3(self):
        now=perf_counter()
        print('solving rune2 ..')
        # hwnd = win32gui.FindWindow(None, "MapleStory")
        position = win32gui.GetWindowRect(self.maplehwnd)
        x, y, w, h = position
        runepos = (x+121, y+143, x+697, y+371) # 800x600
        # runepos = (x+221, y+143, x+797, y+371) # 1074x768
        # runepos = (x+341, y+143, x+917, y+371) # 1280x720
        # runepos = (x+381, y+143, x+957, y+371) # 1366x768
        # runepos = (x+631, y+143, x+1207, y+371) # 1920x1080 # if this coordinate not work, lemme know!
        print(x,y,w,h)
        screenshot = ImageGrab.grab(runepos,all_screens=True)
        # screenshot.show()
        # time.sleep(5)
        img = np.array(screenshot)
        sendjson = {
            'image': img.tolist()
        }
        link = 'http://'+self.ipaddress+':8001/'
        link = link + 'predict'
        r = requests.post(url=link, json=sendjson)
        json_data = json.loads(r.text)
        print(json_data['prediction'])
        sms = json_data['prediction']
        # print(f"{sms}")
        for i in range(len(sms)):
            print(sms[i:i+1])
            # PressKey(captchadict[sms[i:i+1]])
            if sms[i:i+1] == 'u':
                print('up')
                await self.upp(3,11)
                await self.upr(101,171)
            if sms[i:i+1] == 'd':
                print('down')
                await self.downp(3,11)
                await self.downr(101,171)
            if sms[i:i+1] == 'l':
                print('left')
                await self.leftp(3,11)
                await self.leftr(101,171)
            if sms[i:i+1] == 'r':
                print('right')
                await self.rightp(3,11)
                await self.rightr(101,171)
            time.sleep(0.001)
        print(f'{perf_counter()-now=}')


    ############ POST_PERFORM_ACTION ALWAYS PUT AT LAST FOR EASY TO READ ############
    async def post_perform_action(self,x,y):
        self.now = perf_counter()
        self.randomtimer = self.now - self.randomtimer0
        if self.randomtimer > 15:
            self.randomtimer0 = self.now
            # p = random.randint(0, len(self.randomlist)-1)
            code = random.choice(self.randomlist)
            if code is not None:
                print(f'randomiser {code=}')
                await self.send2(code)
                await self.send3(code)
        if self.replaceropeconnect==True:
            if runonce:
                replaceropeconnecttimer0=self.now
                runonce=False
            replaceropeconnecttimer = self.now - replaceropeconnecttimer0
            if replaceropeconnecttimer > 90:
                self.replaceropeconnect=False
                runonce=True
        # self.cosmicshowerplanttimer = self.now - self.cosmicshowerplanttimer0
        # if self.cosmicshowerplanttimer > 59:
        #     self.cosmicshowerplant = True
        # self.fountaintimer = self.now - self.fountaintimer0
        # if self.fountaintimer > 59:
        #     self.fountain = True
        
        ######### RUNETIMER IS NOT NEEDED ANYMORE WE CHECK RUNE CD IN MAIN LOOP ###########3
        # self.runetimer = self.now - self.runetimer0
        # if runetimer > 600: # change to 600 when haste
        # if self.runetimer > 900: # change to 600 when haste
        #     self.checkrune = True
        #     # self.checkrune = False
        # if self.checkrune:
        #     self.solverune = self.runesolver.runechecker(self.g)
        # if self.solverune:
        #     self.solverune=False
        #     await self.runesolver.gotorune(self.g)
        #     await random.choice([self.gorightattack, self.goleftattack])()
        #     time.sleep(1.5)
        #     self.checkrune = self.runesolver.runechecker(self.g)
        #     print(f'here shows previous rune solver success or missed. True means still got rune. False means rune is solved. {self.checkrune = }')
        #     self.runetimer0 = perf_counter()
        # print(f'{x=} {y=} rt={self.runetimer} sr={self.solverune} ft={self.fountaintimer} gl={self.goleft} gr={self.goright}')
        ######### RUNETIMER IS NOT NEEDED ANYMORE WE CHECK RUNE CD IN MAIN LOOP ###########

        print(f'{x=} {y=} ft={self.fountaintimer} gl={self.goleft} gr={self.goright}')






    # randomiser patch

    async def send2(self, code):
        keydown(code)
        r = random.randint(31, 131)
        r /= 1000
        await sleep(r)

    async def send3(self, code):
        keyup(code)
        r = random.randint(31, 131)
        r /= 1000
        await sleep(r)

    # test purpose

    async def testnpc(self):
        await self.npcp()
        await self.npcr()
