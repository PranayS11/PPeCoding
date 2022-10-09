from Source.Exceptions import SetupException, InputException
from Source.Constants import UserMessages


class Player:
    
    def __init__(self, name: str, stPosition: int):
        self.name = name
        self.position = stPosition
        self.chanceWait = 0
    
    def setPosition(self, position: int):
        self.position = position
    
    def steppedOnMine(self):
        self.chanceWait = 2
    
    def decrChanceWait(self):
        self.chanceWait -= 1


class Cell:
    
    def __init__(self, cellId):
        self.id = cellId
        self.snakeTail = None
        self.ladderHead = None
        self.player = None
        self.isCrocodile = False
        self.isMine = False
    
    def setSnakeTail(self, tail: int):
        if self.snakeTail is not None:
            raise SetupException(SetupException.e1)
        if self.isCrocodile:
            raise SetupException(SetupException.e3)
        self.snakeTail = tail
    
    def setLadderHead(self, head: int):
        if self.ladderHead is not None:
            raise SetupException(SetupException.e2)
        self.ladderHead = head
    
    def setIsCrocodile(self):
        if self.snakeTail is not None:
            raise SetupException(SetupException.e1)
        if self.isCrocodile:
            raise SetupException(SetupException.e3)
        self.isCrocodile = True
    
    def setIsMine(self):
        if self.isMine:
            raise SetupException(SetupException.e4)
        self.isMine = True
    
    def setPlayer(self, player: Player):
        self.player = player


class Board:
    
    class MoveEnum:
        MIN = "MIN"
        MAX = "MAX"
        SUM = "SUM"
        all = [MIN, MAX, SUM]
    
    def __init__(self, config):
        try:
            self.maxPlayers = config["N"]
            self.players: list[Player] = []
            self.playerTurn = 0
            self.dimension = config["BS"]
            self.maxSnakes = config["S"]
            self.snakes = 0
            self.maxLadders = config["L"]
            self.ladders = 0
            self.dies = config["D"]
            self.strategy = config["MS"]
            self.cells: list[Cell] = [Cell(i + 1) for i in range(self.dimension * self.dimension)]
            self.outCache = [] if config["ENABLE_TESTING"] else None
            if self.strategy not in Board.MoveEnum.all:
                raise Exception
        except Exception:
            raise SetupException(SetupException.e0)
    
    def _out(self, line):
        if self.outCache is not None:
            self.outCache.append(line)
        print(line)
    
    def addSnake(self, head: int, tail: int):
        if tail >= head or head >= self.dimension * self.dimension or tail < 1:
            raise InputException(InputException.e1.format(variable="Snake Position"))
        cell = self.cells[head - 1]
        cellDestination = self.cells[tail - 1]
        if cellDestination.ladderHead is not None and cellDestination.ladderHead == cell.id:
            raise SetupException(SetupException.e5)
        cell.setSnakeTail(tail)
    
    def addLadder(self, top: int, bottom: int):
        if bottom >= top or top > self.dimension * self.dimension or bottom < 1:
            raise InputException(InputException(InputException.e1.format(variable="Ladder Position")))
        cell = self.cells[bottom - 1]
        cellDestination = self.cells[top - 1]
        if cellDestination.snakeTail is not None and cellDestination.snakeTail == cell.id:
            raise SetupException(SetupException.e5)
        if top - bottom == 5 and cellDestination.isCrocodile:
            raise SetupException(SetupException.e6)
        cell.setLadderHead(top)
    
    def addCrocodile(self, position: int):
        if position >= self.dimension * self.dimension or position < 6:
            raise InputException(InputException.e1.format(variable="Crocodile Position"))
        cell = self.cells[position - 1]
        cellDestination = self.cells[position - 1 - 5]
        if cellDestination.ladderHead is not None and cellDestination.ladderHead == cell.id:
            raise SetupException(SetupException.e6)
        cell.setIsCrocodile()
    
    def addMine(self, position: int):
        if position > self.dimension * self.dimension or position < 1:
            raise InputException(InputException.e1.format(variable="Mines Position"))
        cell = self.cells[position - 1]
        cell.setIsMine()
    
    def addPlayer(self, name: str, stPosition: int):
        if stPosition >= self.dimension * self.dimension or stPosition < 1:
            raise InputException(InputException.e1.format(variable="Player's Starting Position"))
        self.players.append(Player(name, stPosition))
    
    def move(self, player: Player, score: int, position: int):
        cell = self.cells[position - 1]
        if cell.player is not None:
            if cell.id != 1:
                cell.player.setPosition(1)
                if cell.player.chanceWait > 0:
                    cell.player.chanceWait = 0
                self._out(UserMessages.playerReset.format(playerName=cell.player.name,
                                                          newPlayerName=player.name))
        cell.setPlayer(player)
        if cell.snakeTail is not None:
            player.setPosition(position)
            self._out(UserMessages.snakeBit.format(playerName=player.name, score=score,
                                                   edPosition=position, newPosition=cell.snakeTail))
            self.move(player, 0, cell.snakeTail)
        elif cell.ladderHead is not None:
            player.setPosition(position)
            self._out(UserMessages.ladderClimb.format(playerName=player.name, score=score,
                                                      edPosition=position, newPosition=cell.ladderHead))
            self.move(player, 0, cell.ladderHead)
        elif cell.isCrocodile:
            player.setPosition(position)
            self._out(UserMessages.crocodileBit.format(playerName=player.name, score=score,
                                                       edPosition=position, newPosition=position - 5))
            self.move(player, 0, position - 5)
        elif cell.isMine:
            player.steppedOnMine()
            player.setPosition(position)
            self._out(UserMessages.mineStep.format(playerName=player.name, score=score, edPosition=position))
        else:
            prevPos = player.position
            player.setPosition(position)
            if score > 0:
                self._out(UserMessages.rollSuccess.format(playerName=player.name, score=score,
                                                          stPosition=prevPos, edPosition=position))
    
    def roll(self, scores: list[int]):
        totScore = 0
        strat = self.strategy
        # calculate scores
        for score in scores:
            if score > 6 or score < 1:
                raise InputException(InputException.e1.format(variable="Die Value"))
            if strat == Board.MoveEnum.MIN:
                totScore = min(totScore, score)
            if strat == Board.MoveEnum.MAX:
                totScore = max(totScore, score)
            if strat == Board.MoveEnum.SUM:
                totScore += score
        player = self.players[self.playerTurn]
        newPosition = player.position + totScore
        if player.position == self.dimension * self.dimension:
            self._out(UserMessages.playerReached.format(playerName=player.name))
        elif newPosition <= self.dimension * self.dimension:
            self.move(player, totScore, newPosition)
        else:
            self._out(UserMessages.scoreGt100.format(playerName=player.name))
        # player(s) turn skip due to mine stepping
        self.playerTurn = (self.playerTurn + 1) % len(self.players)
        nextPlayer = self.players[self.playerTurn]
        while nextPlayer.chanceWait > 0:
            if nextPlayer.chanceWait == 2:
                self._out(UserMessages.mineWait2.format(playerName=nextPlayer.name))
            else:
                self._out(UserMessages.mineWait1.format(playerName=nextPlayer.name))
            nextPlayer.decrChanceWait()
            self.playerTurn = (self.playerTurn + 1) % len(self.players)
            nextPlayer = self.players[self.playerTurn]
