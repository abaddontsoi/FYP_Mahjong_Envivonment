from MahjongTiles import MahjongTiles

class FaanCalculator:
    FaanList = {
        'self_drawn': 1,
        'white': 1,
        'no_call': 1,
        'red': 1,
        'green': 1,
        'round_wind': 1,
        'round_position': 1,
        'mixed_orphans': 1,
        'all_chow_hand': 1,
        'robbing_additional_kong': 1,
        'self_drawn_on_last_tile': 1,
        'self_drawn_after_kong': 1,
        'all_pong_hand': 3,
        'clean_hand': 3,
        'little_dragon_hand': 5,
        'pure_suit': 7,
        'great_dragon_hand': 10,
        'self_drawn_after_2kong': 10,
        'pure_orphans_hand': 10,
        'all_winds_and_dragons': 10, 
        # 9子連環
        '9_gates_to_haven': 10, 
        '13_orphans': 10,
        'little_4_winds_hand': 10,
        'great_4_winds_hand': 10,
        'all_kong_hand': 10,
        'four_hidden_pong': 10,
        'havenly_hand': 10,
        'earthly_hand': 10,
    }
    def __init__(self, hand, called_tile, round = 0, position = 0):
        self.hand = hand
        self.called_tile = called_tile
        self.round = round
        self.position = position
    
    def update_hand_and_called_tile(self, hand, called_tile):
        self.hand = hand
        self.called_tile = called_tile

    def check_tuple_type(self, tuple: tuple[MahjongTiles.MahjongTiles]):
        if len(tuple) == 4:
            if tuple[0].classId == tuple[1].classId == tuple[2].classId == tuple[3].classId:
                return 'kong'
        if len(tuple) == 3:
            if tuple[0].classId == tuple[1].classId == tuple[2].classId:
                return 'pong'
            if tuple[2].tile_number == tuple[1].tile_number + 1 and tuple[1].tile_number == tuple[0].tile_number + 1:
                return 'chow'
        return None

    def get_tuples_from_hand(self):
        ...

    def no_call(self):
        if self.called_tile:
            return False
        return True
    
    def self_drawn(self):
        return False
    
    def white(self):
        for t in self.called_tile:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 32:
                    return True
        
        if len(self.hand) < 2:
            return False
        
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 32:
                    return True

        return False
    
    def green(self):
        for t in self.called_tile:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 33:
                    return True
        
        if len(self.hand) < 2:
            return False
        
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 33:
                    return True

        return False
    
    def red(self):
        for t in self.called_tile:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 34:
                    return True
        
        if len(self.hand) < 2:
            return False
        
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 34:
                    return True

        return False
    
    def round_wind(self):
        return False
    
    def round_position(self):
        return False

    def mixed_orphans(self):
        for t in self.called_tile:
            if self.check_tuple_type(t) != 'pong':
                return False
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId not in [1, 9, 10, 18, 19, 27, 28, 29, 30, 31, 32, 33, 34]:
                    return False

        return True

    def all_chow_hand(self):
        return False

    def robbing_additional_kong(self):
        return False

    def self_drawn_on_last_tile(self):
        return False

    def self_drawn_after_kong(self):
        return False

    def all_pong_hand(self):
        return False

    def clean_hand(self):
        return False

    def little_dragon_hand(self):
        return False

    def pure_suit(self):
        if not self.no_call():
            flattened_called_tile = [item for tup in self.called_tile for item in tup]
            full_hand = self.hand + flattened_called_tile
            for idx in range(1, len(self.hand)):
                if self.hand[idx].tile_suit != full_hand[idx - 1].tile_suit:
                    return False
        else:
            for idx in range(1, len(self.hand)):
                if self.hand[idx].tile_suit != full_hand[idx - 1].tile_suit:
                    return False
        
        return False

    def great_dragon_hand(self):
        return False

    def self_drawn_after_2kong(self):
        if self.no_call():
            return False
    
    def pure_orphans_hand(self):
        return False

    def all_winds_and_dragons(self):
        return False

    def chained_1_to_9(self):
        if not self.no_call():
            return False

    def thirteen_orphans(self):
        if not self.no_call():
            return False

    def little_4_winds_hand(self):
        return False

    def great_4_winds_hand(self):
        return False

    def all_kong_hand(self):
        if self.no_call():
            return False

    def four_hidden_pong(self):
        if not self.no_call():
            return False
    