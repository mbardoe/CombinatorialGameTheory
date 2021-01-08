import math

def mex(mylist):
    """mex computes the smallest positive integer that is missing from a list.

    mex is essential to calculations with impartial games. By finding the
    smallest excluded value it is possible to find the equivalent nim stack.

    Args:

        mylist (list): a list of of values of positive integers

    Returns:

        int: the smallest positive integer that is missing from the
                list

    Raises:

        ValueError or TypeError if you don't give it a list of
                positive integers
    """
    current = 0
    mylist = list(mylist)
    mylist = sorted(mylist)
    #print str(mylist)
    for i in range(len(mylist)):
        if not isinstance(mylist[i], int):
            raise TypeError("Has to be a list of integers.")
        if mylist[i] < 0:
            raise ValueError("Must be all positive integers.")
        if mylist[i] == current:
            current += 1
        if mylist[i] > current:
            return current

            #print "step"+str(i)+" "+str(current)
    return current


def simplest_number(move_dict):
    """A function that finds the simplest number between the left game
        values and the right game values.

        Args:

            move_dict (dict): A dictionary that contains a list of moves for
                'right' and moves for 'left'

        Returns:

            int: Value of the game.

    """
    print(move_dict)
    try:
        right_min = min(move_dict['right'])
    except:
        right_min = None
    try:
        left_max = min(move_dict['left'])
    except:
        left_max = None
    return simplest_between(left_max, right_min)


def simplest_between(left, right):
    """Calculates the simplest number between two given numbers. Implementing the algorithm from Max Fan.

        Args:
            left (float): an integer that is smaller than right, Can also be
                None.
            right(float): an integer that is larger than left. Can also be
                None.

     """
    positive_difference = right - left

    if 0 > left and 0 < right:
        return 0.0

    power = 0
    while pow(2, power) <= 1 / (positive_difference):
        power += 1

    if abs(right) > abs(left):
        number = math.floor(left)
        while number <= left:
            number += 1 / pow(2, power)

    elif abs(right) < abs(left):
        number = math.ceil(right)
        while number >= right:
            number -= 1 / pow(2, power)

    else:
        raise ValueError

    return float(number)


def main():
    """
    :return None

    """
    print('3 and 8 ' + str(simplest_between(3, 8)))
    print('3 and 4 ' + str(simplest_between(3, 4)))
    print('0 and 1.5 ' + str(simplest_between(0, 1.5)))
    print('-9 and 4 ' + str(simplest_between(-9, 4)))
    print('-7 and -2 ' + str(simplest_between(-7, -2)))
    print('-2.25 and -2 ' + str(simplest_between(-2.25, -2)))


if __name__ == '__main__':
    main()
