import sys
try:
	from tinydb import TinyDB, Query 
except:
	try:
		import sqlite3 
	except:
		pass
	

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

	def __init__(self, mylist, filename='combinatorialGame.db'):
		'''We init with a list of values for the piles.'''
		self.piles=list(mylist)
		if 'tinydb' in sys.modules:
			self.__filename__=filename
		else:
			self.__filename__=filename[:-3]+"SQL.db"
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
		if 'tinydb' in sys.modules:
			try:
				self.__db__=TinyDB(self.__filename__)
			except:
				print("Get Dictionary. Looks like no database. :-(")
		else:
			try:
				self.__db__ = sqlite3.connect(self.__filename__)
				self.cursor=self.__db__.cursor()
				numTables=self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
				record=numTables.fetchall()
				newRecord=[str(x[0]) for x in record]
				if 'nimValues' not in newRecord:
					self.cursor.execute('''CREATE TABLE nimValues(id text, value int)''')
			except:
				print("Get Dictionary. Looks like no database. :-(")
			finally:
				self.__db__.close()
	def lookup_Value(self):
		if 'tinydb' in sys.modules:
			game_id=self.__db_repr__()
			#print game_id
			try:
				record=Query()
				result=self.__db__.search(record.id==game_id)
				#print result
			except:
				result=[]
			if len(result)>0:
			#print("Found in db.")
				return result[0]['value']
			else:
				return -1 
		else: #sqlite3
			game_id=self.__db_repr__()
			gamelookup={"id":game_id}
			#print gamelookup
			try:
				self.__db__ = sqlite3.connect(self.__filename__)
				#print self.__db__
				self.cursor=self.__db__.cursor()
				query=self.cursor.execute('SELECT value FROM nimValues WHERE id=:id', gamelookup)
				#print query
				self.__db__.commit()
				record = query.fetchone()
				#print record
				result = [record[0]]
				#record=Query()
				#result=self.__db__.search(record.id==game_id)
				#print result
			except:
				result=[]
			finally:
				self.__db__.close()
			if len(result)>0:
				#print("Found in db.")
				return result[0]
			else:
				return -1 

	def __record_value__(self, game_id,ans):
		'''Store values in the database.'''
		#game_id=self.__db_repr__()
		if 'tinydb' in sys.modules:
			try:
				self.__db__.insert({'id': game_id, 'value':ans})
			except:
				pass
		else: #sqlite3
			try: 
				self.__db__ = sqlite3.connect(self.__filename__)
				self.cursor=self.__db__.cursor()
				sqlstring="INSERT INTO nimValues VALUES('"+str(game_id)+"', "+str(ans)+")"
				self.cursor.execute(sqlstring)
				self.__db__.commit()
			except:
				pass
			finally:
				self.__db__.close()

	def __db_repr__(self):
		'''A string representation that will be unique and used as the lookup in the database.'''
		ans=0
		for i in range(len(self.piles)):
			ans+=self.piles[i]*10**i
		return str(ans)

	def find_Nim_Value(self):
		'''Utilize a database of previously constructed values to speed computation.'''
		# look up in db
		game_id=self.__db_repr__()
		result=self.lookup_Value()
		if result>0:
			print("Used database")
			ans=result
		else:

			ans=0
			for i in self.piles:
				ans=ans^i
			self.__record_value__(game_id,ans)
		return ans

	def possible_Moves(self):
		'''Compute all other games that are possible moves from this position.'''
		ans=set([])
		for i in range(len(self.piles)):
			for j in range(self.piles[i]):
				newPiles=list(self.piles)
				newPiles[i]=j
				ans.add(CombinatorialGame(newPiles))
		return ans
	def __tree_search__(self):
		moves=self.possible_Moves()
		values=[i.find_Nim_Value() for i in moves]
		result=mex(values)
		return result
	def __repr__(self):
		'''How the game will be represented in python print statements.'''
		return str(self.__db_repr__())





