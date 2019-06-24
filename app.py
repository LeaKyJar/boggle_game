from flask import Flask, request, jsonify, Response, json
from boggle_solver import Boggle
import secrets
import time
app = Flask(__name__)

fd = open("dictionary.txt", "r")
word_dic = str(fd.read()).split("\n")
fd.close()
games = {}
counter = 1

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/games", methods=["POST"])
def create_game():
    if request.method == "POST":
        if "duration" not in request.args:
            return Response("duration missing", status=400)
        if "random" not in request.args:
            return Response("random indicator missing", status=400)
        global counter, games
        b = None
        id = counter
        counter += 1
        duration = request.args.get("duration")
        rand = request.args.get("random")
        board = ""
        token = token_generator()
        if rand == "true": # generate random Boggle board
            b = Boggle(word_dic)
        elif rand == "false":
            if "board" in request.args: # use given board
                board = request.args.get("board")
                b = Boggle(word_dic, board)
            else: # use default board
                f = open("test_board.txt", "r")
                board = str(f.readline())
                board = board.strip("\n")
                b = Boggle(word_dic, board)
                f.close()
        print(b.show_board())
        temp = { # dic for storing game data
        "id": id,
        "token": token,
        "duration": duration,
        "board": board
        }
        json_response = json.dumps(temp)
        temp["points"] = 0 # initialize score
        temp["start"] = time.perf_counter() # initialize start time
        temp["used_words"] = set()
        games[id] = (b, temp)
    return Response(json_response, status=201, mimetype='application/json')

@app.route("/games/<int:id>", methods=["GET","PUT"])
def game(id): #determines all responses to queries in game
    if id not in games:
        return Response("id not found", status=404)
    temp = games[id][1]

    if request.args.get("token") != temp["token"]:
        return Response("Incorrect Token", status=401)

    time_left = remaining_time(temp)
    temp["time_left"] = time_left
    if time_left<0:
        return Response("Time's up", status=200)

    if request.method == "GET":
        return show_game(id)

    if request.method == "PUT":
        word = request.args.get("word")
        return play_game(id, word)

def play_game(id: int, word: str):
    temp = games[id][1]
    if word in temp["used_words"]:
        return Response("you have already tried this valid word", status=200)
    else:
        correct = games[id][0].guess_word(word)
        if correct:
            temp["points"]+=10
            temp["used_words"].add(word)
        else:
            return Response("word not in board", status=200)
    return Response(json.dumps({
        "id": temp["id"],
        "token": temp["token"],
        "duration": temp["duration"],
        "board": temp["board"],
        "time_left": temp["time_left"],
        "points": temp["points"]
    }), status=200, mimetype='application/json')

def show_game(id: int):
    temp = games[id][1]
    return Response(json.dumps({
        "id": temp["id"],
        "token": temp["token"],
        "duration": temp["duration"],
        "board": temp["board"],
        "time_left": temp["time_left"],
        "points": temp["points"]
    }), status=200, mimetype="application/json")

def token_generator():
    return secrets.token_hex(16)

def remaining_time(temp: dict):
    current = time.perf_counter()
    return int(temp["duration"]) - int(current - temp["start"])


if __name__ == '__main__':

    app.run(port=8080)