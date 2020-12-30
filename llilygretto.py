import numpy as np

count_player = 2

# INIT
def get_names_of_player(number_of_names):
    names = []
    for x in range(number_of_names):
        names.append(input('Name: '))
    return names

# PRINT
def print_game(game):
    print('\n\tSPIELERGEBNIS:')
    for g in range(len(game)):
        print('\t ', game[g])

# GAME-PLAY
def get_player_point(player):
    print('\t', player)
    points = 1#int(input())
    return points

def get_round_points(player_names):
    minus_points = []
    plus_points = []
    print('\tEINGABE MINUS-PUNKTE:')
    for p in player_names:
        minus_points.append(get_player_point(p))
    print('\tEINGABE PLUS-PUNKTE:')
    for p in player_names:
        plus_points.append(get_player_point(p))
    return minus_points, plus_points

def main():
    # Init
    player_names = ['ich', 'du']#get_names_of_player(count_player)
    game = []
    # Game
    round_count = 1
    while 1:
        print('\nRUNDE: ', round_count)
        minus_points, plus_points = get_round_points(player_names)
        round_points = [sum(x) for x in zip(minus_points, plus_points)]
        if round_count == 1:
            game.append({'game_round': 1, 'game_points': round_points, 'round_points': round_points, 'minus_points': minus_points, 'plus_points': plus_points})
        else:
            game_points = [sum(x) for x in zip(game[round_count-2]['game_points'], round_points)]
            game.append({'game_round': round_count, 'game_points': game_points, 'round_points': round_points, 'minus_points': minus_points, 'plus_points': plus_points})
        print_game(game)
        if input("\n\tNächste Runde (0/1)?")== '0':
            break
        else:
            round_count += 1

    print('\n\n\t GAME')

    for g in range(len(game)):
        print(game[g]['game_round'])
        for p in game[g]['minus_points']:
            print(p)

if __name__ == "__main__":
    main()