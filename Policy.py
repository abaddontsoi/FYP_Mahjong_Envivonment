from MahjongTiles import MahjongTiles

class Policy:
    def __init__(self):
        self.round_position = None
        self.round_wind = None

    def updat_board_state(self, 
                          discard_pool: list[MahjongTiles], 
                          hand: list[MahjongTiles], 
                          other_player_call_tuples: list[list[tuple[MahjongTiles, ...]]]):
        self.discard_pool = discard_pool
        self.hand = hand
        self.other_player_call_tuples = other_player_call_tuples # Follows the order: next player, opposite player, previous player

    def convert_board_to_vector(self):
        # Existing tiles
        existing = [
            [0]*9, # m
            [0]*9, # p
            [0]*9, # s
            [0]*7, # z
        ]
        for tile in self.discard_pool:
            if tile.tile_suit == 'm':
                existing[0][tile.tile_number-1] += 1
            elif tile.tile_suit == 'p':
                existing[1][tile.tile_number-1] += 1
            elif tile.tile_suit == 's':
                existing[2][tile.tile_number-1] += 1
            elif tile.tile_suit == 'z':
                existing[3][tile.tile_number-1] += 1

        return existing

    def convert_hand_to_vector(self, hand = None):
        if hand is None:
            hand = self.hand
        suits = ['m', 'p', 's', 'z']
        # Hand tiles
        hand_existing = [
            [0]*9, # m
            [0]*9, # p
            [0]*9, # s
            [0]*7, # z
        ]
        for tile in hand:
            if tile.tile_suit == 'm':
                hand_existing[0][tile.tile_number-1] += 1
            elif tile.tile_suit == 'p':
                hand_existing[1][tile.tile_number-1] += 1
            elif tile.tile_suit == 's':
                hand_existing[2][tile.tile_number-1] += 1
            elif tile.tile_suit == 'z':
                hand_existing[3][tile.tile_number-1] += 1
        
        return hand_existing

    def get_dominating_suit(self, hand = None):
        suits = ['m', 'p', 's', 'z']
        hand_existing = self.convert_hand_to_vector(hand)

        # Find dominating number suit in hand
        dominating_number_suit_counts = [sum(hand_existing[i]) for i in range(3)] # Only consider m, p and s
        dominating_suit = suits[dominating_number_suit_counts.index(max(dominating_number_suit_counts))]
        
        return dominating_suit

    def get_pair_count(self, hand = None):
        hand_existing = self.convert_hand_to_vector(hand)
        # Count pairs in hand
        pair_count = 0
        for i in range(4):
            for j in hand_existing[i]:
                if j >= 2:
                    pair_count += 1
        return pair_count

    def get_pong_kong_count(self, hand = None):
        hand_existing = self.convert_hand_to_vector(hand)
        # Count for existing kong and pong sets in hand
        pong_kong_count = 0
        for i in range(4):
            for j in hand_existing[i]:
                if j >= 3:
                    pong_kong_count += 1 # Kong also counts as a pair for simplicity
        return pong_kong_count

    def get_consec_2_count(self, hand = None):
        hand_existing = self.convert_hand_to_vector(hand)
        # Count consecutive 2 tiles set in hand
        consec_2_count = 0
        for i in range(3): # Only consider m, p and s
            for j in range(8):
                if hand_existing[i][j] >= 1 and hand_existing[i][j+1] >= 1:
                    consec_2_count += 1

        return consec_2_count

    def get_alternating_consec_2_count(self, hand = None):
        hand_existing = self.convert_hand_to_vector(hand)
        # Count alternating consecutive 2 tiles set in hand (e.g. 1 and 3, 2 and 4, etc.)
        alternating_consec_2_count = 0
        for i in range(3): # Only consider m, p and s
            for j in range(7):
                if hand_existing[i][j] >= 1 and hand_existing[i][j+2] >= 1:
                    alternating_consec_2_count += 1

        return alternating_consec_2_count

    def get_deck_remaining(self, hand = None):
        remaining = [
            [4]*9, # m
            [4]*9, # p
            [4]*9, # s
            [4]*7, # z
        ]
        existing = self.convert_board_to_vector()
        for i in range(4):
            for j in range(len(existing[i])):
                remaining[i][j] -= existing[i][j]
        hand_existing = self.convert_hand_to_vector(hand)
        for i in range(4):
            for j in range(len(hand_existing[i])):
                remaining[i][j] -= hand_existing[i][j]
        
        return remaining

    def extract_features(self, hand = None):
        existing = self.convert_board_to_vector()
        dominating_suit = self.get_dominating_suit(hand)
        hand_existing = self.convert_hand_to_vector(hand)
        pair_count = self.get_pair_count(hand)
        consec_2_count = self.get_consec_2_count(hand)
        alternating_consec_2_count = self.get_alternating_consec_2_count(hand)
        pong_kong_count = self.get_pong_kong_count(hand)

        return existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count
    
    def decide_kong(self, call_tile: MahjongTiles) -> bool:

        return False
    
    def decide_pong(self, call_tile: MahjongTiles) -> bool:
        return False
    
    def decide_chow(self, call_tile: MahjongTiles) -> bool:
        return False
    
    def decide_win(self, call_tile: MahjongTiles) -> bool:
        return True
