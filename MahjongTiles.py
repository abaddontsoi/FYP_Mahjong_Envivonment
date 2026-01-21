import pygame
tile_classes = {
    1: ('1m', '\U0001F007', 'assets/1m.png'), 
    2: ('2m', '\U0001F008', 'assets/2m.png'), 
    3: ('3m', '\U0001F009', 'assets/3m.png'), 
    4: ('4m', '\U0001F00A', 'assets/4m.png'),
    5: ('5m', '\U0001F00B', 'assets/5m.png'), 
    6: ('6m', '\U0001F00C', 'assets/6m.png'), 
    7: ('7m', '\U0001F00D', 'assets/7m.png'), 
    8: ('8m', '\U0001F00E', 'assets/8m.png'), 
    9: ('9m', '\U0001F00F', 'assets/9m.png'),
    10: ('1p', '\U0001F019', 'assets/1p.png'), 
    11: ('2p', '\U0001F01A', 'assets/2p.png'), 
    12: ('3p', '\U0001F01B', 'assets/3p.png'), 
    13: ('4p', '\U0001F01C', 'assets/4p.png'), 
    14: ('5p', '\U0001F01D', 'assets/5p.png'),
    15: ('6p', '\U0001F01E', 'assets/6p.png'), 
    16: ('7p', '\U0001F01F', 'assets/7p.png'), 
    17: ('8p', '\U0001F020', 'assets/8p.png'), 
    18: ('9p', '\U0001F021', 'assets/9p.png'), 
    19: ('1s', '\U0001F010', 'assets/1s.png'), 
    20: ('2s', '\U0001F011', 'assets/2s.png'), 
    21: ('3s', '\U0001F012', 'assets/3s.png'), 
    22: ('4s', '\U0001F013', 'assets/4s.png'), 
    23: ('5s', '\U0001F014', 'assets/5s.png'),
    24: ('6s', '\U0001F015', 'assets/6s.png'), 
    25: ('7s', '\U0001F016', 'assets/7s.png'), 
    26: ('8s', '\U0001F017', 'assets/8s.png'), 
    27: ('9s', '\U0001F018', 'assets/9s.png'), 
    28: ('1z', '\U0001F000', 'assets/1z.png'), 
    29: ('2z', '\U0001F001', 'assets/2z.png'), 
    30: ('3z', '\U0001F002', 'assets/3z.png'), 
    31: ('4z', '\U0001F003', 'assets/4z.png'),
    32: ('5z', '\U0001F006', 'assets/5z.png'), 
    33: ('6z', '\U0001F005', 'assets/6z.png'), 
    34: ('7z', '\U0001F004\uFE0E', 'assets/7z.png')
}


class MahjongTiles(pygame.sprite.Sprite):
    def __init__(self, classId: int, init_pos = (0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.classId = classId
        self.tile_class_info = tile_classes[self.classId]
        self.tile_suit = self.tile_class_info[0][1]
        self.tile_number = int(self.tile_class_info[0][0])
        self.tile_image_path = self.tile_class_info[2]
        self.image = pygame.image.load(self.tile_image_path)
        self.rect = self.image.get_rect()
        self.rect.bottomright = init_pos
        # print(self.rect.width, self.rect.height)

    def print_tile(self):
        print(self.tile_class_info[1])

    def __str__(self):
        return self.tile_class_info[1]