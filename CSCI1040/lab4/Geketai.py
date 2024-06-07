from enum import Enum
import os

class Color(Enum):
    BLACK = "X"
    RED = "O"


class Piece():
    def __init__(self, color: Color):
        self.color = color
    
    def __str__():
        pass

class Player():
    def __init__(self, color: Color, P: int):
        self.color = color
        self.P = []
        for i in range(P):
            self.P.append(Piece(self.color))

    def remove(self):
        del self.P[0]

    def add(self):
        self.P.append(Piece(self.color))
        
    def get_input(self):
        d = {chr(i+97):i for i in range(0,26)}

        x = list(input())
        while(" " in x):            #remove empty spacing
            x.remove(" ")

        if len(x) == 2:             #not empty list
            x[0]=x[0].lower()
            if d.get(x[0]) is not None and x[1].isnumeric():    #check input formal
                return(int(d[x[0]]), int(x[1])-1)            
            else:
                return(999,999)
        else:
            return(999,999)

class Board():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []                  #board
        for i in range(self.cols):
            col = []
            for j in range(self.rows):
                col.append(None)
            self.cells.append(col)

    def get_piece(self, x, y):
            return self.cells[x][y]
            
        
    def print(self):
        box1 =" +"                 # "+---+---+---+---+---+---+"
        for i in range(self.rows):
            print("   "+chr(i+65), end ="")
            box1 +="---+"
        print ("\n"+box1)

        for i in range(self.rows):

            col = str(i+1)+"|"
            for j in range(self.cols):
                if self.cells[i][j] == None:
                    col +=" "+"  "+"|"
                else:
                    col +=" "+self.cells[i][j]+" "+"|"
            print (col)
            print(box1) 

    def move(self, piece: Piece , y: int, x: int):
        pass       


