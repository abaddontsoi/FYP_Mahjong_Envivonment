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

    def find_first_by_classId(self, classId: int, provided_list: list[MahjongTiles] = None):
        if not provided_list:
            for i in range(len(self.hand)):
                if self.hand[i].classId == classId:
                    return i
        else:
            for i in range(len(provided_list)):
                if provided_list[i].classId == classId:
                    return i
        return -1

    # length must be multiple of 3, max 12
    def count_tuples(self, remaining: list[MahjongTiles]):
        if not remaining or (len(remaining) % 3 != 0) or len(remaining) > 12:
            return 0
            
        # Filter out first pong
        pong_idx = None
        for i in range(2, len(remaining)):
            if remaining[i].classId == remaining[i-1].classId == remaining[i - 2].classId:
                pong_idx = i
                break
        # 'pong' exists case
        if pong_idx:
            return 1 + self.count_tuples(
                [t for idx, t in enumerate(remaining) if idx not in range(pong_idx - 2, pong_idx + 1)]
            )
        else:
            # No 'pong' exists case
            # Permutate and check for all possible chows
            for i in range(3, 28):
                tile_indices = []
                first_chow_tile_idx = self.find_first_by_classId(i - 2, remaining)
                second_chow_tile_idx = self.find_first_by_classId(i - 1, remaining)
                third_chow_tile_idx = self.find_first_by_classId(i, remaining)
                
                if first_chow_tile_idx != -1 and second_chow_tile_idx != -1 and third_chow_tile_idx != -1:
                    tile_indices = [first_chow_tile_idx, second_chow_tile_idx, third_chow_tile_idx]
                    tiles = sorted([t for idx, t in enumerate(remaining) if idx in tile_indices], key= lambda x: x.classId)
                    tiles = tuple(tiles)
                    
                    tuple_type = self.check_tuple_type(tiles)
                    if tuple_type != None:
                        return 1 + self.count_tuples([t for t in remaining if t not in tiles])
            
            return 0


    def is_valid_winning_hand(self):
        # Insert to hand
        remaining = self.hand
        remaining.sort(key= lambda x: x.classId)
        
        # Special winning cases
        # 13 Orphans
        if self.thirteen_orphans():
            return True
        
        # 2 Cases
        required_tuples = 4 - len(self.called_tuples)


        # Filter out 1 pair and check for remainings to see if they can form tuples
        if len(remaining) > 1:
            proposed_eye = []
            for idx in range(1, len(remaining)):
                if remaining[idx].classId == remaining[idx - 1].classId:
                    proposed_eye.append(
                        (remaining[idx - 1], remaining[idx])
                    )

            for eye in proposed_eye:
                tuple_count = self.count_tuples([t for t in remaining if t not in eye])
                if tuple_count == required_tuples:
                    return True


        # 2 tile remains in hand, must be the pair
        if len(remaining) == 2:
            if remaining[0].classId == remaining[1].classId:
                return True

        return False

    # For detecting Faan, assume the hand is a complete valid winning hand (4 tuples + 1 pair/13 orphans)
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
        next_chow, remaining = self.find_next_chow(remaining_hand)
        if next_chow:
            if not remaining:
                return True
            else:
                return self.all_chow_hand_helper(remaining)
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
        flatten_and_combined = []
        for t in self.called_tuples:
            flatten_and_combined.extend(t)
        flatten_and_combined.extend(self.hand)

        # Sort the combined tiles
        flatten_and_combined.sort(key=lambda x: x.classId)

        first_suit = flatten_and_combined[0].tile_suit
        for tile in flatten_and_combined:
            if tile.tile_suit != first_suit and tile.tile_suit != 'z':
                return False
        
        return True

    def little_dragon_hand(self):
        return False

    def pure_suit(self):
        flattened_called_tuples = [item for tup in self.called_tuples for item in tup]
        full_hand = self.hand + flattened_called_tuples
        full_hand.sort(key=lambda x: x.classId)
        first_suit = full_hand[0].tile_suit
        for tile in full_hand:
            if tile.tile_suit != first_suit:
                return False
        
        return True

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
        # Must be all pong/kong hand    
        if self.all_pong_hand() or self.all_kong_hand():
            # Check all tiles are winds or dragons
            for t in self.called_tuples:
                if t[0].classId < 28:
                    return False
            return True
        
        return False

    def nine_gates_to_haven(self):
        if not self.no_call():
            return False

    def thirteen_orphans(self):
        if not self.no_call():
            return False
        
        required_classId = {
            1: 0, 
            9: 0, 
            10: 0, 18: 0, 19: 0, 27: 0,
            28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0
        }
        for tile in self.hand:
            if tile.classId in required_classId:
                required_classId[tile.classId] += 1
        # Check all required tiles are present
        for count in required_classId.values():
            if count not in [1, 2]:
                return False
            
        pair_count = 0
        for count in required_classId.values():
            if count == 2:
                pair_count += 1

        return pair_count == 1

    def little_4_winds_hand(self):
        return False

    def great_4_winds_hand(self):
        east_found = False
        south_found = False
        west_found = False
        north_found = False

        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 28:
                    east_found = True
                elif t[0].classId == 29:
                    south_found = True
                elif t[0].classId == 30:
                    west_found = True
                elif t[0].classId == 31:
                    north_found = True

        # Early stop
        if east_found and south_found and west_found and north_found:
            # Check hand is a pair
            if len(self.hand) != 2:
                return False
            if self.hand[0].classId == self.hand[1].classId:
                return True

        # Check hand tiles
        for i in range(2, len(self.hand)):
            if self.hand[i].classId == self.hand[i - 1].classId == self.hand[i - 2].classId:
                if self.hand[i].classId == 28:
                    east_found = True
                elif self.hand[i].classId == 29:
                    south_found = True
                elif self.hand[i].classId == 30:
                    west_found = True
                elif self.hand[i].classId == 31:
                    north_found = True

        return east_found and south_found and west_found and north_found

    def all_kong_hand(self):
        if self.no_call():
            return False
        
        # Must have 4 kongs called
        kong_count = 0
        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'kong':
                kong_count += 1
        if kong_count != 4:
            return False
        
        # Check hand is a pair
        if len(self.hand) != 2:
            return False
        if self.hand[0].classId != self.hand[1].classId:
            return False

        return True

    def four_hidden_pong(self):
        if not self.no_call():
            return False
        
        if self.all_pong_hand():
            return True
        
        return False
    
    def find_next_chow(self, hand):
        next_chow = None
        remaining = hand
        for idx, tile in enumerate(hand):
            second_tile_number = tile.tile_number + 1
            third_tile_number = tile.tile_number + 2
            second_tile = None
            third_tile = None

            for j in range(len(hand)):
                if hand[j].tile_suit == tile.tile_suit:
                    if hand[j].tile_number == second_tile_number:
                        second_tile = hand[j]
                    elif hand[j].tile_number == third_tile_number:
                        third_tile = hand[j]
            
            if second_tile and third_tile:
                next_chow = (tile, second_tile, third_tile)
                remaining = [t for t in hand if t not in next_chow]
                break
        
        return next_chow, remaining
