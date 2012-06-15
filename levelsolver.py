###
##            0 Nothing           5 Yellow Up
##            1 Player           6 Dark Blue Down
##            2 Grey Static               7 Light Blue DisAppear
##            3 Orange Up           8 Green Exit
##            4 Purple Down               9 Pink DisAppear
##            a Red Gate           b Dark Green Switch
##            c horizontalappear    
##            d horizontaldisappear
##            e moves left upon vertical movement 
##            f moves right on vertical movement
##            g moves left upon horizontal movement 
##            h moves right on horizontal movement
##            i perma green switch
##            
###
from operator import itemgetter, attrgetter
import random
reflist = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i']
master = 0
todo = []
solved = {}
def randnum(low, high):
    return random.randint(low, high-1);
class game():
    def mastersolve(self):
        global master
        global todo
        global solved
        str = self.createstring()
        if str in solved:
            return solved[str]        
        master = self
        master.children = []
        todo = []
        todo.append(self)
        while(len(todo) > 0):            
            ret = todo.pop(0).solve() 
            if(ret != 0):
                solved[str] = ret
                return ret
        solved[str] = ret
        return 0
    def duplicate(self, other):
        other.elementarray = []       
        for i in self.elementarray:
            temp = element(other, i.type)
            if i.type == 1:
                other.player = temp
            temp.state = i.state[:]
            temp.output = i.output[:]           
            other.elementarray.append(temp)            
    def solve(self): 
        global master
        global todo                 
        for child in master.children:               
            if(self.compare(child) and self != child):                 
                return 0   
        
        
        master.children.append(self)
        for i in range(4):
            child = game(self.type, '', self)  
            self.duplicate(child)    
                     
            result = child.input(i+1)
            child.inputs = [i+1]                
                      
            
            if(result == 1):
                
                wininput = [i+1]          
                target = self
                while target.parent != 0:  
                    
                    for t in target.inputs:
                        wininput.insert(0, t)  
                    
                    target = target.parent
                
                return wininput
            elif result == 0:                
                todo.append(child)
                                
        
        return 0
    def interactive(self):
        self.printarray()
        while 1:            
            ch = raw_input()
            if ch == 'w':
                ret = self.input(1)
            elif ch == 'd':
                ret = self.input(2)
            elif ch == 's':
                ret = self.input(3)
            elif ch == 'a':
                ret = self.input(4)  
            elif ch == 'x':
                ret = self.input(5)
            else:
                ret = 0
            
            self.printarray()
    def compare(self, other): #use to compare two games
        # sanity check
        for i in self.elementarray:
            firstfound = False
            for x in other.elementarray:                
                if i.state == x.state and i.type == x.type:                    
                    firstfound = True
                    break
            if not firstfound:                
                return False
                break                
        for x in self.elementarray:
            firstfound = False
            for i in other.elementarray:                
                if i.state == x.state and i.type == x.type:
                    firstfound = True
                    break
            if not firstfound:
                return False
                break
        return True
    def __init__(self, type, array, parent=0):
        self.children = []
        self.parent = parent;
        self.inputs = []
        self.type = type
        self.phase = 0
        self.elementarray = []
        self.todo = []
        self.player = 0                
        if type == 0: #standard           
            self.wx = 10
            self.wy = 3
            for i in range(len(array)):
                bx = i % self.wx;
                by = int((i - bx) / self.wx);  
                if array[i] != '0':
                    self.elementarray.append(element(self, reflist.index(array[i]), [bx,by]))    
        elif type == 1:   #reduced array
            self.wx = 3
            self.wy = 3
            for i in range(len(array)):
                bx = i % self.wx;
                by = int((i - bx) / self.wx);  
                if array[i] != '0':
                    self.elementarray.append(element(self, reflist.index(array[i]), [bx,by]))    
        
        self.elementarray.sort(key = lambda element: element.type)    
    def inputandprint(self, inputs):
        for i in inputs:
            self.printarray()
            print self.input(i)
        self.printarray()
    def input(self, i):      
        
        if self.player.input(i):              
            for element in self.elementarray:
                if element != self.player:
                    element.input(i) 
            
            #now check collisions
            win = False
            lose = False
            for element in self.elementarray:
                if element != self.player:
                    if element.state[2] == 1 and element.state[3] == self.phase:                        
                        #check collision
                        if element.state[0] == self.player.state[0] and element.state[1] == self.player.state[1]:
                            if element.type == 11:
                                self.reversegates()
                                element.state[2] = 0
                            elif element.type == 8:
                                win = True #win
                            elif element.type == 18:
                                self.reversegates()
                            else:
                                lose = True #lose
            if win and not lose:
                return 1
            if lose:
                return -1
            return 0 #boring
        else:
            return -2 #player can't move
    def lose(self):
        print 'lose'
    def win(self):
        print 'Win'
    def reversegates(self):
        for element in self.elementarray:
            if element.type == 10:
                if element.state[3] == self.phase:
                    element.state[2] = 1 - element.state[2]
    def printarray(self):
        printout = []
        for y in range(self.wx*self.wy):                
            printout.append('0')
        
        for element in self.elementarray:                
            if element.state[2] == 1 and element.state[3] == self.phase:
                printout[element.state[0] + element.state[1]*self.wx] = reflist[element.type]
        print ''.join(printout[0:self.wx])            
        print ''.join(printout[self.wx:self.wx*2])
        print ''.join(printout[self.wx*2:self.wx*3])
        print ''    
    def createstring(self):        
        printout = []
        tempprintout = []
        index = 0
        for y in range(self.wx*self.wy):                
            tempprintout.append('0')   
        printout.append(tempprintout)
        for element in self.elementarray:        
            index = 0                
            while(printout[index][element.state[0] + element.state[1]*self.wx] != '0'):
                index += 1
                if(index >= len(printout)):
                    tempprintout = []
                    for y in range(self.wx*self.wy):                
                        tempprintout.append('0')
                    printout.append(tempprintout)
            printout[index][element.state[0] + element.state[1]*self.wx] = reflist[element.type]
        str = ''
        for string in printout:
            str += ''.join(string[0:self.wx*self.wy]) + ' '
        return str
    def checkloc(self, loc, type=range(len(reflist))):
        ret = []
        for element in self.elementarray:
            if element.state[0] == loc[0] and element.state[1] == loc[1] and (element.type in type):
                ret.append(element)
        return ret
    def evolve(self, ref):
        ret = game(self.type, '')
        self.duplicate(ret) 
        if(self.type == 0):                   
            mutationnum = randnum(0, 5)
            for i in range(mutationnum):
                action = randnum(0, 3)            
                if action == 0 and len(ret.elementarray) > 2:
                    target = randnum(0, len(ret.elementarray))
                    while ret.elementarray[target].type == 1 or ret.elementarray[target].type == 8:
                        target = randnum(0, len(ret.elementarray))
                    type = ref[randnum(0, len(ref))]
                    while type == 1 or type == 8:
                        type = ref[randnum(0, len(ref))]
                    state = ret.elementarray[target].state
                    ret.elementarray[target] = element(ret, type, [state[0], state[1]])
                elif action == 1 and len(ret.elementarray) < ret.wx*ret.wy - 2:                    
                    type = ref[randnum(0, len(ref))]
                    while type == 1 or type == 8:
                        type = ref[randnum(0, len(ref))]
                    state = [randnum(0, self.wx), randnum(0, self.wy)]
                    while len(ret.checkloc(state)) != 0:
                        state = [randnum(0, self.wx), randnum(0, self.wy)]
                    ret.elementarray.append(element(ret, type, state))
                elif action == 2 and len(ret.elementarray) > 2:
                    target = randnum(0, len(ret.elementarray))
                    while ret.elementarray[target].type == 1 or ret.elementarray[target].type == 8:
                        target = randnum(0, len(ret.elementarray))
                    ret.elementarray.pop(target)
        elif(self.type == 1):
            mutationnum = randnum(0, 5)
            for i in range(mutationnum):
                action = randnum(0, 3)                  
                if action == 0 and len(ret.elementarray) > 2:
                    target = randnum(0, len(ret.elementarray))
                    while ret.elementarray[target].type == 1 or ret.elementarray[target].type == 8:
                        target = randnum(0, len(ret.elementarray))
                    type = ref[randnum(0, len(ref))]
                    while type == 1 or type == 8:
                        type = ref[randnum(0, len(ref))]
                    state = ret.elementarray[target].state
                    ret.elementarray[target] = element(ret, type, [state[0], state[1]])
                elif action == 1 and len(ret.elementarray) < ret.wx*ret.wy - 2:                    
                    type = ref[randnum(0, len(ref))]
                    while type == 1 or type == 8:
                        type = ref[randnum(0, len(ref))]
                    state = [randnum(0, self.wx), randnum(0, self.wy)]
                    while len(ret.checkloc(state)) != 0:
                        state = [randnum(0, self.wx), randnum(0, self.wy)]
                    ret.elementarray.append(element(ret, type, state))
                elif action == 2 and len(ret.elementarray) > 2:
                    target = randnum(0, len(ret.elementarray))
                    while ret.elementarray[target].type == 1 or ret.elementarray[target].type == 8:
                        target = randnum(0, len(ret.elementarray))
                    ret.elementarray.pop(target)                   
                
        return ret
    def fillrandom(self, num, array):
        if(self.type == 0):
            num = int(num + randnum(-2,2))
            if(num > self.wx*self.wy - 2):
                num = self.wx*self.wy - 2
            elif num < 0:
                num = 0
            self.elementarray = []
            # make players and goals
            self.elementarray.append(element(self, 1, [0, 1]))            
            self.elementarray.append(element(self, 8, [7, 1]))            
            for i in range(num):
                a = array[randnum(0, len(array))]
                loc = [randnum(0, self.wx), randnum(0, self.wy)]
                while a == 1 or a ==8 or len(self.checkloc(loc)) != 0:
                    a = array[randnum(0, len(array))]               
                    loc = [randnum(0, self.wx), randnum(0, self.wy)]
                self.elementarray.append(element(self, a, loc))   
        elif(self.type == 1):
            num = int(num + randnum(-2,2))
            if(num > self.wx*self.wy - 2):
                num = self.wx*self.wy - 2
                print num
            elif num < 0:
                num = 0
            self.elementarray = []
            # make players and goals
            loc = [randnum(0, self.wx), randnum(0, self.wy)]
            self.elementarray.append(element(self, 1, loc))
            
            loc = [randnum(0, self.wx), randnum(0, self.wy)]
            while len(self.checkloc(loc)) != 0:
                loc = [randnum(0, self.wx), randnum(0, self.wy)]
            self.elementarray.append(element(self, 8, loc))
            
            for i in range(num):
                a = array[randnum(0, len(array))]
                loc = [randnum(0, self.wx), randnum(0, self.wy)]
                while a == 1 or a ==8 or len(self.checkloc(loc)) != 0:
                    a = array[randnum(0, len(array))]             
                    loc = [randnum(0, self.wx), randnum(0, self.wy)]
                self.elementarray.append(element(self, a, loc))            
    def specialeval(self, solve):
        ret = len(solve) - len(self.elementarray) / 8
        for i in solve:
            if i == 4 and self.type == 0:
                ret += 0.5
        return ret;
            
