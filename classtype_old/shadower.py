import random
import time
from time import perf_counter
# from configparser import ConfigParser
from action import Action
from initinterception import sleep








class Shadower(Action):

    def __init__(self):
        super().__init__()
        self.offsety=5
        self.offsetx=15
        self.goleft=True
        self.goright=False
        self.randomlist = ['z', 'x', 'c', 'space', '2', '3', '0', 'f9', 'w', 'e', 'r', 't', 's', 'd', 'f', 'v']
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
        self.rotation_list = ['default', 'mapril', 'hotel']
        self.rotation='default'
        self.rotation_mapping = {
            'default': self.clockwise,
            'mapril': self.mapril,
            'hotel': self.hotel,
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
        # await self.limen1_7(x,y)
        # await self.clockwise(x,y)
        # print(f'{self.rotation=}')
        await self.rotation_mapping[self.rotation](x,y)
        
    def get_rotation_list(self):
        return self.rotation_list
        
    def set_rotation(self, rotation):
        self.rotation = rotation
        print(f'{self.rotation=}')

    # basic 4x direction movement (goleft, goright, gooup, godown)
    async def goleftattack(self):
        print(f'goleftattack')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def goleftattack2(self):
        print(f'goleftattack2')
        await self.leftp()
        await self.jumpp(222,388)
        await self.jumpr(3,11)    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.leftr()

    async def gorightattack(self):
        print(f'gorightattack')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def gorightattack2(self):
        print(f'gorightattack2')
        await self.rightp()
        await self.jumpp(222,388)
        await self.jumpr(3,11)
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def goupattack(self): # adele upjump
        print(f'goupattack')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        print(f'press ropeconnect once. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        await sleep(.777)
        print(f'press ropeconnect twice. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        print(f'attack.  ')
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def goupattack2(self): # adele upjump
        print(f'goupattack2')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        print(f'press ropeconnect once. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        await sleep(.888)
        print(f'press ropeconnect twice. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        print(f'attack.  ')
        await self.attackp()
        await self.attackr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)

    async def godownattack(self):
        print(f'godownattack')
        await self.downp()    
        await self.jumpp()
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.downr()

    # variation of 4 basic movement to make sequence more randomise.
    async def goleftattackk(self):
        print(f'goleftattackk')
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
        print(f'goattackleft')
        await self.leftp()
        await self.attackp()
        await self.attackr()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()    
        await self.jumpp()
        await self.jumpr()
        await self.leftr()

    async def goattackkleft(self):
        print(f'goattackleft')
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
        print(f'gorightattackk')
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
        print(f'goattackright')
        await self.rightp()
        await self.attackp()
        await self.attackr()
        await sleep(.5)
        await self.jumpp()
        await self.jumpr()  
        await self.jumpp()
        await self.jumpr()
        await self.rightr()

    async def goattackkright(self):
        print(f'goattackkright')
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

    async def upjumpattack(self):
        print(f'upjumpattack')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()
        await self.attackp()
        await self.attackr()
        await sleep(.1)
    
    async def stormwing(self,x,y,goleft,goright):
        if goright:
            if y < self.top:
                await self.godownattack()
                time.sleep(.3)
            elif y > self.top:
                await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright])()
            if x > self.right:
                await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft])()
                time.sleep(.1)
                goright=False
                goleft=True
        elif goleft:
            if y < self.top:
                await self.godownattack()
                time.sleep(.3)
            elif y > self.top:
                await random.choice([self.goleftattack,self.goattackleft,self.goleftattackk,self.goattackkleft])()
                time.sleep(.1)
            if x < self.left: # only if x < left
                await random.choice([self.gorightattack,self.goattackright,self.gorightattackk,self.goattackkright])()
                time.sleep(.1)
                goright=True
                goleft=False
        return goleft,goright

    # shadower test write
    
    async def testupjump(self):
        print(f'testupjump')
        await self.jumpp()
        await self.jumpr()
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()

    async def mesoexplosionp(self):
        await self.fp() # just change to whatever key your meso explosion is        

    async def mesoexplosionp(self):
        await self.fr() # if it doesn't exist, just write one in action.py
        
    async def testmesoexplosion(self):
        print(f'testmesoexplosion')
        await self.attackp()
        await self.attackr()
        await self.mesoexplosionp() # or you can just use self.fp()
        await self.mesoexplosionr() # or you can just use self.fr()

    # soul master actions patch for limen 1-7
    
    async def rightupjump(self):
        print(f'rightupjump')
        await self.rightp()
        await self.jumpp()
        await self.jumpr()
        await self.rightr(3,11)
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()
        time.sleep(.1)

    async def leftupjump(self):
        print(f'leftupjump')
        await self.leftp()
        await self.jumpp()
        await self.jumpr()
        await self.leftr(3,11)
        await self.upp()
        await self.jumpp()
        await self.jumpr()
        await self.upr()
        time.sleep(.1)

    async def rightjumpattack(self):
        print(f'rightjumpattack')
        await self.rightp()
        await self.jumpp(131,211)
        await self.jumpr()
        await self.attackp()
        await self.attackr()
        await self.rightr()

    async def jumpropeconnectpr(self,x=111,y=222,x2=111,y2=222):
        await self.ropeconnectp(x,y)
        await self.ropeconnectr(x2,y2)

    async def ropeconnectpr(self,x=111,y=222,x2=111,y2=222):
        await self.ropeconnectp(x,y)
        await self.ropeconnectr(x2,y2)

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

    async def walkleft(self,distance=1):
        print(f'walkleft for {distance=}')
        x=int(distance*88)
        y=int(distance*144)
        await self.leftp(x,y)
        await self.leftr()
            
    async def walkright(self,distance=1):
        print(f'walkright for {distance=}')
        x=int(distance*88)
        y=int(distance*144)
        await self.rightp(x,y)
        await self.rightr()

    async def hotel(self,x,y):
        if x < self.right and x > self.left:
            if y > self.top:
                await random.choice([self.gorightattack, self.gorightattackk])()
            else:
                await random.choice([self.goleftattack, self.goleftattackk])()
        elif x > self.right:
            if y > self.top:
                await random.choice([self.goupattack])()
            else:
                await random.choice([self.goleftattack, self.goleftattackk])()
        elif x < self.left:
            if y > self.top:
                await random.choice([self.gorightattack, self.gorightattackk])()
            else:
                await random.choice([self.godownattack])()

        await self.post_perform_action(x,y)

    async def clockwise(self,x,y):
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
        self.runetimer = self.now - self.runetimer0
        # if runetimer > 600: # change to 600 when haste
        if self.runetimer > 900: # change to 600 when haste
            self.checkrune = True
            # self.checkrune = False
        if self.checkrune:
            self.solverune = self.runesolver.runechecker(self.g)
        print(f'{x=} {y=} rt={self.runetimer} sr={self.solverune} ft={self.fountaintimer} gl={self.goleft} gr={self.goright}')

        if self.solverune:
            await self.runesolver.gotorune(self.g)


    async def jumpkeeppr(self,x=2222,y=4444):
        print(f'jumpkeeppr')
        await self.jumpp(x,y)
        await self.jumpr()

    async def downlongpr(self,x=1222,y=1272):
        print(f'downlongpr')
        await self.downp(x,y)
        await self.downr()

    async def mapril(self,x,y):        
        await random.choice([self.jumpkeeppr, self.downlongpr])()
        # time.sleep(.1)