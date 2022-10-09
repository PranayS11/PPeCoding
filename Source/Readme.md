
# Snakes and Ladders

## Questions
- Can we use python to code this machine coding round?
- There are some edge cases while positioning snakes and ladders on board in which we should show error at input of the game or keep playing.
    e.g. if snake head point is ladder top point and snake tail cell is ladder bottom cell, the player can get stuck in infinite loop.
- Is last cell of board is considered to a be finish point?
- Can a snake head be placed at finish point, what to do in this scenario?
As per current understanding, Can you confirm on following:
- Separate config file will be supplied to setup the board.
    - Number of players: N (From config file, max players that can play at a time) (N >= 1)
    - Board Size: BS (BS x BS) (From config file, dimension of the board) (BS >= 1)
    - Number of Snakes: S (From config file, max snakes that can be added on board) (S >= 0)
    - Number of Ladders: L (From config file, max ladders that can be added on board) (L >= 0)
    - Number of Dies: D (From config file, dies used while playing the round) (D >= 1)
    - Movement Strategy: MS (From config file, can be "MIN" | "MAX" | "SUM")
- Input taken at the setup of every round.
    - Total Snakes SI (Can be 0-S snakes)
    - Following SI lines contains pair (Snake’s Head and Snake’s Tail)
    - Total Ladders LI (Can be 0-L ladders)
    - Following LI lines contains pair (Ladder bottom and Ladder top)
    - NI no of players (Can be 0-N max players)
    - Following NI lines contains names & starting locations of each Player
    - An override to manually enter the D die values that each player rolled in each turn. (Can you give more insight to it, is it a flag in config where we enable manual play)
