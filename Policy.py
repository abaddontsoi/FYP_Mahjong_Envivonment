class Policy:
    def __init__(self):
        self.round_position = None
        self.round_wind = None

    def extract_features(self, discard_pool, hand, called_tuples, call_tile):
        # Existing tiles
        m_existing = [0]*9
        p_existing = [0]*9
        s_existing = [0]*9
        z_existing = [0]*7
        pass

    def decide_kong(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_pong(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_chow(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_win(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
