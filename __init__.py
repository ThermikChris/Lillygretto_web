# nimm das
from flask import Flask, render_template, request, session, redirect, url_for
from backend import get_init_player, get_init_game, next_round, set_new_player, calc_game_state
# from flask_sqlalchemy import SQLAlchemy
import json
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)
app.secret_key = "lillygretto"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
#app.permanent_session_lifetime

# db = SQLAlchemy(app)

# class users(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     game = db.Column(db.String(100))
    
#     def __init__(self, game):
#         self.game = game

@app.route("/")
@app.route("/lillygretto")
def home():
    #print(session)
    #session.clear()
    if 'game_data' not in session:
        print('empty SESSION')
        count_player = 3
        count_rounds = 1
        player = get_init_player(count_player)
        game_data = get_init_game(count_player)
    else:
        player = session['player']
        game_data = session['game_data']
        count_player = len(player)
        count_rounds = len(game_data)

    game_data = calc_game_state(game_data, count_player)
    session['player'] = player
    session['game_data'] = game_data
    graphJSON = plot_game_state(game_data, player)
    return render_template(
        "page.html", 
        count_cols = count_player+1, 
        count_rows = count_rounds*4, 
        player_heading=player, 
        data=game_data,
        graphJSON=graphJSON
    )

@app.route("/game_change", methods=["GET", "POST"])
def game_change():
    #print(session)
    if 'game_data' in session:
        player = session['player']
        game_data = session['game_data']
        count_player = len(player)
        count_rounds = len(game_data)
        if request.args.get('btn_game') == 'Reset Session':
            print("CLEAR SESSION")
            session.clear()
            return redirect(url_for('home'))
    else:
        return "<h1>ERROR: session not loaded</h1>"

    if request.method == "GET":
        # NEW PLAYER
        if request.args.get('btn_newPlayer') == 'Neuer Spieler':
            print('Neuer SPIELER')
            player = player + ["Spieler_"+str(count_player)]
            count_player += 1
            game_data = set_new_player(game_data)
        # NEW GAME-ROUND
        if request.args.get('btn_newRound') == 'Neue Runde':
            print('Neue RUNDE')
            count_rounds += 1
            game_data = next_round(game_data)
        # CHANGE-PLAYER-NAME
        for p_i in range(len(player)):
            p_req = request.args.get('player_'+str(p_i+1))
            if p_req != player[p_i] and p_req != None:
                print('Aktualisierter SpielerName')
                player[p_i] = p_req
        # CHANGE GAME-DATA
        for req in request.args:
            str_req = str(req)
            print(str_req)
            if 'cell' in str_req:
                if "minus" in str_req:
                    point_name = "minus_points"
                else:
                    point_name = "plus_points"
                val_req = int(request.args.get(str_req))
                split_str_req = str_req.split('_')
                points = game_data[int(split_str_req[0])-1][point_name]
                points[int(split_str_req[2])-1] = val_req
        game_data = calc_game_state(game_data, count_player)
    
    session['player'] = player
    session['game_data'] = game_data
    return redirect(url_for('home'))

def plot_game_state(game_data, player):
    round_count = len(game_data)
    print(round_count)

    xScale = np.linspace(1, round_count, round_count)

    # Create traces
    data = []
    for i_p in range(len(player)):
        y = []
        for i_g in range(len(game_data)):
            y.append(game_data[i_g]['game_points'][i_p])
        trace_i = go.Scatter(
            x = xScale,
            y = y,
            name = player[i_p]
        )
        data.append(trace_i)

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

if __name__ == "__main__":
    # db.create_all()
    app.debug = True # --> autoreload
    app.run(host='0.0.0.0', port=80)#(threaded=True)