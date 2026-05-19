# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Daniel Chu and Ethan Nguyen
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action

ADJACENT_NEIGHBORS = ((-1,-1), (0,-1), (1, -1), (-1,0), (1, 0), (-1,1), (0,1), (1, 1)) # list of transitions (change to x, change to y) from middle to all neighbors 
CORNER_NEIGHBORS = ((-1,-1), (1, -1), (-1,1), (1, 1))

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		# Copy of the world
		# -3 = queued for reveal
		# -2 = not revealed
		# -1 = flag
		# 0/1 = value
		self.__grid = [[-2 for _ in range(colDimension)] for _ in range(rowDimension)]
		self.__colDimension = colDimension
		self.__rowDimension = rowDimension

		self.__mineTotal = totalMines

		# keep updating these to know where we are
		self.__tileX = startX
		self.__tileY = startY

		# Set to keep track of tiles to reveal?
		self.__revealSet = set() # deque?

		# number of reveals not number moves (bc could repeat flag/unflag)
		self.__numShown = 0

		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# After result of final reveal/move we should leave
		if self.__numShown == (self.__colDimension * self.__rowDimension - self.__mineTotal):
			return Action(AI.Action.LEAVE)
		
		# Update the local copy of the grid
		self.__grid[self.__tileX][self.__tileY] = number

		if number < 1:
			# For number == 0 or number == -1 (there is a mine here bc flag)
			
			# Check all neighbors and add all to the set
			for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if not self.inBounds((new_x, new_y)):
					continue
				
				if self.__grid[new_x][new_y] == -2:
					self.__grid[new_x][new_y] = -3
					self.__revealSet.add(Action(AI.Action.UNCOVER, new_x, new_y))

			next_action = self.prepareNext()

			return next_action
		
		neighbors = []

		# Check how many neighbors aren't revealed
		for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if not self.inBounds((new_x, new_y)):
					continue

				if self.__grid[new_x][new_y] == -2:
					neighbors.append((new_x, new_y))

		if len(neighbors) == 1:
			self.__revealSet.add(Action(AI.Action.FLAG, *(neighbors[0])))

		next_action = self.prepareNext()
		return next_action
	
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def prepareNext(self) -> "Action Object":
		##
		# Prepare for the next action call and return that next action
		##

		try:
			next_action = self.__revealSet.pop()
		except KeyError:
			return Action(AI.Action.LEAVE)
	
		self.__tileX = next_action.getX()
		self.__tileY = next_action.getY()

		# Next move will be an UNCOVER was called
		if next_action.getMove() == AI.Action.UNCOVER:
			self.__numShown += 1
		
		# For testing
		return next_action

	def inBounds(self, coord:tuple) -> bool:
		x_val = coord[0]
		y_val = coord[1]
		return (x_val >= 0 and x_val < self.__colDimension) and (y_val >= 0 and y_val < self.__rowDimension)