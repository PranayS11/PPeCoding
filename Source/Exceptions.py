class SetupException(Exception):
    e0 = "Board Config Failure"
    e1 = "One Snake Head is already present in the cell"
    e2 = "One Ladder Bottom is already present in the cell"
    e3 = "One Crocodile Head is already present in the cell"
    e4 = "One Mine is already present in the cell"
    e5 = "Infinite snake ladder cycle detected"
    e6 = "Infinite crocodile ladder cycle detected"
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f'!!Board Setup Error!! {self.message}'


class InputException(Exception):
    e0 = "Wrong no. inputs or input types are supplied"
    e1 = "Wrong value range for {variable}"
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f'!!Invalid Input Error!! {self.message}'
