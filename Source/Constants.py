class InputMessages:
    i1 = "No crocodiles added in game"
    i2 = "No mines added in game"


class UserMessages:
    rollSuccess = "{playerName} rolled a {score} and moved from {stPosition} to {edPosition}"
    snakeBit = "{playerName} rolled a {score} and bitten by a snake at {edPosition} and moved from {edPosition} to {newPosition}"
    ladderClimb = "{playerName} rolled a {score} and climbed the ladder at {edPosition} and moved from {edPosition} to {newPosition}"
    crocodileBit = "{playerName} rolled a {score} and bitten by a crocodile at {edPosition} and moved from {edPosition} to {newPosition}"
    mineStep = "{playerName} rolled a {score} and stepped on a mine at {edPosition} have to wait 2 turns"
    mineWait2 = "{playerName} have to wait for 1 more turn since stepped on a mine"
    mineWait1 = "{playerName} can play from next turn since stepped on a mine"
    playerReset = "{newPlayerName} resets {playerName} to start"
    playerReached = "{playerName} has reached the finish line !!"
    scoreGt100 = "{playerName} can't move since position more than 100"
