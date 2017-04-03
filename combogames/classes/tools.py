
def mex(mylist):
    """mex computes the smallest positive integer that is missing from a list.

    mex is essential to calculations with impartial games. By finding the
    smallest excluded value it is possible to find the equivalent nim stack.

    :list mylist: a list of of values of positive integers
    :returns: int the smallest positive integer that is missing from the
                    list
    :raises: ValueError or TypeError if you don't give it a list of
                positive integers
    """
    current=0
    mylist=list(mylist)
    mylist=sorted(mylist)
    #print str(mylist)
    for i in range(len(mylist)):
        if not isinstance(mylist[i],int):
            raise TypeError("Has to be a list of integers.")
        if mylist[i]<0:
            raise ValueError("Must be all positive integers.")
        if mylist[i]==current:
            current+=1
        if mylist[i]>current:
            return current

        #print "step"+str(i)+" "+str(current)
    return current

def simplest_number(move_dict):
    print move_dict
    try:
        right_min=min(move_dict['right'])
    except:
        right_min=None
    try:
        left_max=min(move_dict['left'])
    except:
        left_max=None
    return simplest_between(left_max,right_min)

def simplest_between(left,right):
    print str(left) + ' ' +str(right)
    if left is None:
        if right is None:
            return 0
        if right<=0:
            return int(right)-1
        else:
            return 0
    if right is None:
        if left >= 0:
            return int(left)+1
        else:
            return 0
    if left<0 and right>0:
        return 0

    if right<0:
        right,left=-1*left,-1*right
        sign=-1
    else:
        sign=1


    if int(right)-int(left)>1:
        return sign*(int(left)+1)
    else:
        current=1
        power=2**(-current)
        guess =int(left)+power
        while (left>=guess) or (right<=guess):
            #print guess
            if int(guess+power)>=int(right):
                current+=1
                power=2**(-current)
                guess = int(left)+power
            else:
                guess = guess+power
        return sign * guess






def main():
    """
    :return None

    """
    print('3 and 8 '+ str(simplest_between(3,8)))
    print('3 and 4 '+ str(simplest_between(3,4)))
    print('2 and 2.25 '+ str(simplest_between(2,2.25)))
    print('-9 and 4 '+ str(simplest_between(-9,4)))
    print('-7 and -2 '+ str(simplest_between(-7,-2)))
    print('-2.25 and -2 '+ str(simplest_between(-2.25,-2)))



if __name__ == '__main__':
    main()