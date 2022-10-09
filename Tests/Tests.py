from Source.App import App
from Source.Exceptions import SetupException, InputException
import unittest


class Tests(unittest.TestCase):
    def testSnakeBit(self):
        players = [("PPS", 1)]
        snakePos = [(10, 2)]
        rolls = [[4, 5]]
        app = App()
        app.setup("../config.json")
        for i in snakePos:
            app.addSnake(i[0], i[1])
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 1)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f"{players[0][0]} rolled a {tot} and bitten by a snake at {snakePos[0][0]} and moved from {snakePos[0][0]} to {snakePos[0][1]}")
    
    def testLadderClimb(self):
        players = [("PPS", 1)]
        ladderPos = [(3, 10)]
        rolls = [[1, 1]]
        app = App()
        app.setup("../config.json")
        for i in ladderPos:
            app.addLadder(i[0], i[1])
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 1)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f"{players[0][0]} rolled a {tot} and climbed the ladder at {ladderPos[0][0]} and moved from {ladderPos[0][0]} to {ladderPos[0][1]}")
    
    def testCrocBit(self):
        players = [("PPS", 1)]
        crocPos = [10]
        rolls = [[4, 5]]
        app = App()
        app.setup("../config.json")
        for i in crocPos:
            app.addCrocodile(i)
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 1)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f"{players[0][0]} rolled a {tot} and bitten by a crocodile at {crocPos[0]} and moved from {crocPos[0]} to {crocPos[0] - 5}")
    
    def testMineAndRoundRobinAndWaiting(self):
        players = [("PPS", 1), ("PPS1", 1)]
        minePos = [10]
        rolls = [[4, 5], [5, 5], [5, 5]]
        app = App()
        app.setup("../config.json")
        for i in minePos:
            app.addMine(i)
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 5)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f'{players[0][0]} rolled a {tot} and stepped on a mine at {minePos[0]} have to wait 2 turns')
        tot1 = sum(rolls[1])
        self.assertEqual(app.board.outCache[1],
                         f'{players[1][0]} rolled a {tot1} and moved from {players[1][1]} to {players[1][1] + tot1}')
        self.assertEqual(app.board.outCache[2], f'{players[0][0]} have to wait for 1 more turn since stepped on a mine')
        tot2 = sum(rolls[2])
        self.assertEqual(app.board.outCache[3],
                         f'{players[1][0]} rolled a {tot2} and moved from {players[1][1] + tot1} to {players[1][1] + tot1 + tot2}')
        self.assertEqual(app.board.outCache[4], f'{players[0][0]} can play from next turn since stepped on a mine')
        
        # self.assertEqual(app.board.outCache[0],
        #                  f"{players[0][0]} rolled a {tot} and bitten by a snake at {snakePos[0][0]} and moved from {snakePos[0][0]} to {snakePos[0][1]}")
    
    def testMoveGreaterThan100(self):
        players = [("PPS", 98)]
        rolls = [[1, 2]]
        app = App()
        app.setup("../config.json")
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 1)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f"{players[0][0]} can't move since position more than 100")
    
    def testMoveOnOtherPlayerCell(self):
        players = [("PPS", 1), ("PPS1", 1)]
        rolls = [[4, 5], [4, 5]]
        app = App()
        app.setup("../config.json")
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        self.assertEqual(len(app.board.outCache), 3)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f'{players[0][0]} rolled a 9 and moved from {players[0][1]} to {players[0][1] + tot}')
        tot1 = sum(rolls[1])
        self.assertEqual(app.board.outCache[1],
                         f'{players[1][0]} resets {players[0][0]} to start')
        self.assertEqual(app.board.outCache[2],
                         f'{players[1][0]} rolled a 9 and moved from {players[1][1]} to {players[1][1] + tot1}')
    
    def testChainingSnakeLadderCrocodileMine(self):
        players = [("PPS", 1)]
        snakePos = [(10, 2)]
        ladderPos = [(2, 12)]
        crocPos = [12]
        minePos = [7]
        rolls = [[4, 5]]
        app = App()
        app.setup("../config.json")
        for i in snakePos:
            app.addSnake(i[0], i[1])
        for i in ladderPos:
            app.addLadder(i[0], i[1])
        for i in crocPos:
            app.addCrocodile(i)
        for i in minePos:
            app.addMine(i)
        for i in players:
            app.addPlayer(i[0], i[1])
        for i in rolls:
            app.roll(i)
        print(app.board.outCache)
        self.assertEqual(len(app.board.outCache), 6)
        tot = sum(rolls[0])
        self.assertEqual(app.board.outCache[0],
                         f"{players[0][0]} rolled a {tot} and bitten by a snake at {snakePos[0][0]} and moved from {snakePos[0][0]} to {snakePos[0][1]}")
        self.assertEqual(app.board.outCache[1],
                         f"{players[0][0]} rolled a 0 and climbed the ladder at {ladderPos[0][0]} and moved from {ladderPos[0][0]} to {ladderPos[0][1]}")
        self.assertEqual(app.board.outCache[2],
                         f"{players[0][0]} rolled a 0 and bitten by a crocodile at {crocPos[0]} and moved from {crocPos[0]} to {crocPos[0] - 5}")
        self.assertEqual(app.board.outCache[3],
                         f'{players[0][0]} rolled a 0 and stepped on a mine at {minePos[0]} have to wait 2 turns')
        self.assertEqual(app.board.outCache[4], f'{players[0][0]} have to wait for 1 more turn since stepped on a mine')
        self.assertEqual(app.board.outCache[5], f'{players[0][0]} can play from next turn since stepped on a mine')
    
    def testInfiniteSnakeLadder(self):
        snakePos = [(10, 2)]
        ladderPos = [(2, 10)]
        app = App()
        app.setup("../config.json")
        for i in snakePos:
            app.addSnake(i[0], i[1])
        with self.assertRaises(SetupException) as cm:
            app.addLadder(ladderPos[0][0], ladderPos[0][1])
        self.assertEqual(str(cm.exception), "!!Board Setup Error!! Infinite snake ladder cycle detected")
    
    def testInfiniteCrocLadder(self):
        crocPos = [10]
        ladderPos = [(5, 10)]
        app = App()
        app.setup("../config.json")
        for i in crocPos:
            app.addCrocodile(i)
        with self.assertRaises(SetupException) as cm:
            app.addLadder(ladderPos[0][0], ladderPos[0][1])
        self.assertEqual(str(cm.exception), "!!Board Setup Error!! Infinite crocodile ladder cycle detected")
    
    def testInvalidCroc(self):
        crocPos = [4]
        app = App()
        app.setup("../config.json")
        with self.assertRaises(InputException) as cm:
            app.addCrocodile(crocPos[0])
        print(cm.exception)
        self.assertEqual(str(cm.exception), "!!Invalid Input Error!! Wrong value range for Crocodile Position")
    
    def testDualSnakeConfusion(self):
        snakePos = [(10, 2), (10, 8)]
        app = App()
        app.setup("../config.json")
        with self.assertRaises(SetupException) as cm:
            for i in snakePos:
                app.addSnake(i[0], i[1])
        self.assertEqual(str(cm.exception), "!!Board Setup Error!! One Snake Head is already present in the cell")
    
    def testDualLadderConfusion(self):
        ladderPos = [(2, 10), (2, 30)]
        app = App()
        app.setup("../config.json")
        with self.assertRaises(SetupException) as cm:
            for i in ladderPos:
                app.addLadder(i[0], i[1])
        self.assertEqual(str(cm.exception), "!!Board Setup Error!! One Ladder Bottom is already present in the cell")
    
    # For reference
    # def testMaster(self):
    #     """
    #     - Snake bit
    #     :return:
    #     """
    #     players = [("PPS", 1)]
    #     snakePos = [(10, 2)]
    #     ladderPos = []
    #     crocPos = []
    #     minePos = []
    #     rolls = [[4, 5]]
    #     app = App()
    #     app.setup("../config.json")
    #     for i in snakePos:
    #         app.addSnake(i[0], i[1])
    #     for i in ladderPos:
    #         app.addLadder(i[0], i[1])
    #     for i in crocPos:
    #         app.addCrocodile(i)
    #     for i in minePos:
    #         app.addMine(i)
    #     for i in players:
    #         app.addPlayer(i[0], i[1])
    #     for i in rolls:
    #         app.roll(i)
    #     print(app.board.outCache)
    #     self.assertEqual(len(app.board.outCache), 1)
    #     tot = sum(rolls[0])
    #     self.assertEqual(app.board.outCache[0],
    #                      f"{players[0][0]} rolled a {tot} and bitten by a snake at {snakePos[0][0]} and moved from {snakePos[0][0]} to {snakePos[0][1]}")
    
    if __name__ == '__main__':
        unittest.main()
