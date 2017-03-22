
from combinatorialgametools import mex
#try:
#   import cPickle as pickle
#except:
#   import pickle

class GalesNim(object):

	def __init__(self,mylist, number_Of_Zero_Piles=0, k=1):
		self.piles=list(mylist)
		self.number_Of_Zero_Piles=number_Of_Zero_Piles
		self.k=k
		self.__validate__()
		#self.set_Dictionary_File("galesNimDic.db")

	#def set_Dictionary_File(self, filename):
	#	self.__filename__=filename
	#def get_Dictionary(self):
		## Try to open the dictionary
	#	try:
	#		self.nim_Values=pickle.load( open( self.__filename__, "rb" ) )
	#	except:
	#		print "Dictionary of values is missing creating a new one."
	#		newDictionary={}



	def __validate__(self):
		'''__validate is designed to take the zeroes out of the piles. Should we 
		keep the zeroes, or keep track of how many zero piles there are.''' 
		newPiles=[x for x in self.piles if x != 0 ]
		self.number_Of_Zero_Piles+=len(self.piles)-len(newPiles)
		self.piles=newPiles

	def find_Nim_Value(self):
		'''A method to find the nim value of the game'''
		pass
		## case 1 if there are only a player can make one pile zero and win.

		## recursive cases

			## dictionary cases

			## start the search

			## add to the dictionary



	def possible_Moves(self):
		ans=set([])
		for i in range(len(self.piles)):
			for j in range(self.piles[i]):
				newPiles=list(self.piles)
				newPiles[i]=j
				ans.add(GalesNim(newPiles, self.number_Of_Zero_Piles,self.k))
		return ans


	def __repr__(self):
		ans="Game ends when all but "+str(self.k)+" are empty.\n"
		for i in range(len(self.piles)):
			ans+=str(self.piles[i])+"  "
		for i in range(self.number_Of_Zero_Piles):
			ans+="0  "
		return ans.strip()

	def __eq__(self, other):
		myPiles=list(self.piles)
		theirPiles=list(other.piles)
		myPiles.sort()
		theirPiles.sort()
		return self.k==other.k and self.number_Of_Zero_Piles==other.number_Of_Zero_Piles and myPiles==theirPiles

def main():
	game=GalesNim([3,4,5],0,1)
	print game
	possMoves=game.possible_Moves()
	for mygame in possMoves:
		print mygame


if __name__ == '__main__':
	main()