class element():     
    def __init__(self, parent, t, initstate = [0,0], initphase = -1, respinphase=0): # if you want it to respond to phases, set the initphase to 0 or 1
        
        #5th number is responsiveness to phase
        self.parent = parent
        self.output = [0, 1, 2, 3, 0] #direction 1 is up, goes clockwise. 0 means nothing happens. -1 means change in play
        self.state = [0,0,0,0] #x,y, in play, in phase    
        self.type = 0
        self.state[0] = initstate[0]
        self.state[1] = initstate[1]
        self.state[2] = 1
        if(initphase < 0):
            initphase = 0            
        else:
            respinphase = 5        
        self.state[3] = initphase        
        self.type = t        
        if t == 0:
            1
        elif t == 1:                
            self.output = [1, 2, 3, 4, 0]
            self.parent.player = self
        elif t == 2:
            self.output = [0, 0, 0, 0, respinphase]             
        elif t == 3:
            self.output = [1, 0, 1, 0, respinphase]
        elif t == 4:
            self.output = [3, 0, 3, 0, respinphase]
        elif t == 5:
            self.output = [0, 1, 0, 1, respinphase]            
        elif t == 6:
            self.output = [0, 3, 0, 3, respinphase]            
        elif t == 7:
            self.output = [-1, 0, -1, 0, respinphase]            
        elif t == 8:
            self.output = [0, 0, 0, 0, 0]            
        elif t == 9:
            self.state[2] = 0
            self.output = [-1, 0, -1, 0, respinphase]            
        elif t == 10:
            self.output = [0, 0, 0, 0, respinphase]            
        elif t == 11:
            self.output = [0, 0, 0, 0, respinphase]            
        elif t == 12:
            self.state[2] = 0
            self.output = [0, -1, 0, -1, respinphase]            
        elif t == 13:
            self.output = [0, -1, 0, -1, respinphase]            
        elif t == 14:
            self.output = [4, 0, 4, 0, respinphase]            
        elif t == 15:
            self.output = [2, 0, 2, 0, respinphase]            
        elif t == 16:
            self.output = [0, 4, 0, 4, respinphase]            
        elif t == 17:
            self.output = [0, 2, 0, 2, respinphase]            
        elif t == 18:
            self.output = [0, 0, 0, 0, respinphase]        
    def input(self, i):
        
        output = self.output[i-1]                  
        if output == 5:
            self.state[3] = 1 - self.state[3]
        if(self.state[3] == self.parent.phase):        
            if output == 1:
                self.state[1] -= 1
            elif output == 2:
                self.state[0] += 1
            elif output == 3:
                self.state[1] += 1
            elif output == 4:
                self.state[0] -= 1                   
            elif output == -1:
                self.state[2] = 1 - self.state[2]
        if(self.state[1] <= -1):
                self.state[1] = self.parent.wy - 1
        elif self.state[1] >= self.parent.wy:
                self.state[1] = 0
        if self.parent.type != 1:            
            if(self.state[0] <= -1):
                self.state[0] = 0   
                return False
            elif(self.state[0] >= self.parent.wx):
                self.state[0] = self.parent.wx - 1
                return False
        else:
            if(self.state[0] <= -1):
                self.state[0] = self.parent.wx - 1
            elif(self.state[0] >= self.parent.wx):
                self.state[0] = 0
        return True            

