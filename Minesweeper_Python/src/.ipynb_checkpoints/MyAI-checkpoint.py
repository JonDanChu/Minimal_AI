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
		self.__maxShown = (colDimension * rowDimension) - totalMines

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
		if self.__maxShown == self.__numShown:
			print(self.__maxShown)
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
		
		# Going to start as 1
		num_ones = number

		# Check how many neighbors are revealed && have a value of 1
		for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if not self.inBounds((new_x, new_y)):
					continue

				if self.__grid[new_x][new_y] == 1:
					num_ones += 1

		# If 1 or 2 number 1's don't do anything
		#	We can't make any solid decision on where the mine is yet so don't reveal anything yet
		#	Instead:
		#  		-	Don't add anything to the set
		# 		-	Pop off from what's already in the set

		if (num_ones < 3) or ((num_ones == 3) and self.checkStraights()):
			next_action = self.prepareNext()
			
			return next_action

		# Else should be able to find the mine
		mine = self.checkDiagonal() or self.checkCorner() or ()

		# Can't make a solid decision — don't add anything, pop from existing set
		if not mine:
			return self.prepareNext()

		for dx, dy in ADJACENT_NEIGHBORS:
				new_x = self.__tileX + dx
				new_y = self.__tileY + dy

				if (new_x, new_y) == mine:
					continue

				if not self.inBounds((new_x, new_y)):
					continue
				
				if self.__grid[new_x][new_y] == -2:
					self.__grid[new_x][new_y] = -3
					self.__revealSet.add(Action(AI.Action.UNCOVER, new_x, new_y))

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

	def checkStraights(self) -> bool:
		upper = (self.__tileX, self.__tileY - 1)
		lower = (self.__tileX, self.__tileY + 1)

		if self.inBounds(upper) and self.inBounds(lower):
			return (self.__grid[upper[0]][upper[1]] == 1) and (self.__grid[lower[0]][lower[1]] == 1)

		left = (self.__tileX - 1, self.__tileY)
		right = (self.__tileX + 1, self.__tileY)

		if self.inBounds(left) and self.inBounds(right):
			return (self.__grid[left[0]][left[1]] == 1) and (self.__grid[right[0]][right[1]] == 1)

		return False	

	#########
	# For 16 special cases
	##########

	# Check for the case
	# 			X	1			1	X
	# 			1	M			M	1			X	1	X			1	M	1
	# Case 1:	X	1	Case 2:	1	X   Case 3:	1	M	1	Case 4:	X	1	X
	def checkDiagonal(self) -> tuple:
		# check for out of bounds!!
		for dir in [-1, 1]:
			upper = (self.__tileX + dir, self.__tileY - 1)
			lower = (self.__tileX + dir, self.__tileY + 1)

			lhs = (self.__tileX - 1, self.__tileY + dir)
			rhs = (self.__tileX + 1, self.__tileY + dir)
			
			# Case 1 and 2
			if self.inBounds(upper) and self.inBounds(lower):
				if (self.__grid[upper[0]][upper[1]] == 1) and (self.__grid[lower[0]][lower[1]] == 1):
					return (self.__tileX + dir, self.__tileY)
			
			# Case 3 and 4
			if self.inBounds(lhs) and self.inBounds(rhs):
				if (self.__grid[lhs[0]][lhs[1]] == 1) and (self.__grid[rhs[0]][rhs[1]] == 1):
					return (self.__tileX, self.__tileY + dir)
		
		return ()
	
	########################
	# Check
	# - Corners
	# - Vertical Middle
	# - Horizontal Middle
	#########################
	def checkCorner(self) -> tuple:
		for dx, dy in CORNER_NEIGHBORS:
			new_x = self.__tileX + dx
			new_y = self.__tileY + dy

			c_side = (new_x, self.__tileY)
			c_vert = (self.__tileX, new_y)
			c_mine = (new_x, new_y)

			v_side = (new_x, self.__tileY)
			v_diag = (new_x, new_y)
			v_mine = (self.__tileX, new_y)

			h_vert = (self.__tileX, new_y)
			h_diag = (new_x, new_y)
			h_mine = (new_x, self.__tileY)

			#check for bounds first! See the diagonal check for structure
			if self.inBounds(c_side) and self.inBounds(c_vert):
				if (self.__grid[c_side[0]][c_side[1]] == 1) and (self.__grid[c_vert[0]][c_vert[1]] == 1):
					self.__revealSet.add(Action(AI.Action.FLAG, *c_mine))
					return c_mine
			
			# Vertical Middle
			if self.inBounds(v_side) and self.inBounds(v_diag):
				if (self.__grid[v_side[0]][v_side[1]] == 1) and (self.__grid[v_diag[0]][v_diag[1]] == 1):
					self.__revealSet.add(Action(AI.Action.FLAG, *v_mine))
					return v_mine
			
			# Horizontal Middle
			if self.inBounds(h_vert) and self.inBounds(h_diag):
				if (self.__grid[h_vert[0]][h_vert[1]] == 1) and (self.__grid[h_diag[0]][h_diag[1]] == 1):
						self.__revealSet.add(Action(AI.Action.FLAG, *h_mine))
						return h_mine
				
		return ()
