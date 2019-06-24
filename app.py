from flask import Flask, request, Response, json, make_response, render_template
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
def land():
    return make_response(render_template("landing.html"), 200)

@app.route("/games", methods=["POST"])
def create_game():
    if request.method == "POST":
        content = request.get_json()
        if content == None:
            return Response(json.dumps({"message": "JSON payload missing"}), status=400)
        if "duration" not in content:
            return Response(json.dumps({"message": "duration was not provided"}), status=400)
        if "random" not in content:
            return Response(json.dumps({"message": "random was not provided"}), status=400)
        global counter, games
        b = None
        id = counter
        counter += 1
        duration = content["duration"]
        rand = content["random"]
        board = ""
        token = token_generator()
        if rand: # generate random Boggle board
            b = Boggle(word_dic)
            board = b.board
        elif not rand:
            if "board" in content: # use given board
                board = content["board"]
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
        temp["used_words"] = set() # use set to track words used for this game
        games[id] = (b, temp)
    return Response(json_response, status=201, mimetype='application/json')

@app.route("/games/<id>", methods=["GET","PUT"])
def game(id): #determines all responses to queries in game
    content = request.get_json()
    id = int(id)
    if id not in games:
        return Response(json.dumps({"message": "invalid id"}), status=404)
    temp = games[id][1]

    time_left = remaining_time(temp)
    temp["time_left"] = time_left
    if time_left<0:
        return Response(json.dumps({"message": "game duration exceeded"}), status=400)

    if request.method == "GET":
        return show_game(id)

    if request.method == "PUT":
        if content == None:
            return Response(json.dumps({"message": "JSON payload missing"}), status=400)
        if "token" not in content:
            return Response(json.dumps({"message": "token was not provided"}), status=400)
        if content["token"] != temp["token"]:
            return Response(json.dumps({"message": "incorrect token provided"}), status=401)
        if "word" not in content:
            return Response(json.dumps({"message": "word was not provided"}), status=400)
        word = content["word"]
        return play_game(id, word)

def play_game(id: int, word: str):
    temp = games[id][1]
    if word in temp["used_words"]:
        return Response(json.dumps({"message": "this valid word has already been used"}), status=200)
    else:
        correct = games[id][0].guess_word(word)
        if correct:
            temp["points"]+=len(word)
            temp["used_words"].add(word)
        else:
            return Response(json.dumps({"message": "word is incorrect"}), status=400)
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