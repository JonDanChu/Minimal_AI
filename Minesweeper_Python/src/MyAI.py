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

adjacent_neighbors = {[-1,-1], [0,-1], []} # list of transitions (change to x, change to y) from middle to all neighbors 

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__grid = int[rowDimension][colDimension] # what values do these start with
		self.__mineTotal = totalMines

		# keep updating these to know where we are
		self.__tileX = startX
		self.__tileY = startY

		# Set to keep track of tiles to reveal?
		self.__revealSet = []



		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		if number == 0:
			# Check all neighbors and add all to the set
			for x in range(0,8):
				new_x = 
				new_y = 

				self.checkBounds(new_x, new_y)
				# check if out of bounds, if so continue
				
				self.revealSet.add([])

		elif number == 1:
			# mine is close by?

		else:
			# it's a mine!!

		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def checkBounds(self, x_val:int, y_val:int) -> bool:
		return (x_val > 0 and x_val < self.colDimension) and (y_val > 0 and y_val < self.rowDimension)
			
