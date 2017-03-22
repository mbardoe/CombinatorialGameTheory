class LinearGame(object):
	'''A class that will represent an EndNim Game.
	It has takes in an ordered list [a,b,c,...,z]
	and makes it into a game of the form 
			a--b--c---...---z. 
	Methods:
		possible_Moves - finds the list of possible moves
		nim_Value - finds the nim Value of the position
	'''
	def __init__(self,mylist):
		spot=0
		newlist=list(mylist)
		for value in newlist:
			if value==0:
				newlist.pop(spot)
			spot+=1


		self.values=newlist
		self.nim_Value=-1

	def len(self):
		'''How long is the strand.'''
		return len(self.values)

	def possible_Moves(self):
		'''Creates a list of possible moves from the given game.'''
		ans=[]

		mylist=list(self.values)
		originalFront=mylist[0]
		for i in range(self.values[0]):
			mylist[0]=i
			#print "Test front"+str(mylist)
			ans.append(LinearGame(mylist))
		mylist[0]=originalFront
		for i in range(self.values[-1]):
			mylist[-1]=i
			#print "Test back"+str(mylist)
			ans.append(LinearGame(mylist))
		return ans

	def __repr__(self):
		ans=""
		for i in range(len(self.values)-1):
			ans+=str(self.values[i])
			ans+="---"
		ans+=str(self.values[-1])
		return ans

	def __eq__(self, other):
		return self.values==other.values or self.values.reverse()==other.values

	def find_Nim_Value(self):
		if self.nim_Value>-1:
			return self.nim_Value
		else:
			if self.len()==1:
				self.nim_Value=self.values[0]
		
			elif self.len()==2:
				self.nim_Value=self.values[0]^self.values[1]
				
			#elif self.values[0]==self.values[-1]:
			#	self.nim_Value=0

			else:
				moves=self.possible_Moves()
				values=[i.find_Nim_Value() for i in moves]
				self.nim_Value=mex(values)
			return self.nim_Value


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

def main():
	m=15
	for i in range(10):
		x=LinearGame([1,m,i+1])
		print str(x)+"  "+str(x.find_Nim_Value())



if __name__ == '__main__':
	main()