class Gekitai(Board):
    def __init__(self, N: int = 6, P: int = 8, L: int = 3):
        super().__init__(N,N)
        assert 6 <= N <= 8 and 6 <= P <= 12 and 3 <= L <= min(N, P) #Validation of N P L
        self.N = N          #size
        self.P = P          #number of pieces per player
        self.L = L          #number of pieces required to form a line
        self.players = [Player (Color.BLACK,P),Player (Color.RED, P)]    # X:player 1    O: player 2
    
    def outofboard(self, y: int, x: int):
        if 0 <= x <= (self.N-1) and 0 <= y <= (self.N-1):
            return False
        else:
            return True

    def is_move_valid(self, y: int, x: int):
        if not self.outofboard(y, x):
            if self.cells[y][x] == None: 
                return True
            else:
                print("Invalid move!")
                return False
        else:
            print("Invalid move!")
            return False
    

    def move(self, piece: Piece, y: int, x: int):
        if self.is_move_valid(y,x):
            self.cells[y][x] = piece.color.value


            if not self.outofboard(y-1, x-1):
                if self.get_piece(y-1,x-1) != None :           #check not empty
                    if not self.outofboard(y-2,x-2):
                        if self.get_piece(y-2,x-2) == None:                 #check empty
                            self.cells[y-2][x-2] = self.cells[y-1][x-1]     #push cells
                            self.cells[y-1][x-1] = None

                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y-1][x-1]:
                                i.add()                                #p+1
                        self.cells[y-1][x-1] = None

            
            if not self.outofboard(y-1, x):
                if self.get_piece(y-1,x) != None :           #check not empty
                    if not self.outofboard(y-2,x):
                        if self.get_piece(y-2,x) == None:                 #check empty
                            self.cells[y-2][x] = self.cells[y-1][x]     #push cells
                            self.cells[y-1][x] = None
                   
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y-1][x]:
                                i.add()                                #p+1
                        self.cells[y-1][x] = None        
            
            if not self.outofboard(y-1, x+1):
                if self.get_piece(y-1,x+1) != None :           #check not empty
                    if not self.outofboard(y-2,x+2):
                        if self.get_piece(y-2,x+2) == None:                 #check empty
                            self.cells[y-2][x+2] = self.cells[y-1][x+1]     #push cells
                            self.cells[y-1][x+1] = None
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y-1][x+1]:
                                i.add                                #p+1
                        self.cells[y-1][x+1] = None
            
            
            ####################################################################################################
            if not self.outofboard(y, x-1):
                if self.get_piece(y,x-1) != None :           #check not empty
                    if not self.outofboard(y,x-2):
                        if self.get_piece(y,x-2) == None:                 #check empty
                            self.cells[y][x-2] = self.cells[y][x-1]     #push cells
                            self.cells[y][x-1] = None
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y][x-1]:
                                i.add()                                #p+1
                        self.cells[y][x-1] = None
            
            if not self.outofboard(y, x+1):
                if self.get_piece(y,x+1) != None :           #check not empty
                    if not self.outofboard(y,x+2):
                        if self.get_piece(y,x+2) == None:                 #check empty
                            self.cells[y][x+2] = self.cells[y][x+1]     #push cells
                            self.cells[y][x+1] = None
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y][x+1]:
                                i.add()                                #p+1
                        self.cells[y][x+1] = None
      

            ####################################################################################################
            if not self.outofboard(y+1, x-1):
                if self.get_piece(y+1,x-1) != None :           #check not empty
                    if not self.outofboard(y+2,x-2):
                        if self.get_piece(y+2,x-2) == None:                 #check empty
                            self.cells[y+2][x-2] = self.cells[y+1][x-1]     #push cells
                            self.cells[y+1][x-1] = None
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y+1][x-1]:
                                i.add()                                #p+1
                        self.cells[y+1][x-1] = None
            
            
            if not self.outofboard(y+1, x):
                if self.get_piece(y+1,x) != None :           #check not empty
                    if not self.outofboard(y+2,x):
                        if self.get_piece(y+2,x) == None:                 #check empty
                            self.cells[y+2][x] = self.cells[y+1][x]     #push cells
                            self.cells[y+1][x] = None
                    else:                                          #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y+1][x]:
                                i.add()                                #p+1
                        self.cells[y+1][x] = None
            
            if not self.outofboard(y+1, x+1):
                if self.get_piece(y+1,x+1) != None :           #check not empty
                    if not self.outofboard(y+2,x+2):
                        if self.get_piece(y+2,x+2) == None:                 #check empty
                            self.cells[y+2][x+2] = self.cells[y+1][x+1]     #push cells
                            self.cells[y+1][x+1] = None
                    else:                                       #check if out of board
                        for i in self.players:
                            if i.color.value == self.cells[y+1][x+1]:
                                i.add()                                #p+1
                        self.cells[y+1][x+1] = None
            
        
        
        
    def pieces_in_line(self, player: Player):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j] == player.color.value:

                    if not self.outofboard(i+1,j)and not self.outofboard(i+2,j):                #
                        if self.cells[i][j] == self.cells[i+1][j] == self.cells[i+2][j]:        # 
                            return True                                                         #

                    if not self.outofboard(i,j+1) and not self.outofboard(i,j+2):
                        if self.cells[i][j] == self.cells[i][j+1] == self.cells[i][j+2]:         ###
                            return True

                    if not self.outofboard(i-1,j+1) and not self.outofboard(i-2,j+2):               #
                        if self.cells[i][j] == self.cells[i-1][j+1] == self.cells[i-2][j+2]:       #
                            return True                                                           #
                    
                    if not self.outofboard(i+1,j+1) and not self.outofboard(i+2,j+2):            #
                        if self.cells[i][j] == self.cells[i+1][j+1] == self.cells[i+2][j+2]:      # 
                            return True                                                            #
                 
        return False

    def game_over(self):
        
        black = 0; 
        white = 0;

        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j] == Color.BLACK.value:
                    black += 1
                if self.cells[i][j] == Color.RED.value:
                    white += 1

        for i in self.players:
            if self.pieces_in_line(i):
                return True , 0
        
        if black == 8:
            return True , 1
        
        if white == 8:
            return True , 2
        
        return False , 999                         #999 is meaningless just for padding

    def print(self):
        super(Gekitai, self).print()
        X = []
        O = [] 
        for i in self.players:
            for j in i.P:
                if i.color.name == Color.BLACK.name:
                    X.append('X')
                
                if i.color.name == Color.RED.name:
                    O.append('O')



        print("X:",end="")
        print(X)
        print("O:",end="")
        print(O)
    
    def start(self):
        operator = True
        self.print()
        while operator:
            
            for i in self.players:
                print("Player "+i.color.value+"'s turn: ",end="")
                x = i.get_input()
                while not self.is_move_valid(x[1],x[0]):
                    print("Player "+i.color.value+"'s turn: ",end="")
                    x = i.get_input()

                
                self.move(i.P.pop(), x[1], x[0])
                self.print()

                temp = self.game_over()               # 2 values bool and int
                if temp[0] :

                    print("Game over:")
                    self.print()

                    if temp[1] == 0:
                        print("Player "+i.color.value+" wins!")
                    elif temp[1] == 1:
                        print("Player "+Color.BLACK.value+" wins!")
                    elif temp[1] == 2:
                        print("Player "+Color.RED.value+" wins!")
                    
                    operator = False
                    
                    break
        os.system("pause")

                    

            

    


        


        
b = Gekitai()
b.start()