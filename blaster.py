import random
import time
from time import perf_counter
# from configparser import ConfigParser
from action import Action
from initinterception import sleep








class Blaster(Action):

    def __init__(self):
        super().__init__()
        self.offsety=5
        self.offsetx=15
        self.goleft=True
        self.goright=False
        self.randomlist = ['v', '7', 'z', '2', '3', '.', 'h', 'w', 'n', 'r', '.', 'd', '.', '.']

        self.cosmicshowerplanttimer0=0
        self.cosmicshowerplanttimer=0
        self.cosmicshowerplant=True

        self.infantrytimer0=0
        self.infantrytimer=24
        self.infantryplant=True

        self.hurricanetimer0=0
        self.hurricanetimer=14
        self.hurricaneplant=True

        self.fountaintimer0=0
        self.fountaintimer=60
        self.fountain=True

        self.spidertimer0=0
        self.spidertimer=250
        self.spider=True

        self.auratimer0=0
        self.auratimer=140
        self.aura=True

        self.origintimer0=0
        self.origintimer=360
        self.origin=True

        self.cctimer0=0
        self.cctimer=3600
        self.cc=False


        self.randommtimer0=0
        self.randommtimer=0

        self.runetimer0=0
        self.runetimer=0
        self.checkrune=True
        self.solverune=True

        self.now=0  
        self.rotation_list = ['default', 'limen1-7','defaultupj','defaultskate']
        self.rotation='default'
        self.rotation_mapping = {
            'default': self.clockwise,
            'limen1-7': self.limen1_7,
            'defaultupj': self.clockwise_Upj,
            'defaultskate': self.clockwiseskate,
        }

    def define(self):
        pass

    def setup(self,runesolver,g,rotation):
        if runesolver is not None:
            self.runesolver=runesolver
        if rotation is not None:
            self.rotation=rotation
        if g is not None:
            self.g=g
        
    async def perform_next_attack(self, x, y):
        print(f'{self.rotation=}')
        await self.rotation_mapping[self.rotation](x,y)
        
    def get_rotation_list(self):
        return self.rotation_list
        
    def set_rotation(self, rotation):
        self.rotation = rotation
        print(f'{self.rotation=}')
    
    # basic 4x direction movement (goleft, goright, gooup, godown)
    async def goleftattack(self):
        # print(f'goleftattack')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.leftr()
    
    

    async def goleftattack2(self):
        # print(f'goleftattack2')
        await self.leftp()
        await self.jumpp(222,388)
        await self.jumpr(3,11)    
        await self.jumpp()
        await self.jumpr()
        await self.attack2p()
        await self.attack2r()
        await self.leftr()

    async def gorightattack(self):
        # print(f'gorightattack')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def gorightattack2(self):
        # print(f'gorightattack2')
        await self.rightp()
        await self.jumpp(222,388)
        await self.jumpr(3,11)
        await self.jumpp()
        await self.jumpr()
        await self.attack2p()
        await self.attack2r()
        await self.rightr()

    async def goupattackupj(self): # adele upjump
        # print(f'goupattack')
        await sleep(.1)
        #await self.jumpp()
        #await self.jumpr()
        # print(f'press ropeconnect once. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        # await self.upp()
        # await self.blastp(31,101)
        # await self.blastr(31,101)
        # await sleep(.255)
        # await self.blastp(31,101)
        # await self.blastr(31,101)
        # await self.upr() 
        await sleep(.025)
        await self.attack2p()
        await self.attack2r()
        await sleep(.1)

    async def fountaincheck(self):
        while self.fountain == True:
                        if self.fountain:
                            await sleep(.1)
                            await random.choice([self.facerightfountain])()
                        self.fountain=False
                        # print('fountain summoned')
                        self.fountaintimer0=perf_counter()
                        await sleep(.9)

    async def cccheck(self):
        while self.cc == True:
                        if self.cc:
                            await sleep(.4)
                            await random.choice([self.cchannel])()
                        self.cc=False
                        print('changing channels')
                        self.cctimer0=perf_counter()
                        await sleep(.72)

    async def spidercheck(self):
        while self.spider == True:
                        if self.spider:
                            await sleep(.1)
                            await random.choice([self.facerightspider])()
                        self.spider=False
                        # print('spider summoned')
                        self.spidertimer0=perf_counter()
                        await sleep(.96)
                        
    async def infantrycheck(self):
        while self.infantryplant == True:
                        if self.infantry:
                                await sleep(.5)
                                await random.choice([self.infantry])()
                        self.infantryplant=False
                        self.infantrytimer0=perf_counter()    
                        
    async def hurricanecheck(self):
        while self.hurricaneplant == True:
                        if self.hurricane:
                                await sleep(.4)
                                await random.choice([self.hurricane])()
                        self.hurricaneplant=False
                        self.hurricanetimer0=perf_counter()    


    async def auracheck(self):
        while self.aura == True:
                        if self.aura:
                            await sleep(.4)
                            await random.choice([self.aurapr])()
                        self.aura=False
                        # print('aura summoned')
                        self.auratimer0=perf_counter()
                        await sleep(.72)

    async def origincheck(self):
        while self.origin == True:
                        if self.origin:
                            await sleep(.5)
                            await random.choice([self.originpr])()
                        self.origin=False
                        # print('origin used')
                        self.origintimer0=perf_counter()
                        

    async def goupattack(self): # adele upjump
        # print(f'goupattack')
        await sleep(.1)
        await self.downp()
        
        # print(f'press ropeconnect once. ')
        await self.jumpp()
        await self.jumpr()
        await self.downr()
        # print(f'attack.  ')
        await self.attack2p()
        await self.attack2r()
        await self.attack2p()
        await self.attack2r()
        await sleep(.1)

    async def skate(self):
        # print(f'skate')
        await self.dbp()
        await self.dbr()
        await sleep(.01)
        await self.fp()
        await sleep(0.025)
        await sleep(.435)
        await self.fr()
        await sleep(0.28)
        await self.jumpb()
        
        
    
    async def godownattack(self):
        # print(f'godownattack')
        await self.downp()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.downr()

    # skating test
    async def goleftskate(self):
        # print(f'goleftskate')
        await self.leftp()
        await self.leftr()
        await self.skate()

    async def gorightskate(self):
        # print(f'gorightskate')
        await self.rightp()
        await self.rightr()
        await self.skate()



    # variation of 4 basic movement to make sequence more randomise.
    async def goleftattackk(self):
        # print(f'goleftattackk')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.leftr()
        
    async def goattackleft(self):
        # print(f'goattackleft')
        await self.leftp()
        await self.attack2p()
        await self.attack2r()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.leftr()

    async def goattackkleft(self):
        # print(f'goattackleft')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.leftr()
    
    async def gorightattackk(self):
        # print(f'gorightattackk')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await self.rightr()
    
    async def goattackright(self):
        # print(f'goattackright')
        await self.rightp()
        await self.attack2p()
        await self.attack2r()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()  
        await self.jumpp()
        await self.jumpr()
        await self.rightr()

    async def goattackkright(self):
        # print(f'goattackkright')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()  
        await self.jumpp()
        await self.jumpr()
        await self.rightr()
        
   

    # soul master actions patch for limen 1-7
    
    async def rightupjump(self):
        # print(f'rightupjump')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()
        await self.rightr(3,11)
        await self.upp()
        await self.blastp()
        await self.blastr()
        await self.upr()
        time.sleep(.1)

    async def leftupjump(self):
        # print(f'leftupjump')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()
        await self.leftr(3,11)
        await self.upp()
        await self.blastp()
        await self.blastr()
        await self.upr()
        time.sleep(.1)

    async def rightjumpattack(self):
        # print(f'rightjumpattack')
        await self.rightp()
        await self.jumpp(191,211)
        await self.jumpr()
        await self.attack2p()
        await self.attack2r()
        await self.rightr()

    async def jumpropeconnectpr(self,x=111,y=222,x2=111,y2=222):
        await self.ropeconnectp(x,y)
        await self.ropeconnectr(x2,y2)

    async def ropeconnectpr(self,x=111,y=222,x2=111,y2=222):
        await self.ropeconnectp(x,y)
        await self.ropeconnectr(x2,y2)

    async def cosmicshower(self):
        r = random.randint(2,4)
        for i in range(r):
            await self.bp(101,177)
            await self.br()

    async def faceleftfountain(self):
        await self.leftp()
        await self.leftr()
        await self.fountainp()
        await self.fountainr()
        time.sleep(.1)

    async def facerightfountain(self):
        await self.rightp()
        await self.rightr()
        await self.fountainp()
        await self.fountainr()
        time.sleep(.1)

    async def cchannel(self):
        time.sleep(5)
        await self.f8p()
        await self.f8r()
        await self.rightp()
        await self.rightr()
        await self.enterp()
        await self.enterr()
        await self.enterp()
        await self.enterr()
        time.sleep(1)

    async def hurricane(self):
        await self.jumpp()
        await self.jumpr()
        await self.hurricanep()
        await self.hurricaner()
        time.sleep(.1)

    async def aurapr(self):
        await self.aurap()
        await self.aurar()
        time.sleep(.1)
    
    async def originpr(self):
        await self.originp()
        await self.originr()
        time.sleep(.1)

    async def hurricanepr(self):
        await self.jumpp()
        await self.jumpr()
        await self.hurricanep()
        await self.hurricaner()
        time.sleep(.1)   

    async def infantry(self):
        await self.infantryp()
        await self.infantryr()
        time.sleep(.1)

    async def faceleftspider(self):
        await self.leftp()
        await self.leftr()
        await self.spiderp()
        await self.spiderr()
        time.sleep(.1)

    async def facerightspider(self):
        await self.rightp()
        await self.rightr()
        await self.spiderp()
        await self.spiderr()
        time.sleep(.1)

    async def walkleft(self,distance=1):
        # print(f'walkleft for {distance=}')
        x=int(distance*88)
        y=int(distance*144)
        await self.leftp(x,y)
        await self.leftr()

            
    async def walkright(self,distance=1):
        # print(f'walkright for {distance=}')
        x=int(distance*88)
        y=int(distance*144)
        await self.rightp(x,y)
        await self.rightr()



    async def limen1_7(self, x, y):
         print ('hi')

    async def post_perform_action(self,x,y):
            self.now = perf_counter()
            self.randommtimer = self.now - self.randommtimer0
            if self.randommtimer > 15:
                self.randommtimer0 = self.now
            # p = random.randint(0, len(self.randomlist)-1)
                code = random.choice(self.randomlist)
            if code is not None:
                # print(f'randomiser {code=}')
                await self.send2(code)
                await self.send3(code)


    async def clockwise(self, x, y):
        try:
            if y > self.top and (y > self.btm - self.offsety and y <= self.btm + self.offsety):
                if x > self.left + self.offsetx:
                    if x < self.left + self.offsetx + 5:
                        await random.choice([self.leftwalk])()
                    else:
                        await random.choice([self.goleftattack, self.goleftattackk])()
                elif x < self.left - self.offsetx:
                    if x > self.left - self.offsetx - 5:
                        await random.choice([self.rightwalk])()
                    else:
                        await random.choice([self.fountaincheck])()
                        await random.choice([self.gorightattack, self.gorightattackk])()
                elif x >= self.left - self.offsetx and x <= self.left + self.offsetx:
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack])()
                    else:
                        await random.choice([self.goupattack])()
                        
            elif y <= self.top + self.offsety and y > self.top - self.offsety:
                if x < self.right - self.offsetx:
                    await random.choice([self.fountaincheck])()
                    await random.choice([self.gorightattack, self.gorightattackk])()
                elif x > self.right + self.offsetx:
                    await random.choice([self.goleftattack, self.goleftattackk])()
                elif x >= self.right - self.offsetx and x <= self.right + self.offsetx:
                    await random.choice([self.spidercheck])()
                    await random.choice([self.godownattack])()
                    
            elif y > self.top and not (y > self.btm - self.offsety and y <= self.btm + self.offsety):
                if x >= self.left - self.offsetx and x <= self.left + self.offsetx:
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack])()
                    else:
                        await random.choice([self.goupattack])()
                        
                elif x >= self.right - self.offsetx and x <= self.right + self.offsetx:
                    await random.choice([self.spidercheck])()
                    await random.choice([self.godownattack])()
                else:
                    if x < ((self.right - self.left) / 2):
                        if self.replaceropeconnect:
                            await random.choice([self.goupattack_v3])()
                        else:
                            await random.choice([self.goupattack])()
                            
                    elif x >= ((self.right - self.left) / 2):
                        await random.choice([self.spidercheck])()
                        await random.choice([self.godownattack])()
            
            else:
                await random.choice([self.spidercheck])()
                await random.choice([self.godownattack])()

            await random.choice([self.auracheck])()
            await random.choice([self.origincheck])()
            await random.choice([self.infantrycheck])()
            await random.choice([self.hurricanecheck])()
            await random.choice([self.cccheck])()
           
            # Update timers
            self.update_timers()
            await self.post_perform_action(x,y)
        except TypeError as e:
            print(f"TypeError occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def post_perform_action(self,x,y):
        self.now = perf_counter()
        self.randommtimer = self.now - self.randommtimer0
        if self.randommtimer > 15:
            self.randommtimer0 = self.now
            # p = random.randint(0, len(self.randomlist)-1)
            code = random.choice(self.randomlist)
            if code is not None:
                print(f'randomiser {code=}')
                await self.send2(code)
                await self.send3(code)
        

        self.runetimer = self.now - self.runetimer0

        if self.runetimer > 900: # change to 600 when haste
            self.checkrune = True

        if self.checkrune:
            self.solverune = self.runesolver.runechecker(self.g)
        #print(f'{x=} {y=} rt={self.runetimer} sr={self.solverune} ft={self.fountaintimer} gl={self.goleft} gr={self.goright}')

        if self.solverune:
            await self.runesolver.gotorune(self.g)
       
        


    def update_timers(self):
        # Handling all timer related updates in a dedicated method
        self.fountaintimer = self.now - self.fountaintimer0
        if self.fountaintimer > 59:
            self.fountain = True
        #spider timer 
        self.spidertimer = self.now - self.spidertimer0
        if self.spidertimer > 249:
            self.spider = True
        #hurricane timer 
        self.hurricanetimer = self.now - self.hurricanetimer0
        if self.hurricanetimer > 13:
            self.hurricaneplant = True
        #infantry timer    
        self.infantrytimer = self.now - self.infantrytimer0
        if self.infantrytimer > 23:
            self.infantryplant = True
        #aura timer 
        self.auratimer = self.now - self.auratimer0
        if self.auratimer > 139:
            self.aura = True
        #origin timer    
        self.origintimer = self.now - self.origintimer0
        if self.origintimer > 299:
            self.origin = True
        #changechannel timer 
        self.cctimer = self.now - self.cctimer0
        if self.cctimer > 3599:
            self.cc = True

        


    

                    
        

    async def clockwise_Upj(self,x,y):
        
        if y == 29.5 or y == 59.5:
            while self.infantryplant == True:
                if self.infantry:
                    await random.choice([self.infantry])()
                self.infantryplant=False
                self.infantrytimer0=perf_counter()
        while self.hurricaneplant == True:
            if self.hurricane:
                    await random.choice([self.hurricane])()
            self.hurricaneplant=False
            self.hurricanetimer0=perf_counter()                                    
        
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
                    await random.choice([self.fountaincheck])()
                    await random.choice([self.gorightattack, self.gorightattackk])()
            elif x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattackupj])()
                    
                else:
                    await random.choice([self.goupattackupj])()
                    
        elif y <= self.top+self.offsety and y > self.top-self.offsety:
            if x < self.right-self.offsetx:
                await random.choice([self.fountaincheck])()
                await random.choice([self.gorightattack, self.gorightattackk])()
            elif x > self.right+self.offsetx:
                await random.choice([self.goleftattack, self.goleftattackk])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.spidercheck])()
                await random.choice([self.godownattack])()
        elif y > self.top and not (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    
                    await random.choice([self.goupattackupj])()
                    
                else:
                    await random.choice([self.goupattackupj])()
                    
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.spidercheck])()
                await random.choice([self.godownattack])()
            else:
                if x < ((self.right-self.left)/2):
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack_v3])()
                    else:
                        await random.choice([self.goupattackupj])()
                        
                elif x >= ((self.right-self.left)/2):
                    await random.choice([self.spidercheck])()
                    await random.choice([self.godownattack])()
        
        else:
            await random.choice([self.spidercheck])()
            await random.choice([self.godownattack])()

        
        #fountain timer
        self.fountaintimer = self.now - self.fountaintimer0
        if self.fountaintimer > 59:
            self.fountain = True
        #spider timer 
        self.spidertimer = self.now - self.spidertimer0
        if self.spidertimer > 249:
            self.spider = True
        #hurricane timer 
        self.hurricanetimer = self.now - self.hurricanetimer0
        if self.hurricanetimer > 13:
            self.hurricaneplant = True
        #infantry timer    
        self.infantrytimer = self.now - self.infantrytimer0
        if self.infantrytimer > 23:
            self.infantryplant = True
 
        #changechannel timer 
        self.cctimer = self.now - self.cctimer0
        if self.cctimer > 4:
            self.cc = True

        self.now = perf_counter()
        self.randommtimer = self.now - self.randommtimer0
        if self.randommtimer > 15:
            self.randommtimer0 = self.now
            code = random.choice(self.randomlist)
        await self.post_perform_action(x,y)    

    async def clockwiseskate(self,x,y):
          
        if y > self.top and (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x > self.left+self.offsetx:
                if x < self.left+self.offsetx+5:
                    await random.choice([self.leftwalk])()
                else:
                    await random.choice([self.goleftskate])()
            elif x < self.left-self.offsetx:
                if x > self.left-self.offsetx-5:
                    
                    await random.choice([self.rightwalk])()
                else:
                    await random.choice([self.fountaincheck])()
                    await random.choice([self.gorightattack, self.gorightattackk])()
            elif x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    await random.choice([self.goupattack])()
                    
                else:
                    await random.choice([self.goupattack])()
                    
        elif y <= self.top+self.offsety and y > self.top-self.offsety:
            if x < self.right-self.offsetx:
                await random.choice([self.fountaincheck])()
                await random.choice([self.gorightattack, self.gorightattackk])()
            elif x > self.right+self.offsetx:
                await random.choice([self.goleftskate])()
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.spidercheck])()
                await random.choice([self.godownattack])()
        elif y > self.top and not (y > self.btm-self.offsety and y <= self.btm+self.offsety):
            if x >= self.left-self.offsetx and x <= self.left+self.offsetx:
                if self.replaceropeconnect:
                    
                    await random.choice([self.goupattack])()
                    
                else:
                    await random.choice([self.goupattack])()
                    
            elif x >= self.right-self.offsetx and x <= self.right+self.offsetx:
                await random.choice([self.spidercheck])()
                await random.choice([self.godownattack])()
            else:
                if x < ((self.right-self.left)/2):
                    if self.replaceropeconnect:
                        await random.choice([self.goupattack_v3])()
                    else:
                        await random.choice([self.goupattack])()
                        
                elif x >= ((self.right-self.left)/2):
                    await random.choice([self.spidercheck])()
                    await random.choice([self.godownattack])()
        
        else:
            await random.choice([self.spidercheck])()
            await random.choice([self.godownattack])()
        await random.choice([self.auracheck])()
        await random.choice([self.origincheck])()
        await random.choice([self.infantrycheck])()
        await random.choice([self.hurricanecheck])()
        #fountain timer
        self.fountaintimer = self.now - self.fountaintimer0
        if self.fountaintimer > 59:
            self.fountain = True
        #spider timer 
        self.spidertimer = self.now - self.spidertimer0
        if self.spidertimer > 249:
            self.spider = True
        #hurricane timer 
        self.hurricanetimer = self.now - self.hurricanetimer0
        if self.hurricanetimer > 13:
            self.hurricaneplant = True
        #infantry timer    
        self.infantrytimer = self.now - self.infantrytimer0
        if self.infantrytimer > 23:
            self.infantryplant = True
        #aura timer 
        self.auratimer = self.now - self.auratimer0
        if self.auratimer > 139:
            self.aura = True
        #origin timer    
        self.origintimer = self.now - self.origintimer0
        if self.origintimer > 299:
            self.origin = True

        # await self.post_perform_action(x,y)
        self.now = perf_counter()
        self.randommtimer = self.now - self.randommtimer0
        if self.randommtimer > 15:
            self.randommtimer0 = self.now
            code = random.choice(self.randomlist)