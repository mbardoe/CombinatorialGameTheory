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