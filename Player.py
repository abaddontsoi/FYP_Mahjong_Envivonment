import MahjongTiles

class Player:
    def __init__(self, id = None):
        self.hand = []
        self.id = id
        self.called_tuples = []

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
    
    def clear_hand(self):
        self.hand = []
    
    def call_response(self, call_tile: MahjongTiles.MahjongTiles, chow_allowed = False):
        available_actions = []
        # Put those selected mahjong tiles to self.called_tuples, responses are: 
        # 'win'
        # 'kong'
        
        # 'pong'
        call_tile_id = call_tile.classId
        count = 0
        for t in self.hand:
            if t.classId == call_tile_id:
                count += 1
        if count >= 2:
            available_actions.append('pong')
        # 'chow'

        # Choose action
        if available_actions:
            action = int(input(f"{str(available_actions)}: "))
            return available_actions[action]
        
        return False
    
    def win(self, call_tile: MahjongTiles.MahjongTiles):
        pass
    
    def kong(self, call_tile: MahjongTiles.MahjongTiles):
        pass
    
    def pong(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        pong_tiles = [t for t in self.hand if t.classId == call_tile_id]
        self.hand = [t for t in self.hand if t.classId != call_tile_id]
        
        pong_tiles.append(call_tile)
        self.called_tuples.append(tuple(pong_tiles))

    def chow(self, call_tile: MahjongTiles.MahjongTiles):
        pass