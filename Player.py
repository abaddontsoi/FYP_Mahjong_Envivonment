import MahjongTiles
import MahjongEnv

class Player:
    def __init__(self, env: MahjongEnv, id = None):
        self.hand = []
        self.game_env = env
        self.id = id
        self.called_tuples = []
        self.round_position = -1
        self.current_discard_pool = []
        self.current_discard_buffer = None

    def assign_env(self, env: MahjongEnv):
        self.game_env(env)

    def draw_tiles(self, tiles: list[MahjongTiles.MahjongTiles]):
        self.hand += tiles
        self.hand.sort(key=lambda x: x.classId)

    def display_hand(self):
        print(self.get_hand_as_string())
        print(self.get_called_tuples_as_string())

    def display_current_discards(self):
        discard_pool = self.game_env.get_pool_and_buffer()
        
        if not discard_pool:
            return 
        
        print("="*20 + "Discard Pool" + "="*20)
        counter = 10
        for tile in discard_pool:
            print(tile.tile_class_info[1], end=' ')
            counter -= 1
            if counter == 0:
                print()
                counter = 10
        print()
        print("=" * 50)

    def get_hand_as_string(self):
        return ' '.join([t.tile_class_info[1] for t in self.hand])
    
    def get_called_tuples_as_string(self):
        tuples_as_string = []
        for tuple in self.called_tuples:
            temp = [tile.tile_class_info[1] for tile in tuple]
            tuples_as_string.append(' '.join(temp))
        return '\n'.join(tuples_as_string)

    def safe_get_option(self, options: list, prompt: str):
        while True:
            try:
                idx = int(input(prompt))
                if not 0 <= idx < len(options):
                    raise IndexError("Index out of range.")
                return options.pop(idx)
            except ValueError:
                print("Invalid input, try again.")
            except IndexError:
                print("Index out of range, try again.")

    def discard(self):
        self.display_current_discards()
        self.display_hand()
        return self.safe_get_option(self.hand, "Input index to discard: ")
    
    def receive_discarded(self, discard_pool: list[MahjongTiles.MahjongTiles], discard_buffer: MahjongTiles.MahjongTiles):
        self.current_discard_pool = discard_pool
        self.current_discard_buffer = discard_buffer

    def clear_current_discard_pool(self):
        self.current_discard_buffer = None
        self.current_discard_pool = []

    def clear_hand(self):
        self.hand = []
        self.called_tuples = []
    
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
        if call_tile.tile_suit != 'z': # 'z' suit not allow to 'chow'
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
                available_actions.append('chow')
            
        # Add a 'pass' option
        # Choose action
        if available_actions:
            available_actions.append('pass')
            self.display_current_discards()
            self.display_hand()
            return self.safe_get_option(available_actions, f"{str(available_actions)}: ")
        
        return False
    
    def find_first_by_number(self, tile_number: int, suit):
        for i in range(len(self.hand)):
            if self.hand[i].tile_number == tile_number:
                if self.hand[i].tile_suit == suit:
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
    
    def additional_kong(self):
        ...
    
    def hidden_kong(self):
        ...
    
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

    def chow(self, call_tile: MahjongTiles.MahjongTiles):
        same_suit_tiles = set([self.find_first_by_number(t.tile_number, call_tile.tile_suit) for t in self.hand 
                               if t.tile_suit == call_tile.tile_suit and call_tile.tile_suit != 'z'])
        same_suit_tiles = list(same_suit_tiles)
        same_suit_tiles.sort()

        chow_options = []
        if len(same_suit_tiles) >= 2:
            for i in range(1, len(same_suit_tiles)):
                chow_valid = self.chow_check([self.hand[same_suit_tiles[i]], self.hand[same_suit_tiles[i - 1]]], call_tile)
                if chow_valid:
                    chow_options.append(
                        (
                            same_suit_tiles[i],
                            same_suit_tiles[i - 1]
                        )
                    )
        chow_selection = 0
        if len(chow_options) > 1:
            for idx, option in enumerate(chow_options):
                print(f"[{idx}] {str(self.hand[option[1]])} {str(self.hand[option[0]])}")
            chow_selection = int(input(f"Choose chow combination: "))
        else:
            chow_selection = 0
        chow_tiles = [t for idx, t in enumerate(self.hand) if idx in chow_options[chow_selection]]
        self.hand = [t for idx, t in enumerate(self.hand) if idx not in chow_options[chow_selection]]
        chow_tiles.append(call_tile)
        chow_tiles.sort(key= lambda x: x.classId)
        self.called_tuples.append(tuple(chow_tiles))