class Actor:
    def __init__(self) -> None:
        self.direction = (0, 0)
    
    def updatedir(self, dir):
        self.direction = dir