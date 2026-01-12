import MahjongEnv
from BotPlayer import BotPlayer
from Player import Player
def main():
    env = MahjongEnv.MahjongEnv(real_player=True)
    # env.view_deck()
    env.add_players([BotPlayer(env, i) for i in range(3)] + [Player(env, 3)])
    env.start_game()

if __name__ == '__main__':
    main()