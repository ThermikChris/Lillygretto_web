# INITIALIZATION
#my test change
def get_init_player(count_player):
    player_list = []
    for i in range(count_player):
        player_list.append("Spieler_"+str(i+1))
    return player_list

def get_init_game(player_count):
    game = []
    game.append({'game_round': 1, 'game_points': [0]*player_count, 'round_points': [0]*player_count, 'minus_points': [0]*player_count, 'plus_points': [0]*player_count})
    return game


# NEXT/NEW: ROUND/PLAYER
def next_round(game):
    game.append({'game_round': game[-1]['game_round']+1, 'game_points': [0]*len(game[0]['minus_points']), 'round_points': [0]*len(game[0]['minus_points']), 'minus_points': [0]*len(game[0]['minus_points']), 'plus_points': [0]*len(game[0]['minus_points'])})
    return game

def set_new_player(game_data):
    new_game_data = []
    for i_g in range(len(game_data)):
        g = game_data[i_g]
        game_points = g['game_points'].append(0)
        round_points = g['round_points'].append(0)
        minus_points = g['minus_points'].append(0)
        plus_points = g['plus_points'].append(0)
        new_game_data.append({'game_round': i_g, 'game_points': game_points, 'round_points': round_points, 'minus_points': minus_points, 'plus_points': plus_points})
    return game_data

# GAME-STATE
def calc_game_state(game, count_player):
    new_game_state = []
    # for each round
    for i_g in range(len(game)):
        g = game[i_g]
        minus_points = g['minus_points']
        plus_points = g['plus_points']
        round_points = [x2-x1 for (x1, x2) in zip(minus_points, plus_points)]
        if i_g == 0:
            game_points = round_points
        else:
            game_points = [sum(x) for x in zip(game[i_g-1]['game_points'], round_points)]
        new_game_state.append({'game_round': i_g+1, 'game_points': game_points, 'round_points': round_points, 'minus_points': minus_points, 'plus_points': plus_points})
    return new_game_state
