class Policy:
    def __init__(self):
        self.round_position = None
        self.round_wind = None

    def decide_kong(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_pong(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_chow(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
    
    def decide_win(self, discard_pool, hand, called_tuples, call_tile) -> bool:
        return False
