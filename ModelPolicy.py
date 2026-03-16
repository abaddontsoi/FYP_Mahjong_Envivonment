from pyexpat import features

from Policy import Policy
from MahjongTiles import MahjongTiles
import torch
import torch.nn as nn
import os 
from Encoder import encoder
from FaanCalculator import check_tuple_type

class ChowMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2), 
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)  # Single logit output
        )
    
    def forward(self, x):
        return self.net(x).squeeze(-1)  # Remove last dim: (batch, 1) -> (batch,)

class DiscardMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2), 
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 34)  # 34-dim
        )
    
    def forward(self, x):
        return self.net(x)  # Return all 34 logits

class KongMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2), 
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)  # Single logit output
        )
    
    def forward(self, x):
        return self.net(x).squeeze(-1)  # Remove last dim: (batch, 1) -> (batch,)

class PongMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2), 
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)  # Single logit output
        )
    
    def forward(self, x):
        return self.net(x).squeeze(-1)  # Remove last dim: (batch, 1) -> (batch,)

class ModelPolicy(Policy):
    def __init__(self):
        super().__init__()
        self.discard_model = None
        self.pong_model = None
        self.kong_model = None
        self.chow_model = None
        self.load_models()

    def load_models(self):
        MODEL_ROOT = "models"
        if os.path.exists(os.path.join(MODEL_ROOT, "discard_model.pth")):
            self.discard_model = DiscardMLP(input_dim=426) 
            checkpoint = torch.load(os.path.join(MODEL_ROOT, "discard_model.pth"), weights_only=True)
            self.discard_model.load_state_dict(checkpoint['model_state_dict'])
            self.discard_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "pong_model.pth")):
            self.pong_model = PongMLP(input_dim=460)
            checkpoint = torch.load(os.path.join(MODEL_ROOT, "pong_model.pth"), weights_only=True)
            self.pong_model.load_state_dict(checkpoint['model_state_dict'])
            self.pong_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "kong_model.pth")):
            self.kong_model = KongMLP(input_dim=460)
            checkpoint = torch.load(os.path.join(MODEL_ROOT, 'kong_model.pth'), weights_only=True)
            self.kong_model.load_state_dict(checkpoint['model_state_dict'])
            self.kong_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "chow_model.pth")):
            self.chow_model = ChowMLP(input_dim=460)
            checkpoint = torch.load(os.path.join(MODEL_ROOT, 'chow_model.pth'), weights_only=True)
            self.chow_model.load_state_dict(checkpoint['model_state_dict'])
            self.chow_model.eval()

    def convert_to_dict(self):
        state = {}
        state['current_wind'] = self.round_wind
        state['round_position'] = self.round_position
        state['hand'] = [tile.classId for tile in self.hand]
        state['called_tuples'] = [ [tile.classId for tile in tuple] for tuple in self.self_call_tuples ]
        state['discard_pool'] = [tile.classId for tile in self.discard_pool]
        state['next_player_called_tuples'] = [ [tile.classId for tile in tuple] for tuple in self.other_player_call_tuples[0] ]
        state['opposite_player_called_tuples'] = [ [tile.classId for tile in tuple] for tuple in self.other_player_call_tuples[1] ]
        state['previous_player_called_tuples'] = [ [tile.classId for tile in tuple] for tuple in self.other_player_call_tuples[2] ]
        return state

    def decide_discard(self):
        if not self.discard_model:
            print("Discard model not found, using default policy.")
            return super().decide_discard()
        else:
            state_dict = self.convert_to_dict()
            state_dict['action'] = 'discard'
            state_dict['action_tile'] = None
            encoded_features = encoder(state_dict)
            processed_feature = encoded_features[:392] + encoded_features[426:]  # Exclude action tile features
            features_tensor = torch.tensor(processed_feature, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
            with torch.no_grad():
                logits = self.discard_model(features_tensor)
                # Find top 5 candidate tiles for discard
                top_5 = torch.topk(logits, k=5).indices.squeeze(0).tolist()  # Get top 5 indices
                
                # Check by order to see if the tile is in hand
                for idx, tile in enumerate(self.hand):
                    if tile.classId in top_5:
                        return idx  # Return the index of the tile to discard
        # Fallback case
        return super().decide_discard()
        
    def decide_kong(self, call_tile: MahjongTiles) -> bool:
        # Basic rule-based checks before invoking the model
        # Find the first chow
        for call in self.self_call_tuples:
            if check_tuple_type(call) == 'chow' and call[0].tile_suit != call_tile.tile_suit and call_tile.tile_suit != 'z':
                if call_tile.tile_suit != call[0].tile_suit:
                    return False
        
        if not self.kong_model:
            print("Kong model not found, using default policy.")
            return super().decide_kong(call_tile)
        else:
            state_dict = self.convert_to_dict()
            state_dict['action'] = 'kong'
            state_dict['action_tile'] = call_tile.classId
            features = encoder(state_dict)
            features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                logit = self.kong_model(features_tensor)
                return logit.item() > 0.5  # Thresholding at 0.5 

    def decide_chow(self, call_tile: MahjongTiles) -> bool:
        # Basic rule-based checks before invoking the model
        dominating_suit = self.get_dominating_suit()
        call_tile_suit = call_tile.tile_suit
        if call_tile_suit == 'z': # Cannot chow dragon tiles
            return False, None

        # If chow on a non dominating suit, then the hand is hard to achieve clean_hand
        if dominating_suit != call_tile_suit:
            return False, None
        
        # If chow is not the same suit as the selected suit, hard to achieve clean hand or other high faan combinations, hence should not chow
        for calls in self.self_call_tuples:
            if calls[0].tile_suit != 'z' and calls[0].tile_suit != call_tile_suit:
                return False, None
        
        if not self.chow_model:
            print("Chow model not found, using default policy.")
            return super().decide_chow(call_tile)
        else:
            state_dict = self.convert_to_dict()
            state_dict['action'] = 'chow'
            state_dict['action_tile'] = call_tile.classId
            features = encoder(state_dict)
            features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                logit = self.chow_model(features_tensor)
                return logit.item() > 0.5, None

        
    def decide_pong(self, call_tile: MahjongTiles) -> bool:
        # Basic rule-based checks before invoking the model
        # Find the first chow
        for call in self.self_call_tuples:
            if check_tuple_type(call) == 'chow' and call[0].tile_suit != call_tile.tile_suit and call_tile.tile_suit != 'z':
                if call_tile.tile_suit != call[0].tile_suit:
                    return False
                
        if not self.pong_model:
            print("Pong model not found, using default policy.")
            return super().decide_pong(call_tile)
        else:
            state_dict = self.convert_to_dict()
            state_dict['action'] = 'pong'
            state_dict['action_tile'] = call_tile.classId
            features = encoder(state_dict)
            features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                logit = self.pong_model(features_tensor)
                return logit.item() > 0.5  # Thresholding at 0.5