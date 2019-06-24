import string
import random

class Boggle:
    def __init__(self, word_dic, board=None):
        if board is None:
            board = self.random_board()
        self.board = board
        self.word_dic = word_dic
        self.__dic = self.make_dic(self.board)
        self.__visited = set()

    # create dictionary of all adjacent tiles for each tile
    def make_dic(self, board_str: str) -> dict:
        dic = {}
        board_str = board_str.split(", ")
        for i in range(len(board_str)):
            temp = []
            if i == 0: # upper left of grid
                temp.append((board_str[i + 1],i+1))
                temp.append((board_str[i + 4], i+4))
            elif i == 3: # upper right of grid
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i + 4], i+4))
            elif i == 12: # lower left of grid
                temp.append((board_str[i + 1], i+1))
                temp.append((board_str[i - 4], i-4))
            elif i == 15: # lower right of grid
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i - 4], i-4))
            elif i<4: # upper row of grid
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i + 1], i+1))
                temp.append((board_str[i + 4], i+4))
            elif i>11: # lower row of grid
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i + 1], i+1))
                temp.append((board_str[i - 4], i-4))
            elif i%4 == 0:  # leftmost column of grid
                temp.append((board_str[i + 1], i+1))
                temp.append((board_str[i - 4], i-4))
                temp.append((board_str[i + 4], i+4))
            elif i%4==3: # rightmost column of grid
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i - 4], i-4))
                temp.append((board_str[i + 4], i+4))
            else: # all other tiles
                temp.append((board_str[i - 1], i-1))
                temp.append((board_str[i + 1], i+1))
                temp.append((board_str[i - 4], i-4))
                temp.append((board_str[i + 4], i+4))
            dic[board_str[i], i] = temp
        return dic

    # check that word is in the Boggle board
    def word_check(self, word: str, ls: list) -> bool:
        word = word[1:]
        if len(word) == 0: # word exists in grid
            self.__visited.clear()
            return True
        keys = list(filter(lambda x: x[0] == word[0] or x[0] == "*", ls))  # find all keys with the first letter
        ans = False
        if len(keys) == 0:  # letter is not adjacent
            self.__visited.clear()
            return False
        for i in keys: # next letter in word is adjacent
            if i not in self.__visited: # prevents same letter from repeating
                self.__visited.add(i)

                ans = self.word_check(word, self.__dic[i])
            if ans: # returns the moment a solution is found
                return ans

    # check that word is in the dictionary
    def dic_check(self, word: str) -> bool:
        if word.lower() in self.word_dic:
            return True
        return False

    # check if word is correct
    def guess_word(self, word: str) -> bool:
        word = word.upper()
        word_copy = word # backup of word
        ans = False
        keys = list(filter(lambda x: x[0] == word[0] or x[0] == "*", self.__dic))  # find all keys with the first letter
        if len(keys) == 0:  # letter does not exist
            return False
        for i in keys:
            if not ans: # Stop trying once a valid answer is found
                self.__visited.add(i) # add letter and index to visited set
                ans = self.word_check(word, self.__dic[i])
        if ans:
            ans = self.dic_check(word_copy)
        return ans

    # returns string representation of the board
    def show_board(self) -> str: # prints a string in 4x4 format
        board = self.board.split(", ")
        board = str(board[0:4]) + "\n" + str(board[4:8]) + "\n" + str(board[8:12]) + "\n" + str(board[12:])
        return board

    # generate a random string of 16 chars separated by commas
    def random_board(self) -> str:
        board = []
        for i in range(16):
            board.append(string.ascii_uppercase[random.randint(0, len(string.ascii_uppercase)-1)])
        board = str(board)
        board = ''.join(c for c in board if c not in "[]''")
        return board


