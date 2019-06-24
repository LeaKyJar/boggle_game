#Boggle API

Simple API allowing you to play a game of Boggle.

##Deployment instructions
Navigate to root directory of the project from your command line and use:
```
python app.py
``` 
The command should fire up the API endpoints to listen on your local server

A deployed version for testing can be found temporarily at https://boggle-game-kenjyi.herokuapp.com

##Create Game
Make a POST request to https://boggle-game-kenjyi.herokuapp.com/games with the following parameters to create a new Boggle game:
- `duration` (required)(JSON payload): the time (in seconds) that specifies the duration of the game
- `random` (required)(JSON payload): if `true`, then the game will be generated with random board. Otherwise, it will be generated based on input.
- `board` (optional)(JSON payload): if `random` is not true, this will be used as the board for new game. If this is not present, new game will get the default board from `test_board.txt`

##Play Game
Make a PUT request to https://boggle-game-kenjyi.herokuapp.com/games/[id] with the following parameters to try a word in the Boggle game:
- `id` (required)(part of url): The ID of the game
- `token` (required)(JSON payload): The token for authenticating the game
- `word` (required)(JSON payload): The word that can be used to play the game

##Show Game
Make a GET request to https://boggle-game-kenjyi.herokuapp.com/games/[id] with the following parameters to get current state of the game in the Boggle game:
- 'id' (required)(part of url): The ID of the game