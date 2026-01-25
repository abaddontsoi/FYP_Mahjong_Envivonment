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
    def __init__(self, round = 0, position = 0):
        self.hand = []
        self.call_tile = None
        self.called_tuples = []
        self.round = round
        self.position = position
    
    def update_hand_and_called_tuples(self, hand, called_tuples):
        self.hand = hand
        self.called_tuples = called_tuples

    def update_call_tile(self, call_tile):
        self.call_tile = call_tile
    
    def check_tuple_type(self, tuple: tuple[MahjongTiles]):
        if len(tuple) == 4:
            if tuple[0].classId == tuple[1].classId == tuple[2].classId == tuple[3].classId:
                return 'kong'
        if len(tuple) == 3:
            if tuple[0].classId == tuple[1].classId == tuple[2].classId:
                return 'pong'
            if tuple[2].tile_number == tuple[1].tile_number + 1 and tuple[1].tile_number == tuple[0].tile_number + 1:
                if tuple[0].tile_suit == tuple[1].tile_suit == tuple[2].tile_suit:
                    return 'chow'
        
        return None

    def get_tuples_from_hand(self):
        ...


    # For detecting Faan, assume the hand is a complete hand (4 tuples + 1 pair/13 orphans)
    def no_call(self):
        if self.called_tuples:
            return False
        return True
    
    def self_drawn(self):
        return False
    
    def white(self):
        for t in self.called_tuples:
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
        for t in self.called_tuples:
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
        for t in self.called_tuples:
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
        # Round wind mapping: 0-East, 1-South, 2-West, 3-North
        # Check called tuples first
        for tuple in self.called_tuples:
            if self.check_tuple_type(tuple) == 'pong':
                if tuple[0].classId == 28 + self.round:
                    return True
        
        if len(self.hand) < 2:
            return False
        
        # Check hand tiles
        # When finds a pong shape, check if it is the round wind
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 28 + self.round:
                    return True
        
        return False
    
    def round_position(self):
        # Round position mapping: 0-East, 1-South, 2-West, 3-North
        # Check called tuples first
        for tuple in self.called_tuples:
            if self.check_tuple_type(tuple) == 'pong':
                if tuple[0].classId == 28 + self.position:
                    return True
        
        if len(self.hand) < 2:
            return False
        
        # Check hand tiles
        # When finds a pong shape, check if it is the position wind
        for i in range(2, len(self.hand)):  
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 28 + self.position:
                    return True
        
        return False

    def mixed_orphans(self):
        # Valid pong class
        valid_pong_classes = [1, 9, 10, 18, 19, 27, 28, 29, 30, 31, 32, 33, 34]
        
        # Must be all pong hand
        if not self.all_pong_hand():
            return False
        
        for t in self.called_tuples:
            if t[0].classId not in valid_pong_classes:
                return False
        
        for t in self.hand:
            if t.classId not in valid_pong_classes:
                return False
        
        return True

    def all_chow_hand_helper(self, remaining_hand):
        if not remaining_hand:
            return True
        
        for i in range(len(remaining_hand)):
            first_tile = remaining_hand[i]
            # Try to form a chow with first_tile
            second_tile_number = first_tile.tile_number + 1
            third_tile_number = first_tile.tile_number + 2
            second_tile = None
            third_tile = None

            for j in range(len(remaining_hand)):
                if remaining_hand[j].tile_suit == first_tile.tile_suit:
                    if remaining_hand[j].tile_number == second_tile_number:
                        second_tile = remaining_hand[j]
                    elif remaining_hand[j].tile_number == third_tile_number:
                        third_tile = remaining_hand[j]
            
            if second_tile and third_tile:
                # Formed a chow, remove these tiles and continue
                new_remaining_hand = remaining_hand.copy()
                new_remaining_hand.remove(first_tile)
                new_remaining_hand.remove(second_tile)
                new_remaining_hand.remove(third_tile)
                
                if self.all_chow_hand_helper(new_remaining_hand):
                    return True
        
        return False

    def all_chow_hand(self):
        for t in self.called_tuples:
            if self.check_tuple_type(t) != 'chow':
                return False
        
        for i in range(1, len(self.hand)):
            # Finding pair in hand
            if self.hand[i].classId == self.hand[i - 1].classId:
                # Found pair, remove and check remaining tiles
                pair= (self.hand[i - 1], self.hand[i])
                remaining = [t for t in self.hand if t not in pair]
                if self.all_chow_hand_helper(remaining):
                    return True

        return False

    def robbing_additional_kong(self):
        return False

    def self_drawn_on_last_tile(self):
        return False

    def self_drawn_after_kong(self):
        return False

    def all_pong_hand(self):
        # Consists of all pong/kong tuples and a pair
        for t in self.called_tuples:
            if self.check_tuple_type(t) != 'pong' and self.check_tuple_type(t) != 'kong':
                return False
            
        # Find out the only pair in hand
        pair_found = False
        pair = None
        if len(self.hand) == 2:
            if self.hand[0].classId == self.hand[1].classId:
                pair_found = True
                pair = (self.hand[0], self.hand[1])
        
        if not pair_found:
            for i in range(1, len(self.hand)):
                if self.hand[i].classId == self.hand[i - 1].classId:
                    if i - 2 >= 0:
                        if self.hand[i - 1].classId == self.hand[i - 2].classId:
                            continue
                    if i + 1 < len(self.hand):
                        if self.hand[i].classId == self.hand[i + 1].classId:
                            continue
                    pair_found = True
                    pair = (self.hand[i - 1], self.hand[i])
                    break

        if not pair_found:
            return False
        
        # Check remaining tiles are all pong/kong
        remaining_tiles = [tile for tile in self.hand if tile not in pair]
        for i in range(0, len(remaining_tiles), 3):
            if i + 2 >= len(remaining_tiles):
                return False
            if remaining_tiles[i].classId != remaining_tiles[i + 1].classId or remaining_tiles[i].classId != remaining_tiles[i + 2].classId:
                return False

        return True

    def clean_hand(self):
        return False

    def little_dragon_hand(self):
        return False

    def pure_suit(self):
        if not self.no_call():
            flattened_called_tuples = [item for tup in self.called_tuples for item in tup]
            full_hand = self.hand + flattened_called_tuples
            for idx in range(1, len(self.hand)):
                if self.hand[idx].tile_suit != full_hand[idx - 1].tile_suit:
                    return False
        else:
            for idx in range(1, len(self.hand)):
                if self.hand[idx].tile_suit != full_hand[idx - 1].tile_suit:
                    return False
        
        return False

    def great_dragon_hand(self):
        white_found = False
        green_found = False
        red_found = False

        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 32:
                    white_found = True
                elif t[0].classId == 33:
                    green_found = True
                elif t[0].classId == 34:
                    red_found = True

        if len(self.hand) < 2:
            return False
        
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 32:
                    white_found = True
                elif self.hand[i].classId == 33:
                    green_found = True
                elif self.hand[i].classId == 34:
                    red_found = True

        return white_found and green_found and red_found

    def self_drawn_after_2kong(self):
        if self.no_call():
            return False
    
    def pure_orphans_hand(self):
        # Valid pong class
        valid_pong_classes = [1, 9, 10, 18, 19, 27]

        for t in self.called_tuples:
            if self.check_tuple_type(t) != 'pong':
                return False
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId not in valid_pong_classes:
                    return False

        if len(self.hand) < 2:
            return False

        # Check any pairs in hand is not in valid pong classes
        for i in range(1, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId:
                if self.hand[i].classId not in valid_pong_classes:
                    return False
                
        # Check any pong shape in hand is not in valid pong classes
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId not in valid_pong_classes:
                    return False

        return True

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
        
        if self.all_pong_hand():
            return True
        
        return False
    