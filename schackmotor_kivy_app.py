import chess
import copy
from chess import *


def sort_moves(pos):
	pos_eval = evl(pos)
	move_list = []
	for i in pos.legal_moves:
		board = copy.copy(pos)
		board.push_uci(str(i))
		move_eval = evl(board)
		if move_eval != pos_eval or board.is_check() == 1:
			move_list.insert(0, i)
		else:
			move_list.append(i)
	return move_list

def evl(pos):
	summ = 0
	for i in pos.board_fen():
		if i == "p":
			summ -= 1
		elif i == "n":
			summ -= 3
		elif i == "b":
			summ -= 3
		elif i == "r":
			summ -= 5
		elif i == "q":
			summ -= 10
		elif i == "P":
			summ += 1
		elif i == "N":
			summ += 3
		elif i == "B":
			summ += 3
		elif i == "R":
			summ += 5
		elif i == "Q":
			summ += 10
	return summ

def minimax(pos, alpha, beta, maxi, depth, prev_move):

	if depth == 0 or pos.is_checkmate():
		if pos.is_checkmate() and pos.fen().split(" ")[1] == "w":
			return -99999999999999999999, str(prev_move)
		elif pos.is_checkmate() and pos.fen().split(" ")[1] == "b":
			return 99999999999999999999, str(prev_move)
		return evl(pos), prev_move
 
	if maxi:
		max_eval = -99999999999999999999
		# best_move = ""
		# next_best_move = ""
		for i in sort_moves(pos):
			board = copy.copy(pos)
			board.push_uci(str(i))
			eval, next_move = minimax(board, alpha, beta, 0, depth - 1, str(i))
			if eval > max_eval:
				next_best_move = next_move
				best_move = str(i)
			max_eval = max(max_eval, eval)
			alpha = max(alpha, eval)
			if beta <= alpha:
				break
		return max_eval, best_move + " " + next_best_move
 
	else:
		min_eval = 99999999999999999999
		# best_move = ""
		# next_best_move = ""
		for i in sort_moves(pos):
			board = copy.copy(pos)
			board.push_uci(str(i))
			eval, next_move = minimax(board, alpha, beta, 1, depth - 1, str(i))
			if eval < min_eval:
				next_best_move = next_move
				best_move = str(i)
			min_eval = min(min_eval, eval)
			beta = min(beta, eval)
			if beta <= alpha:
				break

		return min_eval, best_move + " " + next_best_move
 


def engine(fen, depth):
	board = chess.Board()
	board.set_fen(fen)
	if fen.split(" ")[1] == "w":
		result = (minimax(board, -99999999999999999999, 99999999999999999999, 1, depth, ""))
	else:
		result = (minimax(board, -99999999999999999999, 99999999999999999999, 0, depth, ""))
	if result[0] == 99999999999999999999:
		return ("vit får schackmatt!!!\noptimal fortsättning på spelet: " + result[1], result)
	elif result[0] == -99999999999999999999:
		return ("svart får schackmatt!!!\noptimal fortsättning på spelet: " + result[1], result)
	else:
		return ("positionens värdering: " + str(result[0]) + "\n" + "optimal fortsättning på spelet: " + result[1][:len(result[1]) - 5:], result)

class chess_engine():

	def __init__(self, board, engine_depth):
		self.board = board
		self.engine_depth = engine_depth

	def evaluate_fen(self, fen):
		evl = engine(fen, self.engine_depth)
		print(evl[0])
		return evl

	def set_fen(self, fen):
		self.board.set_fen(fen)

	def play(self):
		move = str(engine(self.board.fen(), self.engine_depth)[1][1])[0:4]
		self.board.push_uci(str(move))
		print("datorn gör draget: " + str(move))
		print(self.board)
		print("-----------------------")
		return self.board, move

	def move(self, move):
		board.push_uci(str(move))
		print("du gör draget: " + move)
		print(self.board)
		print("-----------------------")
		return self.board

board = chess.Board()
game = chess_engine(board, 4)
game.evaluate_fen("N1k5/8/8/8/r5p1/6P1/6K1/8 w - - 0 2")	


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy import *


class AgeCalculator(App):
	def build(self):
		self.window = GridLayout()
		self.window.cols = 1
		self.moveRequest = Label(text = "Enter your move")
		self.window.add_widget(self.moveRequest)
		self.move = TextInput(multiline=False)
		self.window.add_widget(self.move)
		self.button = Button(text = "Calculate FEN")
		self.button.bind(on_press = self.getMove)
		self.window.add_widget(self.button)
		self.depthControl = Slider(min = 0, max = 50)
		self.window.add_widget(Label(text ="schackmotorns djup"))
		self.window.add_widget(Label(text ='Slider Value'))
		self.depthValue = Label(text ='0')
		self.window.add_widget(self.depthValue)
		self.window.add_widget(self.depthControl)
		self.depthControl.bind(value = self.on_value)
		self.depth = 0
		return self.window

	def on_value(self, instance, depth):
		self.depthValue.text = "% d"% depth
		self.depth = int(self.depthValue.text)

	def getMove(self, event):
		board = chess.Board()
		game = chess_engine(board, self.depth)
		inputt = self.move.text
		self.moveRequest.text =	game.evaluate_fen(inputt)[0]


if __name__ == "__main__":
	AgeCalculator().run()
