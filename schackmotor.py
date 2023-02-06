import chess
from hashlib import sha256
import copy
from chess import *
from termcolor import colored
import time


def sort_moves(pos):

	return pos.legal_moves
	move_list = []
	for i in pos.legal_moves:
		if ("x" or "+") in pos.san(i):
			move_list.insert(0, i)
		else:
			move_list.append(i)
	return move_list

def find_piece_index(pos, piece):
	i_index = 0
	pos_list = []
	for i in pos.fen().split(" ")[0].split("/"):
		j_index = 1
		for j in i:
			if j.isdigit():
				j_index = j_index * int(j)
			elif j == piece:
				pos_list.append([i_index, j_index])
		i_index += 1
	return pos_list


def evl(pos):
	summ = 0
	game_time = 0
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

	summ += 0.05 * (abs(3.5 - (find_piece_index(pos, "K")[0][0])) + abs(3.5 - (find_piece_index(pos, "K")[0][1])))
	summ -= 0.05 * (abs(3.5 - (find_piece_index(pos, "k")[0][0])) + abs(3.5 - (find_piece_index(pos, "k")[0][1])))
	game_time = 32 - len(pos.piece_map().keys()):
	summ -= game_time * 0.01 * (abs(3.5 - (find_piece_index(pos, "K")[0][0])) + abs(3.5 - (find_piece_index(pos, "K")[0][1])))
	summ += game_time * 0.01 * (abs(3.5 - (find_piece_index(pos, "k")[0][0])) + abs(3.5 - (find_piece_index(pos, "k")[0][1])))

	return summ

def hash_function(s):
	return sha256(s.encode('utf-8')).hexdigest()

hash_dict = {}
iter_num = 0
rec = 0

def minimax(pos, alpha, beta, maxi, depth, prev_move):
	global iter_num
	global rec
	iter_num += 1

	if depth == 0 or pos.is_checkmate() or pos.is_stalemate():
		pos_eval = evl(pos)

		if pos.is_stalemate():
			return 0, prev_move

		if pos.is_checkmate() and pos.fen().split(" ")[1] == "w":
			return -9999999999999999999, str(prev_move)
		elif pos.is_checkmate() and pos.fen().split(" ")[1] == "b":
			return 9999999999999999999, str(prev_move)

		# if pos.is_checkmate() == 0:
		# 	for i in pos.legal_moves:
		# 		if "x" in pos.san(i) or "+" in pos.san(i):
		# 			return minimax(pos, alpha, beta, maxi, 1, prev_move)

		return pos_eval, prev_move
 
	if maxi:
		pos_hash = hash_function(pos.fen())
		if pos_hash in hash_dict:
			return hash_dict[pos_hash][0], hash_dict[pos_hash][1]

		max_eval = -99999999999999999999
		sorted_moves = sort_moves(pos)
		for i in sorted_moves:
			board = pos.copy()
			board.push_uci(str(i))
			eval, next_move = minimax(board, alpha, beta, 0, depth - 1, str(i))
			if eval > max_eval:
				next_best_move = next_move
				best_move = str(i)
			max_eval = max(max_eval, eval)
			alpha = max(alpha, eval)
			if beta <= alpha:
				break

		hash_dict[hash_function(board.fen())] = (max_eval, best_move + " " + next_best_move)
		return max_eval, best_move + " " + next_best_move

	else:
		pos_hash = hash_function(pos.fen())
		if pos_hash in hash_dict:
			return hash_dict[pos_hash][0], hash_dict[pos_hash][1]

		min_eval = 99999999999999999999
		sorted_moves = sort_moves(pos)
		for i in sorted_moves:
			board = pos.copy()
			board.push_uci(str(i))
			eval, next_move = minimax(board, alpha, beta, 1, depth - 1, str(i))
			if eval < min_eval:
				next_best_move = next_move
				best_move = str(i)
			min_eval = min(min_eval, eval)
			beta = min(beta, eval)
			if beta <= alpha:
				break

		hash_dict[hash_function(board.fen())] = (min_eval, best_move + " " + next_best_move)
		return min_eval, best_move + " " + next_best_move
 


def engine(fen, depth):
	board = chess.Board()
	board.set_fen(fen)
	if fen.split(" ")[1] == "w":
		result = (minimax(board, -99999999999999999999, 99999999999999999999, 1, depth, ""))
	else:
		result = (minimax(board, -99999999999999999999, 99999999999999999999, 0, depth, ""))
	if result[0] == 9999999999999999999:
		return ("vit får schackmatt!!!\noptimal fortsättning på spelet: " + result[1], result)
	elif result[0] == -9999999999999999999:
		return ("svart får schackmatt!!!\noptimal fortsättning på spelet: " + result[1], result)
	else:
		return ("positionens värdering: " + str(result[0]) + "\n" + "optimal fortsättning på spelet: " + result[1][:len(result[1]) - 5:], result)

class chess_engine():

	def __init__(self, board, engine_depth):
		self.board = board
		self.engine_depth = engine_depth

	def evaluate_fen(self, fen):
		start = time.time()
		evl = engine(fen, self.engine_depth)
		print(evl[0])
		end = time.time()
		print(end - start)
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
		self.board.push_uci(str(move))
		print("du gör draget: " + move)
		print(self.board)
		print("-----------------------")
		return self.board



# olika kommandon man kan använda:

position = chess.Board()
game = chess_engine(position, 8)
# game.set_fen("N1k5/8/8/8/r5p1/6P1/6K1/8 w - - 0 2")
# game.move("a8b6")
# game.play()
game.evaluate_fen("k2r4/8/5r2/8/2K5/8/8/8 b - - 0 1")
print(iter_num)
# print(hash_dict)
# position.set_fen("k2r4/8/5r2/8/2K5/8/8/8 b - - 0 1")
