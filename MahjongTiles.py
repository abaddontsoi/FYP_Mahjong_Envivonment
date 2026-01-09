tile_classes = {
    1: ('1m', '\U0001F007'), 
    2: ('2m', '\U0001F008'), 
    3: ('3m', '\U0001F009'), 
    4: ('4m', '\U0001F00A'),
    5: ('5m', '\U0001F00B'), 
    6: ('6m', '\U0001F00C'), 
    7: ('7m', '\U0001F00D'), 
    8: ('8m', '\U0001F00E'), 
    9: ('9m', '\U0001F00F'),
    10: ('1p', '\U0001F019'), 
    11: ('2p', '\U0001F01A'), 
    12: ('3p', '\U0001F01B'), 
    13: ('4p', '\U0001F01C'), 
    14: ('5p', '\U0001F01D'),
    15: ('6p', '\U0001F01E'), 
    16: ('7p', '\U0001F01F'), 
    17: ('8p', '\U0001F020'), 
    18: ('9p', '\U0001F021'), 
    19: ('1s', '\U0001F010'), 
    20: ('2s', '\U0001F011'), 
    21: ('3s', '\U0001F012'), 
    22: ('4s', '\U0001F013'), 
    23: ('5s', '\U0001F014'),
    24: ('6s', '\U0001F015'), 
    25: ('7s', '\U0001F016'), 
    26: ('8s', '\U0001F017'), 
    27: ('9s', '\U0001F018'), 
    28: ('1z', '\U0001F000'), 
    29: ('2z', '\U0001F001'), 
    30: ('3z', '\U0001F002'), 
    31: ('4z', '\U0001F003'),
    32: ('5z', '\U0001F006'), 
    33: ('6z', '\U0001F005'), 
    34: ('7z', '\U0001F004\uFE0E')
}


class MahjongTiles:
    def __init__(self, classId: int):
        self.classId = classId
        self.tile_class_info = tile_classes[self.classId]
        self.tile_suit = self.tile_class_info[0][1]
        self.tile_number = int(self.tile_class_info[0][0])

    def print_tile(self):
        print(self.tile_class_info[1])

    def __str__(self):
        return self.tile_class_info[1]