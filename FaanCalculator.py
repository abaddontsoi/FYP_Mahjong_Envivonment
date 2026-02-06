from MahjongTiles import MahjongTiles

def faan_to_score(faan_count: int, self_drawn: bool):
    # Set to maximum 10 faan
    faan_count = min(faan_count, 10)
    # (win_score, self_drawn_score)
    score_table = [(16, 24), (32, 48), (64, 96), (128, 192)]
    for i in range(4, 11):
        if i % 2 == 0:
            score_table.append((score_table[i-1][0]*1.5, score_table[i-1][1]*1.5))
        else:
            score_table.append((score_table[i-2][0]*2, score_table[i-2][1]*2))

    if self_drawn:
        return score_table[faan_count - 1][1]
    
    return score_table[faan_count - 1][0]

class FaanCalculator:
    def __init__(self, round = 0, position = 0):
        self.FaanList = {
            'self_drawn': (1, self.self_drawn),
            'white': (1, self.white),
            'no_call': (1, self.no_call),
            'red': (1, self.red),
            'green': (1, self.green),
            'round_wind': (1, self.round_wind),
            'round_position': (1, self.round_position),
            'mixed_orphans': (1, self.mixed_orphans),
            'all_chow_hand': (1, self.all_chow_hand),
            'robbing_additional_kong': (1, self.robbing_additional_kong),
            'self_drawn_on_last_tile': (1, self.self_drawn_on_last_tile),
            'self_drawn_after_kong': (1, self.self_drawn_after_kong),
            'all_pong_hand': (3, self.all_pong_hand),
            'clean_hand': (3, self.clean_hand),
            'little_dragon_hand': (5, self.little_dragon_hand),
            'pure_suit': (7, self.pure_suit),
            'great_dragon_hand': (10, self.great_dragon_hand),
            'self_drawn_after_2kong': (10, self.self_drawn_after_2kong),
            'pure_orphans_hand': (10, self.pure_orphans_hand),
            'all_winds_and_dragons': (10, self.all_winds_and_dragons), 
            # 9子連環
            '9_gates_to_haven': (10, self.nine_gates_to_haven), 
            '13_orphans': (10, self.thirteen_orphans),
            'little_4_winds_hand': (10, self.little_4_winds_hand),
            'great_4_winds_hand': (10, self.great_4_winds_hand),
            'all_kong_hand': (10, self.all_kong_hand),
            'four_hidden_pong': (10, self.four_hidden_pong),
            'havenly_hand': (10, None),
            'earthly_hand': (10, None),
        }
        self.hand = []
        self.called_tuples = []
        self.round = round
        self.position = position
        self.self_drawn_flag = False
        self.consecutive_kong_count = 0
        self.robbing_additional_kong_flag = False
        self.self_drawn_on_last_tile_flag = False
    
    def update_hand_and_called_tuples(self, hand, called_tuples):
        self.hand = hand
        self.called_tuples = called_tuples
    
    def check_tuple_type(self, tuple: tuple[MahjongTiles]):
        # Convert to list and sort
        call_tuple = sorted(list(tuple), key=lambda x: x.classId)
        if len(call_tuple) == 4:
            if call_tuple[0].classId == call_tuple[1].classId == call_tuple[2].classId == call_tuple[3].classId:
                return 'kong'
        if len(call_tuple) == 3:
            if call_tuple[0].classId == call_tuple[1].classId == call_tuple[2].classId:
                return 'pong'
            if call_tuple[2].tile_number == call_tuple[1].tile_number + 1 and call_tuple[1].tile_number == call_tuple[0].tile_number + 1:
                if call_tuple[0].tile_suit == call_tuple[1].tile_suit == call_tuple[2].tile_suit:
                    return 'chow'
        
        return None

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
        return self.self_drawn_flag
    
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
        return self.robbing_additional_kong_flag 
    
    def self_drawn_on_last_tile(self):
        return self.self_drawn_on_last_tile_flag

    def self_drawn_after_kong(self):
        return self.consecutive_kong_count == 1 and self.self_drawn_flag

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
        wind_or_dragon_found = False
        for tile in flatten_and_combined:
            if tile.tile_suit != first_suit and tile.tile_suit != 'z':
                return False
            if tile.tile_suit == 'z':
                wind_or_dragon_found = True
        
        return wind_or_dragon_found

    def little_dragon_hand(self):
        white = None
        green = None
        red = None

        # Check for called tuples first
        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'pong' or self.check_tuple_type(t) == 'kong':
                if t[0].classId == 32:
                    white = 'pong'
                elif t[0].classId == 33:
                    green = 'pong'
                elif t[0].classId == 34:
                    red = 'pong'

        # Check hand tiles
        if len(self.hand) == 2:
            if self.hand[0].classId == self.hand[1].classId:
                if self.hand[0].classId == 32:
                    white = 'pair'
                elif self.hand[0].classId == 33:
                    green = 'pair'
                elif self.hand[0].classId == 34:
                    red = 'pair'
        else:
            white_count = self.count_by_classId(32)
            green_count = self.count_by_classId(33)
            red_count = self.count_by_classId(34)
            if white_count == 2:
                white = 'pair'
            if green_count == 2:
                green = 'pair'
            if red_count == 2:
                red = 'pair'
            if white_count >=3:
                white = 'pong'
            if green_count >=3:
                green = 'pong'
            if red_count >=3:
                red = 'pong'

        # Greate dragon hand case, return False
        if white == 'pong' and green == 'pong' and red == 'pong':
            return False
        
        if any([
            white == 'pong' and green == 'pong' and red == 'pair',
            white == 'pong' and green == 'pair' and red == 'pong',
            white == 'pair' and green == 'pong' and red == 'pong'
        ]):
            return True

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
        kong_count = 0
        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'kong':
                kong_count += 1
        if kong_count < 2:
            return False
        
        return self.consecutive_kong_count >= 2 and self.self_drawn_flag
    
    def pure_orphans_hand(self):
        # Valid pong class
        valid_pong_classes = [1, 9, 10, 18, 19, 27]

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

    def all_winds_and_dragons(self):
        # If classId < 28, return False
        for t in self.called_tuples:
            if t[0].classId < 28:
                return False
        for t in self.hand:
            if t.classId < 28:
                return False
        
        # Must be all pong/kong hand
        if not self.all_pong_hand():
            return False

        return True

    def nine_gates_to_haven(self):
        # Must have no call
        if not self.no_call():
            return False
        
        # Must be pure suit
        if not self.pure_suit():
            return False
        
        required_tile_number = {
            1: 3, 
            2: 1, 
            3: 1, 
            4: 1, 
            5: 1,
            6: 1, 
            7: 1, 
            8: 1, 
            9: 3
        }
        for tile in self.hand:
            if tile.tile_number in required_tile_number:
                required_tile_number[tile.tile_number] -= 1
            else:
                return False

        for count in required_tile_number.values():
            if count > 0:
                return False

        if any(count < 0 for count in required_tile_number.values()):
            return True

        return False

    def thirteen_orphans(self):
        if not self.no_call():
            return False
        
        required_classId = {
            1: 1, 
            9: 1, 
            10: 1, 
            18: 1, 
            19: 1, 
            27: 1,
            28: 1, 
            29: 1, 
            30: 1, 
            31: 1, 
            32: 1, 
            33: 1, 
            34: 1
        }
        for tile in self.hand:
            if tile.classId in required_classId:
                required_classId[tile.classId] -= 1
            else:
                return False

        for count in required_classId.values():
            if count > 0:
                return False

        return True

    def little_4_winds_hand(self):
        east = None
        south = None
        west = None
        north = None

        for t in self.called_tuples:
            if self.check_tuple_type(t) == 'pong':
                if t[0].classId == 28:
                    east = 'pong'
                elif t[0].classId == 29:
                    south = 'pong'
                elif t[0].classId == 30:
                    west = 'pong'
                elif t[0].classId == 31:
                    north = 'pong'
        
        if len(self.hand) == 2:
            if self.hand[0].classId == self.hand[1].classId:
                if self.hand[0].classId == 28:
                    east = 'pair'
                elif self.hand[0].classId == 29:
                    south = 'pair'
                elif self.hand[0].classId == 30:
                    west = 'pair'
                elif self.hand[0].classId == 31:
                    north = 'pair'
        else:
            east_count = self.count_by_classId(28)
            south_count = self.count_by_classId(29)
            west_count = self.count_by_classId(30)
            north_count = self.count_by_classId(31)
            if east_count == 2:
                east = 'pair'
            if south_count == 2:
                south = 'pair'
            if west_count == 2:
                west = 'pair'
            if north_count == 2:
                north = 'pair'
            if east_count >=3:
                east = 'pong'
            if south_count >=3:
                south = 'pong'
            if west_count >=3:
                west = 'pong'
            if north_count >=3:
                north = 'pong'

        # Great 4 winds hand case, return False
        if east == 'pong' and south == 'pong' and west == 'pong' and north == 'pong':
            return False

        if any([
            east == 'pong' and south == 'pong' and west == 'pong' and north == 'pair',
            east == 'pong' and south == 'pong' and west == 'pair' and north == 'pong',
            east == 'pong' and south == 'pair' and west == 'pong' and north == 'pong',
            east == 'pair' and south == 'pong' and west == 'pong' and north == 'pong',
        ]):
            return True

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

    def count_by_classId(self, classId: int):
        count = 0
        for tile in self.hand:
            if tile.classId == classId:
                count += 1
        return count
    
    def check_faan_match(self):
        faan_achieved = []
        self.hand.sort(key=lambda x: x.classId)
        if not self.is_valid_winning_hand():
            return faan_achieved
        
        # Check each faan condition
        for faan_name, (faan_value, check_method) in self.FaanList.items():
            if check_method and check_method():
                faan_achieved.append((faan_name, faan_value))
        
        # Some of the small value faans are removed in final calculation
        removing_faan = []
        for faan in faan_achieved:
            if faan[0] == 'little_dragon_hand':
                removing_faan.extend(['white', 'green', 'red'])
            if any([self.self_drawn_after_kong(), self.self_drawn_on_last_tile(), self.self_drawn_after_2kong()]):
                removing_faan.append('self_drawn')
            if any([self.four_hidden_pong(), self.all_kong_hand()]):
                removing_faan.append('all_pong_hand')
        
        removing_faan = set(removing_faan)
        faan_achieved = [faan for faan in faan_achieved if faan[0] not in removing_faan]

        return faan_achieved