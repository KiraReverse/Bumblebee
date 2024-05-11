#!/usr/bin/env python
#coding=utf-8

from ctypes import *
beep = windll.kernel32.Beep

class pySong(object):
    __pitchhz = {}
    __pianohz = {}
    __keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    __keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')
    __simple_equal = {1:0, "1#":1, 2:2, "2#":2, 3:4, 4:5, "4#":6, 5:7, "5#":8, 6:9, "6#":10, 7:11}
    
    _bpm = 120
    
    def __init__(self, bpm=120):
        self._bpm = bpm
        # build pitch hz map
        for k in range(88):
            freq = 27.5 * 2.0 **(k/12.0)
            oct = (k+9) // 12
            noteS = '%s%u' % (self.__keys_s[k%12], oct)
            self.__pitchhz[noteS] = freq
            noteF = '%s%u' % (self.__keys_f[k%12], oct)
            self.__pitchhz[noteF] = freq
            self.__pianohz[k] = freq
        
    def playSimple(self, simpleScore, octane=5):
        '''
        notes range from 1-7. H stands for higher otance, L stands for lower
        octane, S for half beat, Q for quarter beat, D for double beats
        '''
        hzmsList = self.parseSimpleScore(simpleScore, octane)
        self.playHzMsList(hzmsList)
        
    def playSPN(self, spnTupleList):
        beatTime = 60000 // self._bpm        
        for spnTuple in spnTupleList:
            key = spnTuple[0]
            freq = 0
            if key == 'r':
            # if key <> 'r':
                freq = self.__pitchhz[key]
            time = beatTime // spnTuple[1]
            beep(int(freq), time)                

    def playHzMsList(self, hzmsList):
        for hzms in hzmsList:
            beep(int(hzms[0]), hzms[1])
    
    def parseSimpleScore(self, score, octane):
        if not score:
            raise Error("null input")
        scoreArr = []
        l = len(score)
        index = 0
        beatTime = 60000 // self._bpm
        while(index < l):
            actualOctane = octane
            actualBeatTime = beatTime
            note = int(score[index])
            while(index + 1 < l and not score[index+1].isdigit()):
                index = index + 1
                decorator = score[index].upper()
                if decorator == "H":
                    actualOctane = actualOctane + 1
                elif decorator == "L":
                    actualOctane = actualOctane - 1
                elif decorator == "S":
                    actualBeatTime = actualBeatTime // 2
                elif decorator == "Q":
                    actualBeatTime = actualBeatTime // 4
                elif decorator == "D":
                    actualBeatTime = actualBeatTime * 2
                elif decorator == "W":
                    actualBeatTime = actualBeatTime * 4
                elif decorator == "#":
                    note = str(note) + "#"
                else:
                    raise Error("simple note syntax error")
            scoreArr.append((self.__convertSimpleNoteToFeq(note, actualOctane), actualBeatTime))
            index = index + 1
        return scoreArr
    
    def __convertSimpleNoteToFeq(self, simpleNote, octane):
        if (str(simpleNote).isdigit()) and ( simpleNote < 1 or simpleNote > 7):
            return 0
        base = 12 * octane - 8
        piano = base + self.__simple_equal[simpleNote]
        return self.__pianohz[piano]
        
if __name__ == '__main__':
#    mysong = pySong("ok")
#    mysong.play()
    mysong = pySong()
#    a = mysong.parseSimpleScore('76543217L6L5L4L3L2L1L', 5)
#    mysong.playHzMsList(a)
    mysong._bpm = 120
    #mysong.playSimple("12345671H2H3H4H5H6H7H")
    mysong.playSimple("3Q2#Q3Q2#Q3Q7LQ2Q1Q6LW1L3LQ6LQ7L03L5#LQ7LQ103LQ3Q2#Q3Q2#Q3Q7LQ2Q1Q6LW1L3LQ6LQ7L03L1Q7LQ6L0", octane = 6)
    #mysong.playSimple("51HQ6Q553q5q6q1hq5565q3q22")
    #mysong.playSimple("12311231345034505Q6Q5Q4Q315Q6Q5Q4Q3125L1025L1", octane = 6)
    #mysong.playSimple("5330S4220S123455505330S4220S13553022222340S333334505330S4220S13551D")
    song1 = (
  ('bb4', 8),
  ('g5', 2), ('f5', 8), ('g5', 8), ('f5', 8/3), ('eb5', 4), ('bb4', 8),
  ('g5', 4), ('c5', 8), ('c6', 4), ('g5', 8), ('bb5', 8/3), ('ab5', 4), ('g5', 8),
  ('f5', 8/3), ('g5', 4), ('d5', 8), ('eb5', 8/3), ('c5', 8/3),
  ('bb4', 8), ('d6', 8), ('c6', 8), ('bb5', 16), ('ab5', 16), ('g5', 16), ('ab5', 16), ('c5', 16), ('d5', 16), ('eb5', 8/3),
)

    #mysong.playSPN(song1)
    
            