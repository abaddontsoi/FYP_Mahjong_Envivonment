import MahjongTiles
from FaanCalculator import FaanCalculator

class PlayerGUI:
    def __init__(self, id = None):
        self.hand = []
        self.game_env = None
        self.id = id
        self.called_tuples = []
        self.round_position = -1

        # Each player's faan calculator
        self.faan_calculator = FaanCalculator()

    def assign_env(self, env):
        self.game_env = env

    def sort_hand(self):
        self.hand.sort(key=lambda x: x.classId)

    def draw_tiles(self, tiles: list[MahjongTiles.MahjongTiles]):
        self.hand += tiles
        self.sort_hand()
        self.faan_calculator.update_hand_and_called_tuples(self.hand, self.called_tuples)

    def get_hand_as_string(self):
        return ' '.join([t.tile_class_info[1] for t in self.hand])
    
    def get_called_tuples_as_string(self):
        tuples_as_string = []
        for tuple in self.called_tuples:
            temp = [tile.tile_class_info[1] for tile in tuple]
            tuples_as_string.append(' '.join(temp))
        return '\n'.join(tuples_as_string)

    def display_hand(self):
        print(self.get_hand_as_string())
        print(self.get_called_tuples_as_string())

    def check_tuple_type(self, tuple: tuple[MahjongTiles.MahjongTiles]):
        return self.faan_calculator.check_tuple_type(tuple)

    def safe_get_option(self, options: list, prompt: str):
        while True:
            try:
                idx = int(input(prompt))
                if idx >= len(options):
                    raise IndexError("Index out of range.")
                return options.pop(idx)
            except ValueError:
                print("Invalid input, try again.")
            except IndexError:
                print("Index out of range, try again.")

    def discard(self):
        ...

    def clear_hand(self):
        self.hand = []
        self.called_tuples = []
        self.faan_calculator.update_hand_and_called_tuples(self.hand, self.called_tuples)

    def find_first_by_number(self, tile_number: int, suit, provided_list: list[MahjongTiles.MahjongTiles] = None):
        if not provided_list:
            for i in range(len(self.hand)):
                if self.hand[i].tile_number == tile_number:
                    if self.hand[i].tile_suit == suit:
                        return i
        else:
            for i in range(len(provided_list)):
                if provided_list[i].tile_number == tile_number:
                    if provided_list[i].tile_suit == suit:
                        return i
        return -1
    
    def find_first_by_classId(self, classId: int, provided_list: list[MahjongTiles.MahjongTiles] = None):
        if not provided_list:
            for i in range(len(self.hand)):
                if self.hand[i].classId == classId:
                    return i
        else:
            for i in range(len(provided_list)):
                if provided_list[i].classId == classId:
                    return i
        return -1

    def simplify_hand(self):
        # Return a list where each tile is unique on classId
        unique_tiles = []
        unique_tiles.append(self.hand[0])
        for i in range(1, len(self.hand)):
            if self.hand[i].classId != self.hand[i - 1].classId:
                unique_tiles.append(self.hand[i])
        return unique_tiles
        
    def check_possible_calls(self, call_tile: MahjongTiles.MahjongTiles, chow_allowed = False):
        actions = []
        # Put those selected mahjong tiles to self.called_tuples, responses are: 
        # 'win'
        if self.check_win(call_tile):
            actions.append('win')

        # 'kong'
        call_tile_id = call_tile.classId
        count = 0
        for t in self.hand:
            if t.classId == call_tile_id:
                count += 1
        if count == 3:
            actions.append('kong')
        
        # 'pong'
        count = 0
        for t in self.hand:
            if t.classId == call_tile_id:
                count += 1
        if count >= 2:
            actions.append('pong')
        
        # 'chow'
        if call_tile.tile_suit != 'z' and chow_allowed: # 'z' suit not allow to 'chow'
            same_suit_tiles_idx = []
            for i in range(len(self.hand)):
                if self.hand[i].tile_suit != call_tile.tile_suit:
                    continue
                else:
                    target_idx = self.find_first_by_number(self.hand[i].tile_number, call_tile.tile_suit)
                    if target_idx > -1:
                        same_suit_tiles_idx.append(target_idx)
            
            same_suit_tiles_idx = set(same_suit_tiles_idx)
            same_suit_tiles_idx = list(same_suit_tiles_idx)
            same_suit_tiles_idx.sort()

            chow_options = []
            if len(same_suit_tiles_idx) >= 2:
                for i in range(1, len(same_suit_tiles_idx)):
                    chow_valid = self.chow_check([self.hand[same_suit_tiles_idx[i]], self.hand[same_suit_tiles_idx[i - 1]]], call_tile)
                    if chow_valid:
                        chow_options.append(
                            (
                                same_suit_tiles_idx[i],
                                same_suit_tiles_idx[i - 1]
                            )
                        )

            if chow_options:
                actions.append('chow')
        
        return actions

    # length must be multiple of 3, max 12
    def count_tuples(self, remaining: list[MahjongTiles.MahjongTiles]):
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

    def check_13_orphans(self, hand: list[MahjongTiles.MahjongTiles]):
        required_classId = [1, 9, 10, 18, 19, 27, 28, 29, 30, 31, 32, 33, 34]
        for classId in required_classId:
            if self.find_first_by_classId(classId) == -1:
                return False
        
        proposed_eye = []
        for idx in range(1, len(hand)):
            if hand[idx].classId == hand[idx - 1].classId:
                proposed_eye.append(
                    (hand[idx - 1], hand[idx])
                )
        if len(proposed_eye) == 1:
            return True
        else:
            return False

    def check_win(self, call_tile: MahjongTiles.MahjongTiles = None):
        # Insert to hand
        remaining = self.hand + []
        if call_tile:
            remaining += [call_tile]
        
        remaining.sort(key= lambda x: x.classId)
        
        # Special winning cases
        # 13 Orphans
        if self.check_13_orphans(remaining):
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


        # 1 tile remains
        if required_tuples == 0 and len(self.hand) == 1:
            if call_tile.classId == self.hand[0].classId:
                return True
            
        return False
    
    def check_on_draw_action(self):
        actions = []
        # check self drawn
        if self.check_win():
            actions.append('self_drawn')
        
        # check additional kong
        for tile in self.hand:
            for tuple in self.called_tuples:
                if tuple[0].classId == tile.classId and self.check_tuple_type(tuple) == 'pong':
                    # Possible additional kong exists
                    actions.append('additional_kong')
                    break

        # check hidden kong
        if len(self.hand) >= 4:
            for idx in range(3, len(self.hand)):
                tuple = (self.hand[idx], self.hand[idx - 1], self.hand[idx - 2], self.hand[idx - 3])
                tuple_type = self.check_tuple_type(tuple)
                if tuple_type == 'kong':
                    actions.append('hidden_kong')
                    break
        
        if actions:
            actions.append('pass')
        
        return actions
    
    def self_drawn(self):
        options = ['self drawn', 'pass']
        if self.check_win():
            result = self.safe_get_option(options, f"{options}: ")
            return result == 'self drawn'
        return False
            
    def kong(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        kong_tiles = [t for t in self.hand if t.classId == call_tile_id]
        self.hand = [t for t in self.hand if t.classId != call_tile_id]
        
        kong_tiles.append(call_tile)
        self.called_tuples.append(tuple(kong_tiles))
    
    def additional_kong(self):
        for tile in self.hand:
            for tuple in self.called_tuples:
                if self.check_tuple_type(tuple) == 'pong' and tuple[0].classId == tile.classId:
                    # Possible additional kong exists
                    self.called_tuples.remove(tuple)
                    new_kong = (tuple[0], tuple[1], tuple[2], tile)
                    self.called_tuples.append(new_kong)
                    self.hand.remove(tile)
                    return


    def hidden_kong(self):
        if len(self.hand) >= 4:
            print("Checking hidden kong...")
            for idx in range(3, len(self.hand)):
                tuple = (self.hand[idx], self.hand[idx - 1], self.hand[idx - 2], self.hand[idx - 3])
                tuple_type = self.check_tuple_type(tuple)
                if tuple_type == 'kong':
                    self.called_tuples.append(tuple)
                    for tile in reversed(tuple):
                        self.hand.remove(tile)
                    break

    def pong(self, call_tile: MahjongTiles.MahjongTiles):
        call_tile_id = call_tile.classId
        pong_tiles = [t for t in self.hand if t.classId == call_tile_id]
        self.hand = [t for t in self.hand if t.classId != call_tile_id]
        # If pong_tiles has more than 2 tiles (kong case)
        # Put 1 back to hand
        while len(pong_tiles) > 2:
            self.hand.append(pong_tiles.pop())

        pong_tiles.append(call_tile)
        self.called_tuples.append(tuple(pong_tiles))

    def chow_check(self, chow_tiles: list[MahjongTiles.MahjongTiles], call_tile: MahjongTiles.MahjongTiles):
        temp = chow_tiles + [call_tile]
        temp.sort(key=lambda x: x.tile_number)
        if len(temp) != 3:
            return False
        if temp[1].tile_number == temp[0].tile_number + 1 and temp[2].tile_number == temp[0].tile_number + 2:
            return True
        return False

    # Return all possible chow options
    def get_chow_options(self, call_tile: MahjongTiles.MahjongTiles):
        chow_options = []
        # For each 2 consecutive tiles in hand, check the tuple (t[idx - 1], t[idx]) with call_tile is a chow tuple
        if len(self.hand) < 2:
            return chow_options
        
        simplyfied_hand = self.simplify_hand()
        for i in range(1, len(simplyfied_hand)):
            if simplyfied_hand[i].tile_suit != call_tile.tile_suit:
                continue
            else:
                tuple_type = self.check_tuple_type(sorted([simplyfied_hand[i - 1], simplyfied_hand[i], call_tile], key=lambda x: x.classId))
                if tuple_type == 'chow':
                    chow_options.append(
                        (
                            simplyfied_hand[i - 1],
                            simplyfied_hand[i]
                        )
                    )
                # Also check non-consecutive tiles
                tuple_type = self.check_tuple_type(sorted([simplyfied_hand[i - 2], simplyfied_hand[i], call_tile], key=lambda x: x.classId))
                if i - 2 >= 0 and tuple_type == 'chow':
                    chow_options.append(
                        (
                            simplyfied_hand[i - 2],
                            simplyfied_hand[i]
                        )
                    )
        return chow_options
    
    def chow(self, call_tile: MahjongTiles.MahjongTiles, chosen_option: tuple):
        chow_tiles = list(chosen_option)
        self.hand = [t for t in self.hand if t not in chosen_option]
        chow_tiles.append(call_tile)
        self.called_tuples.append(tuple(chow_tiles))


    def align_tile_sprites(self):   
        self.sort_hand()
        # set each tile's x-position based on index
        for idx, tile in enumerate(self.hand):
            tile.rect.topleft = (50 + idx * tile.rect.width, 1000)

    def align_called_tuple_sprites(self):
        # Set called tuples' positions
        # Flatted called tuples
        flatted_called_tuples = []
        for tuple in self.called_tuples:
            for tile in tuple:
                flatted_called_tuples.append(tile)
        
        for idx, tile in enumerate(flatted_called_tuples):
            tile.rect.topleft = (50 + (14 + idx) * tile.rect.width, 1000)