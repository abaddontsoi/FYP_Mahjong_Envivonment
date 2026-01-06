import MahjongTiles

class Player:
    def __init__(self):
        self.hand = []

    def draw_tiles(self, tiles: list[MahjongTiles.MahjongTiles]):
        self.hand += tiles
        self.hand.sort(key=lambda x: x.classId)

    def display_hand(self):
        print(self.get_hand_as_string())

    def get_hand_as_string(self):
        return ' '.join([t.tile_class_info[1] for t in self.hand])
    
    def discard(self):
        self.display_hand()
        discard_idx = int(input("Input index to discard: "))
        return self.hand.pop(discard_idx)