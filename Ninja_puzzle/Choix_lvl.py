class Map_lvl:
    def __init__(self, lvl):
        self.maptxt  = "lvl"+str(lvl)+".txt"
        self.num = lvl

        self.jump = False
        if lvl > 3:
            self.jump = True

        self.back = True
        if lvl >= 7:
            self.back = False

