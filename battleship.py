from typing import Deque, Tuple
import pygame
import numpy as np
from pygame_widgets import Button
from collections import deque
import random 
buttons = []
PREGAME = 0
ATTACKING = 1
SHIPS = [5,4,3,3,2]
class BButton(Button):
    def __init__(self,BShip,Nx,Ny,screen,xNum,yNum, SizeX, SizeY,
            inactiveColour=(255,255,255),
            pressedColour=(0, 255, 0), radius=100):#lambda: fire(xNum,yNum)
        super(BButton,self).__init__(screen,xNum,yNum, SizeX, SizeY,
            inactiveColour=inactiveColour,
            pressedColour=pressedColour, radius=radius,
            onClick=lambda: BShip.ButtonClick(Nx,Ny))



class Board:
    def __init__(self,winSize):
        self.array = np.zeros((10,10,2))
        for xnum in range(10):
            for ynum in range(10):
                self.array[xnum][ynum] = [xnum * (winSize[0]/10)+((winSize[0]/10)/4),ynum * (winSize[1]/10)+((winSize[0]/10)/4)]
        
                
        

class Ship:
    def __init__(self,_size,_x,_y,_orientation):
        self.size = _size
        self.orentiation = _orientation#[0,1] up [1,0] right [0,-1] down [-1,0] left
        self.sunken = False
        self.x = _x
        self.y = _y
        self.locations = []
        self.hits = 0
        self.hitLocs = []
        for i in range(self.size):
            self.locations.append((self.x+(self.orentiation[0]*i),self.y+(self.orentiation[1]*i)))
    def move(self,nX,nY,orientation = None):
        self.x = nX
        self.y = nY
        if orientation != None:
            self.orentiation = orientation
        self.locations = []
        for i in range(self.size):
            self.locations.append((self.x+(self.orentiation[0]*i),self.y+(self.orentiation[1]*i)))
    def hit(self,Tx,Ty):
        for x,y in self.locations:
            if x == Tx and y == Ty:
                self.hits += 1
                self.hitLocs.append((x,y))
                return True
        return False
    def CheckIfSunk(self):
        return self.hits == self.size
        
        
        

class Player:
    def __init__(self):
        self.ships = []
    def hitShip(self,x,y):
        for ship in self.ships:
            if ship.hit(x,y):
                ship.CheckIfSunk()
                return [x,y]
        return False
    def draw(self,buttons):
        for ship in self.ships:
            for loc in ship.locations:
                buttons[loc[0]+loc[1]].setInactiveColour((0,0,255))
        return buttons
    def addShip(self,_x,_y,size,direction):
        self.ships.append(Ship(size,_x,_y,direction))
    def randomShips(self):
        for ship in range(5):
            x = random.randint(0,9)
            y = random.randint(0,9)
            if not self.hitShip(x,y):
                d = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                self.addShip(x,y,SHIPS[ship],d)
            


        
class BattleShip:
    def __init__(self,_resX,_resY):
        self.MAXPLAYERS = 2
        self.buttons = []
        self.board = Board((_resX,_resY))
        self.resX = _resX
        self.resY = _resY
        self.turn = 0
        self.stage = ATTACKING
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 30)
        self.run = True
        self.players = deque([Player(),Player()],maxlen=self.MAXPLAYERS)
        self.screen = pygame.display.set_mode([self.resX,self.resY])
        self.clock = pygame.time.Clock()
        for ynum in range(10):
            for xnum in range(10):
                self.buttons.append(BButton(self,xnum,ynum,self.screen,self.board.array[xnum][ynum][0],self.board.array[xnum][ynum][1],50,50,(255,255,255)))
        for player in self.players:
            player.randomShips()
    def nextPlayer(self,n):
        if n < self.MAXPLAYERS:
            return n
        else:
            return 0
    def ButtonClick(self,x,y):
        print("clicked X =",x,"Y =",y)
        if self.stage == ATTACKING:
            if self.players[self.nextPlayer(self.turn)].hitShip(x,y) != False:
                self.buttons[x+(y*10)].setInactiveColour((244,21,23))
            self.turn = self.nextPlayer(self.turn+1)
        # if self.stage == PREGAME:
        #     self.players[self.turn].addShip(x,y)

        
    def PyGameStuff(self):
        self.clock.tick(30)
        for button in self.buttons:
            button.listen(pygame.event.get())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
    
    def step(self):
        if self.stage == PREGAME:
            pass
        else:
            pass

    def render(self):
        for button in self.buttons:
            button.draw()
        self.buttons = self.players[self.turn].draw(self.buttons)
        self.turnindicator = self.myfont.render("Player: "+str(self.turn+1),1, (255,0,0))
        self.screen.blit(self.turnindicator,(800,950))
        pygame.display.flip()


game = BattleShip(1000,1000)

while game.run:
    game.step()
    game.PyGameStuff()
    game.render()