from tinydb import TinyDB, Query 

def mex(mylist):
	current=0
	mylist=sorted(mylist)
	#print str(mylist)
	for i in range(len(mylist)):
		if mylist[i]==current:
			current+=1
		if mylist[i]>current:
			return current
		#print "step"+str(i)+" "+str(current)
	return current

class CombinatorialGame(object):

	def __init__(self, mylist):
		'''We init with a list of values for the piles.'''
		self.piles=list(mylist)
		self.__filename__='combinatorialGame.db'
		self.__validate__()
		self.__get_dictionary__()

	def __validate__(self):
		'''This is make sure the form of the input is valid for this game.'''
		## remove zeros from piles
		new_Piles=[x for x in self.piles if x!=0]
		new_Piles.sort()
		#print new_Piles
		self.piles=list(new_Piles)


	#def __set_up_dictionary__(self, filename):
	#	pass

	def __get_dictionary__(self):
		'''Set up the database file for this game. The path is stored as __filename__.'''
		self.__db__=TinyDB(self.__filename__)

	def find_Nim_Value(self):
		'''Utilize a database of previously constructed values to speed computation.'''
		# look up in db
		game_id=self.__db_rep__()
		record=Query()
		result=self.__db__.search(record.id==game_id)
		if len(result)>0:
			#print("Used database")
			ans=result[0]['value']
		else:

			ans=0
			for i in self.piles:
				ans=ans^i
			self.__record_value__(game_id,ans)
		return ans
	
	def __record_value__(self, game_id,ans):
		'''Store values in the database.'''
		game_id=self.__db_rep__()
		self.__db__.insert({'id': game_id, 'value':ans})


	def possible_Moves(self):
		'''Compute all other games that are possible moves from this position.'''
		ans=set([])
		for i in range(len(self.piles)):
			for j in range(self.piles[i]):
				newPiles=list(self.piles)
				newPiles[i]=j
				ans.add(CombinatorialGame(newPiles))
		return ans

	def __db_rep__(self):
		'''A representation that will be unique and used as the lookup in the database.'''
		ans=0
		for i in range(len(self.piles)):
			ans+=self.piles[i]*10**i
		return ans

	def __repr__(self):
		'''How the game will be represented in python print statements.'''
		return str(self.__db_rep__())





