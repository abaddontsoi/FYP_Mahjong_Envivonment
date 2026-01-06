import MahjongEnv

def main():
    env = MahjongEnv.MahjongEnv(real_player=True)
    # env.view_deck()
    env.add_players()
    env.start_game()

if __name__ == '__main__':
    main()