def gen(type, num, myref=reflist):    
    gamearray = []
    for i in range(20):        
        a = game(type, '')
        a.fillrandom(num, myref)
        while a.mastersolve() == 0:
            a = game(type, '')
            a.fillrandom(num, myref)
        gamearray.append(a)  
        print len(gamearray)   
    while 1:
        
        for i in range(20):
            gamearray.append(gamearray[randnum(0, len(gamearray))].evolve(myref))
        print 'evolved'
        solve = []
        for i in gamearray:
            a = i.mastersolve()
            if(a != 0):
                solve.append([a, i])
        print 'solved'
        newgamearray = []
        solve.sort(key = lambda list: list[1].specialeval(list[0]))  
        print 'sorted'
        for i in range(len(solve)-1):        
            if(randnum(0, len(solve)*(len(solve)-1)/2) < i*11):
                newgamearray.append(solve[i][1])
                for i in solve[i][1].elementarray:
                    if i.state[2] == 0 and i.type != 9 and i.type != 12:
                        print 'uhoh'
        newgamearray.append(solve[len(solve)-1][1])                
        print 'chosen'
        gamearray = newgamearray 
        print 'adding one random'
        a = game(type, '')
        print 'created blank game'
        a.fillrandom(num, myref)
        print 'made random game, now solving'
        while a.mastersolve() == 0:
            a = game(type, '')
            a.fillrandom(num, myref)
            print 'rejected', a.createstring()
        gamearray.append(a)  
        print 'number of games', len(gamearray)
        a = solve[len(solve)-1][1].mastersolve()
        print a, solve[len(solve)-1][1].createstring(), len(a)
        print >>file, a, solve[len(solve)-1][1].createstring(), len(a)
        file.flush()
    return solve[len(solve)-1][1].mastersolve(), solve[len(solve)-1][1].createstring()

def quickanddirty(type, str):
    a = game(type, str)
    sa = a.mastersolve()
    print sa, len(sa), str 
    
file = open("output.txt", "a")
#Uncomment to generate new levels 
#gen(0, 12, range(len(reflist)-7))

#Uncomment to solve the level 'lock' (number 8) from the game Impasse at http://www.kongregate.com/games/wanderlands/impasse 
quickanddirty(0, '240032400210343442382224000332')

#To understand the output - the numbers represent key presses: 1 is up, 2 is right, 3 is down, 4 is left. 