


class Gamestate():
    def __init__(self):
        #board is 8x8 2d list each element of list of 2 characters
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.in_Check = False
        self.pins = []
        self.checks = []

        self.checkMate = False
        self.staleMate = False

    #takes a move then executes the move

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--" #empty space now moved
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log moves
        self.whiteToMove = not self.whiteToMove #swap turns
         
        #update kings location
        if move.pieceMoved == "wk":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bk":
            self.blackKingLocation = (move.endRow, move.endCol)

        # if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
        #     self.enPassantPossible = ((move.endRow + move.startRow) //2, move.endCol)
        # else:
        #     if move.enPassant:
        #         self.board[move.startRow][move.endCol] == "--"


    #undo last move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            #update kings position
            if move.pieceMoved == "wk":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bk":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        
        moves = []
        self.in_Check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.in_Check:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]
                
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3] * i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not(moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
                
            else:
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves = self.getAllPossibleMoves()
        
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves




        # moves = self.getAllPossibleMoves()
        # for i in range(len(moves)-1,-1,-1):
        #     self.makeMove(moves[i])
            
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         moves.remove(moves[i])
            
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        # if len(moves) == 0:
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False


        # return moves


    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
    
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        #print([x.startRow for x in moves])
        return moves

    #get pawn moves
    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.removes(self.pins[i])
                break





        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))

            if c-1>= 0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 < 7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
    
        else:
            if self.board[r+1][c] == '--':
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == '--':
                        moves.append(Move((r,c),(r+2,c),self.board))
                
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c),(r+1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))



    def getRookMoves(self,r,c,moves):
        
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.removes(self.pins[i])
                break
        
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]

                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break

                else:
                    break


    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.removes(self.pins[i])
                break
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
    

    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.removes(self.pins[i])
                break
        directions = ((-1,-1), (1,1),(-1,1),(1,-1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]

                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break

                else:
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        #kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1))

        rowMoves = (-1,-1,-1,0,0,1,1,1)
        colMoves = (-1,0,1,-1,1,-1,0,1)

        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:

                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow,endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r,c),(endRow,endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r,c)

                    else:
                        self.blackKingLocation = (r,c)



    def checkForPinsAndChecks(self):
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.whiteToMove:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.whiteKingLocation[0]
            start_col = self.whiteKingLocation[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.blackKingLocation[0]
            start_col = self.blackKingLocation[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

         

class Move():

    ranksToRows = { "1": 7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}

    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a": 0, "b":1,"c":2,"d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




