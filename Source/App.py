"""
>> Snake And Ladders <<
"""
import json
import random
import logging as l
import time
from Source.Services import Board
from Source.Exceptions import SetupException, InputException
from Source.Constants import InputMessages

l.basicConfig(level=l.INFO)


class Utils:
    @staticmethod
    def input(expectedLength: int, isInts: bool):
        try:
            if expectedLength == 1:
                return int(input()) if isInts else input()
            else:
                inps = input().split(" ")
                if isInts:
                    inps = [int(i) for i in inps]
                if len(inps) != expectedLength:
                    raise Exception()
                return inps
        except Exception:
            raise InputException(InputException.e0)


class App:
    board = None
    
    @staticmethod
    def addLadder(bottom: int, top: int):
        App.board.addLadder(top, bottom)
    
    @staticmethod
    def addSnake(head: int, tail: int):
        App.board.addSnake(head, tail)
    
    @staticmethod
    def addPlayer(name: str, stPosition: int):
        App.board.addPlayer(name, stPosition)
    
    @staticmethod
    def addCrocodile(position: int):
        App.board.addCrocodile(position)
    
    @staticmethod
    def addMine(position: int):
        App.board.addMine(position)
    
    @staticmethod
    def roll(scores: list[int]) -> bool:
        App.board.roll(scores)
    
    @staticmethod
    def autoPlay():
        while True:
            scores = [random.randint(1, 6) for _ in range(App.board.dies)]
            App.board.roll(scores)
            time.sleep(5)
    
    @staticmethod
    def setup(fileName):
        try:
            f = open(fileName)
            config = json.loads(f.read())
            f.close()
        except Exception:
            raise SetupException(SetupException.e0)
        l.debug("Config Added")
        App.board = Board(config)
    
    @staticmethod
    def start():
        try:
            App.setup("config.json")
            l.debug("Enter No of snakes")
            si = Utils.input(1, True)
            
            for i in range(si):
                l.debug("Enter Head and Tail")
                head, tail = Utils.input(2, True)
                App.addSnake(head, tail)
            
            l.debug("Enter Ladders")
            li = Utils.input(1, True)
            for i in range(li):
                l.debug("Enter Bottom and Top")
                bottom, top = Utils.input(2, True)
                App.addLadder(bottom, top)
            
            l.debug("Enter Players")
            n = Utils.input(1, True)
            if n < 1:
                raise InputException(InputException.e1.format(variable="Players"))
            for i in range(n):
                l.debug("Enter Name and Position")
                name, coordinate = Utils.input(2, False)
                try:
                    coordinate = int(coordinate)
                except Exception:
                    raise InputException(InputException.e0)
                App.addPlayer(name, coordinate)
            
            l.debug("Enter Crocodiles")
            try:
                ci = Utils.input(1, True)
            except Exception:
                print(InputMessages.i1)
                ci = 0
            for i in range(ci):
                l.debug("Enter Position")
                coordinate = Utils.input(1, True)
                App.addCrocodile(coordinate)
            
            l.debug("Enter Mines")
            try:
                mi = Utils.input(1, True)
            except Exception:
                print(InputMessages.i2)
                mi = 0
            for i in range(mi):
                l.debug("Enter Position")
                coordinate = Utils.input(1, True)
                App.addMine(coordinate)
            
            l.debug("Let's Play")
            config = json.loads(open("config.json").read())
            if config.get("MANUAL_PLAY") is True:
                while True:
                    l.debug("Enter Values")
                    scores = Utils.input(config["D"], True)
                    resp = App.roll(scores)
                    if resp:
                        break
            else:
                App.autoPlay()
        except Exception as e:
            print(e)
