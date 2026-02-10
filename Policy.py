import random
from MahjongTiles import MahjongTiles
from FaanCalculator import check_tuple_type

class Policy:
    def __init__(self):
        self.round_position = None
        self.round_wind = None
        self.discard_pool = []
        self.hand = []
        self.self_call_tuples = []
        self.other_player_call_tuples = [] # Follows the order: next player, opposite player, previous player

    def update_board_state(self, 
                          discard_pool: list[MahjongTiles], 
                          hand: list[MahjongTiles], 
                          self_call_tuples: list[tuple[MahjongTiles, ...]],
                          other_player_call_tuples: list[list[tuple[MahjongTiles, ...]]]):
        self.discard_pool = discard_pool
        self.hand = hand
        self.self_call_tuples = self_call_tuples
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
        if self.self_call_tuples:
            first_call_tuple = self.self_call_tuples[0]
            if first_call_tuple[0].tile_suit in ['m', 'p', 's']:
                # Assuming the first call tuple is the most recent one, and the first tile in the tuple is the called tile
                return first_call_tuple[0].tile_suit 
        
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

    def get_max_remaining(self, hand = None):
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
    
    def decide_discard(self):
        suits = ['m', 'p', 's', 'z']
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_2_count, pong_kong_count = self.extract_features()
        hand_vector = self.convert_hand_to_vector()
        max_remaining = self.get_max_remaining()
        converted_max_remaining = [('m', max_remaining[0]), ('p', max_remaining[1]), ('s', max_remaining[2]), ('z', max_remaining[3])]
        converted_max_remaining.sort(key = lambda x: sum(x[1]), reverse=True) # Prioritize suits with more remaining tiles

        discard_index = random.randint(0, len(self.hand) - 1)
        available_discard_indices = []
        
        for idx, tile in enumerate(self.hand):
            if tile.tile_suit != dominating_suit:
                available_discard_indices.append(idx)
        
        if available_discard_indices:
            discard_index = random.choice(available_discard_indices)

        return discard_index

    # When the following decision functions are called, that means the player is available to call for actions

    def decide_kong(self, call_tile: MahjongTiles) -> bool:

        return False
    
    def decide_pong(self, call_tile: MahjongTiles) -> bool:
        suits = ['m', 'p', 's', 'z']
        call_tile_suit = call_tile.tile_suit
        call_tile_number = call_tile.tile_number
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_2_count, pong_kong_count = self.extract_features()
        
        # If the called tuple is not pong/kong, only pong when the suit is same
        if call_tile_suit != 'z':
            first_call_tuple = self.self_call_tuples[0] if self.self_call_tuples else None
            if first_call_tuple:
                first_call_suit = first_call_tuple[0].tile_suit
                tuple_type = check_tuple_type(first_call_tuple)
                # 'pong' and 'chow' in different suits is hard to achieve clean hand or other high faan combinations, hence should not pong
                if tuple_type == 'chow' and call_tile_suit != first_call_suit:
                    return False

        # If pair_count >= 5 - len(self.self_call_tuples), achieving all_pong_hand is more valuable than chow hand, hence should not chow
        if pair_count >= 5 - len(self.self_call_tuples) and call_tile_suit == dominating_suit:
            return True
        new_consec_2_count = 0
        new_alternating_2_count = 0
        
        # Remove 2 tiles from hand that is as same as the call_tile
        same_tile_in_hand = []
        for tile in self.hand:
            if tile.classId == call_tile.classId:
                same_tile_in_hand.append(tile)
        new_hand = [tile for tile in self.hand if tile.classId != call_tile.classId]
        
        if len(same_tile_in_hand) > 2:
            new_hand.append(same_tile_in_hand[0])
        
        new_consec_2_count = self.get_consec_2_count(new_hand)
        new_alternating_2_count = self.get_alternating_consec_2_count(new_hand)
        
        if new_alternating_2_count > alternating_2_count:
            return False
        
        return True
    
    def decide_chow_helper(self, suit, call_tile_number):
        original_consec_2_count = self.get_consec_2_count()
        original_alternating_consec_2_count = self.get_alternating_consec_2_count()
        should_chow = False, None
        upper_consec_2 = [None, None]
        lower_consec_2 = [None, None]
        alter = [None, None]
        if call_tile_number in range(3, 8):
            upper_consec_2 = [call_tile_number + 1, call_tile_number + 2]
            lower_consec_2 = [call_tile_number - 1, call_tile_number - 2]
            alter = [call_tile_number - 1, call_tile_number + 1]
        elif call_tile_number == 2:
            upper_consec_2 = [call_tile_number + 1, call_tile_number + 2]
            alter = [call_tile_number - 1, call_tile_number + 1]
        elif call_tile_number == 8:
            lower_consec_2 = [call_tile_number - 1, call_tile_number - 2]
            alter = [call_tile_number - 1, call_tile_number + 1]
        elif call_tile_number == 1:
            upper_consec_2 = [call_tile_number + 1, call_tile_number + 2]
        elif call_tile_number == 9:
            lower_consec_2 = [call_tile_number - 1, call_tile_number - 2]

        possible_hand_after_chow = []
        if upper_consec_2 != [None, None]:
            new_hand_after_chow = [tile for tile in self.hand if not (tile.tile_suit == suit and tile.tile_number in upper_consec_2)]
            possible_hand_after_chow.append((new_hand_after_chow, upper_consec_2))
        if lower_consec_2 != [None, None]:
            new_hand_after_chow = [tile for tile in self.hand if not (tile.tile_suit == suit and tile.tile_number in lower_consec_2)]
            possible_hand_after_chow.append((new_hand_after_chow, lower_consec_2))
        if alter != [None, None]:
            new_hand_after_chow = [tile for tile in self.hand if not (tile.tile_suit == suit and tile.tile_number in alter)]
            possible_hand_after_chow.append((new_hand_after_chow, alter))
        
        statisctics_after_chow = []
        for possible_hand, chow_option in possible_hand_after_chow:
            new_alternating_2_count = self.get_alternating_consec_2_count(possible_hand)
            new_consec_2_count = self.get_consec_2_count(possible_hand)
            statisctics_after_chow.append((chow_option, new_consec_2_count, new_alternating_2_count))

        statisctics_after_chow.sort(key = lambda x: (x[1], x[2]), reverse=True) # Prioritize chow options that lead to more consec_2 and alternating_consec_2 in hand

        best_chow_option = statisctics_after_chow[0]

        if best_chow_option[2] >= original_alternating_consec_2_count:
            should_chow = False, None
        else:
            should_chow = True, best_chow_option[0]
        
        return should_chow

    def decide_chow(self, call_tile: MahjongTiles) -> bool:
        suits = ['m', 'p', 's', 'z']
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.extract_features()
        
        # If pair_count >= 5 - len(self.self_call_tuples), achieving all_pong_hand/four_hidden_pong is more valuable than chow hand, hence should not chow
        if pair_count >= 5 - len(self.self_call_tuples): 
            return False, None
        
        call_tile_suit = call_tile.tile_suit
        call_tile_number = call_tile.tile_number
        
        if call_tile_suit == 'z': # Cannot chow dragon tiles
            return False, None

        # If chow on a non dominating suit, then the hand is hard to achieve clean_hand
        if dominating_suit != call_tile_suit:
            return False, None
        
        # If chow is not the same suit as the most recent call tuple, hard to achieve clean hand or other high faan combinations, hence should not chow
        last_call_tuple = self.self_call_tuples[-1] if self.self_call_tuples else None
        if last_call_tuple:
            last_call_suit = last_call_tuple[0].tile_suit
            if call_tile_suit != last_call_suit:
                return False, None

        return self.decide_chow_helper(call_tile_suit, call_tile_number)
    
    def decide_win(self, call_tile: MahjongTiles) -> bool:
        return True
