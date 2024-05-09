import random
import time
# from configparser import ConfigParser
from action import Action
from initinterception import sleep








class Nightlord(Action):

    def __init__(self):
        super().__init__()
        self.offsety=5
        self.offsetx=15  
        self.rotation_list = ['default']
        self.rotation='default'
        self.rotation_mapping = {
            'default': self.clockwise,
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
        print(f'{self.rotation=}')
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

    async def goupattack(self): # adele upjump
        print(f'goupattack')
        await sleep(.1)
        await self.jumpp()
        await self.jumpr()
        print(f'press ropeconnect once. ')
        await self.ropeconnectp(31,101)
        await self.ropeconnectr(31,101)
        await sleep(.555)
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