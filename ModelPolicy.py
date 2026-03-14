from Policy import Policy
from MahjongTiles import MahjongTiles
import torch
import torch.nn as nn
import os 
from Encoder import encoder

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

    def load_models(self):
        MODEL_ROOT = "models"
        if os.path.exists(os.path.join(MODEL_ROOT, "discard_model.pth")):
            self.discard_model = DiscardMLP(input_dim=460)  # Adjust input_dim as needed
            self.discard_model.load_state_dict(torch.load(os.path.join(MODEL_ROOT, "discard_model.pth"), weights_only=True))
            self.discard_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "pong_model.pth")):
            self.pong_model = PongMLP(input_dim=460)  # Adjust input_dim as needed
            self.pong_model.load_state_dict(torch.load(os.path.join(MODEL_ROOT, "pong_model.pth"), weights_only=True))
            self.pong_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "kong_model.pth")):
            self.kong_model = KongMLP(input_dim=460)
            self.kong_model.load_state_dict(torch.load(os.path.join(MODEL_ROOT, 'kong_model.pth'), weights_only=True))
            self.kong_model.eval()
        
        if os.path.exists(os.path.join(MODEL_ROOT, "chow_model.pth")):
            self.chow_model = ChowMLP(input_dim=460)
            self.chow_model.load_state_dict(torch.load(os.path.join(MODEL_ROOT, 'chow_model.pth'), weights_only=True))
            self.chow_model.eval()

    def decide_discard(self):
        if not self.discard_model:
            return super().decide_discard()
        
    def decide_kong(self, call_tile: MahjongTiles) -> bool:
        if not self.kong_model:
            return super().decide_kong(call_tile)

    def decide_chow(self, call_tile: MahjongTiles) -> bool:
        return super().decide_chow(call_tile)
        
    def decide_pong(self, call_tile: MahjongTiles) -> bool:
        if not self.pong_model:
            return super().decide_pong(call_tile)
        