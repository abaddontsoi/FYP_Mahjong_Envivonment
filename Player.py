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
        call_tile_id = call_tile.classId
        count = 0
        for t in self.hand:
            if t.classId == call_tile_id:
                count += 1
        if count == 3:
            available_actions.append('kong')
        
        # 'pong'
        count = 0
        for t in self.hand:
            if t.classId == call_tile_id:
                count += 1
        if count >= 2:
            available_actions.append('pong')
        
        # 'chow'
        neighbor_number_range = range(max(1, call_tile.tile_number - 2), min(9, call_tile.tile_number + 2) + 1)
        print(neighbor_number_range)
        neighbor_tiles = [t for t in self.hand if t.tile_number in neighbor_number_range and t.tile_suit == call_tile.tile_suit]
        # From t.tile_number - 2 to t.tile_number + 2, if exists in hand, set to 1
        neighbor_hit = [0, 0, 0, 0, 0]
        for neighbor in neighbor_tiles:
            neighbor_hit[neighbor.tile_number - call_tile.tile_number + 2] = 1
        
        for i in range(2, 5):
            if neighbor_hit[i] and neighbor_hit[i-1] and neighbor_hit[i-2]:
                # A 'chow' combination exists
                available_actions.append('chow')
                break

        # Choose action
        if available_actions:
            action = int(input(f"{str(available_actions)}: "))
            return available_actions[action]
        
        return False
    
    def find_first_by_number(self, tile_number: int):
        for i in range(len(self.hand)):
            if self.hand[i].tile_number == tile_number:
                return i
        return -1

    def win(self, call_tile: MahjongTiles.MahjongTiles):
        pass
    
    def kong(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        kong_tiles = [t for t in self.hand if t.classId == call_tile_id]
        self.hand = [t for t in self.hand if t.classId != call_tile_id]
        
        kong_tiles.append(call_tile)
        self.called_tuples.append(tuple(kong_tiles))
    
    def additional_kong(self, call_tile: MahjongTiles.MahjongTiles):
        ...
    
    def hidden_kong(self):
        ...
    
    def pong(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        pong_tiles = [t for t in self.hand if t.classId == call_tile_id]
        self.hand = [t for t in self.hand if t.classId != call_tile_id]
        
        pong_tiles.append(call_tile)
        self.called_tuples.append(tuple(pong_tiles))

    def chow(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        
        # Draw the tile to hand first
        self.hand.append(call_tile)
        self.hand.sort(key=lambda x: x.classId)

        neighbor_number_range = range(max(1, call_tile.tile_number - 2), min(9, call_tile.tile_number + 2) + 1)
        neighbor_tiles = [t for t in self.hand if t.tile_number in neighbor_number_range and t.tile_suit == call_tile.tile_suit]
        # From t.tile_number - 2 to t.tile_number + 2, if exists in hand, set to 1
        neighbor_hit = [0, 0, 0, 0, 0]
        chow_proposals = []
        for neighbor in neighbor_tiles:
            neighbor_hit[neighbor.tile_number - call_tile.tile_number + 2] = 1
        
        for i in range(2, 5):
            if neighbor_hit[i] and neighbor_hit[i-1] and neighbor_hit[i-2]:
                # A 'chow' combination exists
                # Propose a 'chow' combination using index
                chow_combination = (
                    self.find_first_by_number(i - 2 + call_tile.tile_number),
                    self.find_first_by_number(i - 1 - 2 + call_tile.tile_number),
                    self.find_first_by_number(i - 2 - 2 + call_tile.tile_number),
                )
                chow_proposals.append(chow_combination)
        
        chow_selection = int(input(f"Choose chow combination [{0}] - [{len(chow_proposals) - 1}]: "))
        chow_tiles = [t for idx, t in enumerate(self.hand) if idx in chow_proposals[chow_selection]]
        self.hand = [t for idx, t in enumerate(self.hand) if idx not in chow_proposals[chow_selection]]

        self.called_tuples.append(tuple(chow_tiles))