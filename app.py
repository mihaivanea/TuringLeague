from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from threading import Timer
from player import Player
from human import Human
from chatbot import ChatBot
from bots import bot
from game import Game
import random
from db import database

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

players_in_game = {} # username -> game
players_in_lobby = [] # usernames
username_to_player = {} # username -> player
session_to_username = {}
db = database.Database()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/highscores')
def highscores():
    return render_template('highscores.html')

@app.route('/bots')
def bots():
    return render_template('bots.html')

@app.route('/leaderboards/bots', methods=['GET'])
def get_best_bots():
    return db.get_top_bots_table()

@app.route('/leaderboards/users', methods=['GET'])
def get_best_users():
    return db.get_top_users_table()

@socketio.on('start_request', namespace='/chat')
def start_request(message):
    username = message['nickname']
    print 'start request by ' + username

    if not ((username in players_in_game) or (username in players_in_lobby)):
        player = Human(username, request.sid, db)
        username_to_player[username] = player
        session_to_username[request.sid] = username

        if not players_in_lobby:
            print 'adding ' + username  + ' to lobby...'
            players_in_lobby.append(username)

        else:
            # remove first player form lobby
            opponent_username = players_in_lobby.pop()
            opponent = username_to_player[opponent_username]

            if random.choice([True, False]):
                name, random_bot = random.choice(bot.BOTS)
                chatbot = ChatBot(name, random_bot.start_session(),
                        random_bot.bot_type(), db)
                print 'matching ' + opponent.name() + ' with ' + chatbot.name()
                players_in_game[opponent] = Game(opponent, chatbot, players_in_game)

                print 'adding ' + username  + ' to lobby...'
                players_in_lobby.append(username)

            else:
                print 'matching ' + player.name() + ' with ' + opponent.name()
                #if random.choice([True, False]):
                game = Game(player, opponent, players_in_game)
                #else:
                #    game = Game(opponent, player, players_in_game)

                players_in_game[player] = game
                players_in_game[opponent] = game

@socketio.on('message_submitted', namespace='/chat')
def message_submitted(message):
    print 'message submitted by ' + message['user']
    players_in_game[username_to_player[message['user']]].message(message['user'], message['message'])

@socketio.on('bot_decision', namespace='/chat')
def bot_decision(message):
    print 'bot decision sent by ' + message['user']
    try:
        players_in_game[username_to_player[message['user']]].attacker_guess(message['bot'])
    except KeyError:
        pass

@socketio.on('loss', namespace='/chat')
def player_forfeit(message):
    print 'forfeit by ' + message['user']
    try:
        players_in_game[username_to_player[message['user']]].player_forfeit(message['user'])
    except KeyError:
        pass

@socketio.on('connect', namespace='/chat')
def socket_connect():
    print 'connect'

@socketio.on('disconnect', namespace='/chat')
def socket_disconnect():
    try:
        print 'discconect by ' + session_to_username[request.sid]
        players_in_game[username_to_player[session_to_username[request.sid]]].player_forfeit(session_to_username[request.sid])
    except KeyError:
        pass

def start_timer(timer):
    timer.start()

def create_bot_game(player):
    print player.name() + ' will play a bot game'

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
