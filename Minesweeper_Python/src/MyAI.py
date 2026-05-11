# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
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
		# -2 = not revealed
		# -1 = flag
		# 0/1 = value
		self.__grid = [[-2 for _ in colDimension] for _ in rowDimension] # what values do these start with
		self.__colDimension = colDimension
		self.__rowDimension = rowDimension

		self.__mineTotal = totalMines

		# keep updating these to know where we are
		self.__tileX = startX
		self.__tileY = startY

		# Set to keep track of tiles to reveal?
		self.__revealSet = set()

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
		
		# don't need case to check for a mine

		# make a copy of the neighbors to check - 
		# - how many actually need to be revealed
		# - how many 1's are arround

		# After result of final reveal/move we should leave
		if self.__numShown == (self.__colDimension * self.__rowDimension - self.__mineTotal):
			return (AI.ACTION.LEAVE)
		
		# Update the local copy of the grid
		self.grid[self.__tileX][self.__tileY] = number

		if number < 1:
			# For number == 0 or number == -1 (there is a mine here bc flag)
			
			# Check all neighbors and add all to the set
			for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if not self.checkBounds(new_x, new_y):
					continue
				
				if self.__grid[new_x][new_y] == -2:
					self.__revealSet.add(Action(AI.ACTION.UNCOVER, new_x, new_y))

			next_action = self.prepareNext()
		
			return next_action
		
		# Going to start as 1
		num_ones = number

		# Neighbors w a 1
		neighborhood = []

		# Check how many neighbors are revealed && have a value of 1
		for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if self.__grid[new_x][new_y] == 1:
					num_ones += 1
					neighborhood.append((new_x, new_y))

		# If 1 or 2 number 1's don't do anything
		#	We can't make any solid decision on where the mine is yet so don't reveal anything yet
		#	Instead:
		#  		-	Don't add anything to the set
		# 		-	Pop off from what's already in the set

		if (num_ones == 3) and self.checkStraights():
			next_action = self.prepareNext()
			
			return next_action

		# Else should be able to find the mine
		mine = ()

		# # Check for the case
		# # X	1
		# # 1	M
		# # X	1
		# if self.checkDiagonal(1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX + 1, self.__tileY))
		# 	m = (self.__tileX + 1, self.__tileY)
		
		# # Check for the case
		# # 1	X
		# # M	1
		# # 1	X
		# elif self.checkDiagonal(-1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX - 1, self.__tileY))
		# 	m = (self.__tileX - 1, self.__tileY)

		if not self.checkDiagonal():
			print("Diagonal Case: Fail")
		else:
			print("Diagonal Case: Pass")
		
		# figure out a for loop to loop through all combos of (±1, ±1)
		# elif self.checkCorner(1,1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX + 1, self.__tileY - 1))
		# elif self.checkCorner(1, -1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX + 1, self.__tileY - 1))
		# elif self.checkCorner(-1,1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX - 1, self.__tileY + 1))
		# elif self.checkCorner(-1, -1):
		# 	self.__revealSet.add(Action(AI.ACTION.FLAG, self.__tileX - 1, self.__tileY - 1))
		
		if not self.checkCorner():
			print("Corner Case: Fail")
		else:
			print("Corner Case: Pass")
		
		for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if (new_x, new_y) == mine:
					continue

				if not self.checkBounds(new_x, new_y):
					continue
				
				if self.__grid[new_x][new_y] == -2:
					self.__revealSet.add(Action(AI.ACTION.UNCOVER, new_x, new_y))

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
			next_action = self.actionSet.pop()
		except KeyError:
			# if the set was empty
			print("Actionset was empty")
			return Action(AI.ACTION.LEAVE)
	
		self.__tileX = next_action.getX()
		self.__tileY = next_action.getY()

		# Next move will be an UNCOVER was called
		if next_action.getMove() == AI.Action.UNCOVER:
			self.__numShown += 1
		
		# For testing
		return next_action

	def checkBounds(self, x_val:int, y_val:int) -> bool:
		return (x_val > 0 and x_val < self.colDimension) and (y_val > 0 and y_val < self.rowDimension)
	

	#########
	# For 6 special cases
	# may need to change to return an action or tuple so that we know which tuple
	# the AI idenitifed to have the mine
	##########
	
	# Check for the case
	# X	1		1	X
	# 1	M		M	1
	# X	1	and 1	X
	def checkDiagonal(self) -> bool:
		# check for out of bounds!!
		for dir in [-1, 1]:
			upper = (self.__tileX + dir, self.__tileY - 1)
			lower = (self.__tileX + dir, self.__tileY + 1)
			
			if (not self.checkBounds(upper[0], upper[1])) or (not self.checkBounds(lower[0], lower[1])):
						return False
			
			return (self.__grid[upper[0]][upper[1]] == 1) and (self.__grid[lower[0]][lower[1]] == 1)
	
	def checkCorner(self) -> bool:
		for dx, dy in CORNER_NEIGHBORS:
			new_x = self.__tileX + dx
			new_y = self.__tileY + dy

			if (self.__grid[new_x][self.__tileY] == 1) and (self.__grid[self.__tileX][new_y] == 1):
				self.__revealSet.add(Action(AI.ACTION.FLAG, new_x, new_y))
				return True
		
		return False