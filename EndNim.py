from combinatorialgametools import mex, CombinatorialGame

try:
	from tinydb import TinyDB, Query 
except:
	pass

class EndNim(CombinatorialGame):
	'''A class that will represent an EndNim Game.
	It has takes in an ordered list [a,b,c,...,z]
	and makes it into a game of the form 
			a--b--c---...---z. 
	Methods:
		possible_Moves - finds the list of possible moves
		find_Nim_Value - finds the nim Value of the position
	'''
	def __init__(self,mylist):
		self.piles=mylist
		self.__validate__()
		self.__filename__="endNim.db"
		self.__get_dictionary__()
		
		
	def __validate__(self):
		newlist=[x for x in self.piles if x!=0]
		self.piles=newlist

	def len(self):
		'''How long is the strand.'''
		return len(self.piles)

	def possible_Moves(self):
		'''Creates a list of possible moves from the given game.'''
		ans=set([])

		mylist=list(self.piles)
		originalFront=mylist[0]
		for i in range(self.piles[0]):
			mylist[0]=i
			#print "Test front"+str(mylist)
			ans.add(EndNim(mylist))
		mylist[0]=originalFront
		for i in range(self.piles[-1]):
			mylist[-1]=i
			#print "Test back"+str(mylist)
			ans.add(EndNim(mylist))
		return ans

	def __repr__(self):
		ans=""
		for i in range(len(self.piles)-1):
			ans+=str(self.piles[i])
			ans+="---"
		ans+=str(self.piles[-1])
		return ans

	def __db_rep__(self):
		if self.piles[0]>self.piles[-1]:
			self.piles.reverse()
		return self.__repr__()

	def __eq__(self, other):
		return self.piles==other.values or self.piles.reverse()==other.values

	def find_Nim_Value(self):
		result=self.lookup_Value()
		if result<0:
			if self.len()==1:
				result=self.piles[0]
		
			elif self.len()==2:
				result=self.piles[0]^self.piles[1]
				
			else:
				moves=self.possible_Moves()
				values=[i.find_Nim_Value() for i in moves]
				result=mex(values)
			self.__record_value__(self.__db_rep__(),result)
		return result


def main():
	m=15
	for i in range(10):
		x=EndNim([1,m,i+1])
		print str(x)+"  "+str(x.find_Nim_Value())



if __name__ == '__main__':
	main()
