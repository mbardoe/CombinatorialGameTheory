import sys
try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


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

class CombinatorialGame(object):
    """A base class for investigating impartial combinatorial games.

    One goal of this class is create methods that allow for back searches
    of previously computed games. This class can utilize either tinyDB or
    sqlite3 to record the values of games that have been computed. The goal
    is to make the computation of larger games much faster. This particular
    base class is really a standard nim game.
    """

    def __init__(self, **kwargs):
        #def __init__(self, myfilename):
        """
        Args:
            mylist: the list of piles sizes for the game
            filename: the path for the database file. To be saved in
            __filename__.
        """
        #self.piles=list(mylist)

        if 'filename' in kwargs.keys():
            self.__filename__=kwargs['filename']
        else:
            raise SyntaxError('Need at least a filename argument')


        if 'tinydb' not in sys.modules:
            self.__filename__=self.__filename__[:-3]+"SQL.db"
        #self.__validate__()
        self.__get_dictionary__()

    def __validate__(self):
        """This is make sure the form of the input is valid for this game.

        It also makes sure that the piles in a specific order.
        """
        pass

    def __get_dictionary__(self):
        """Set up the database file for this game. The path is stored
        as __filename__.
        """
        if 'tinydb' in sys.modules:
            try:
                self.__db__=TinyDB(self.__filename__)
                #print "Made a db"
            except:
                print("Get Dictionary. Looks like no database. :-(")
        else:
            try:
                self.__db__ = sqlite3.connect(self.__filename__)
                self.cursor=self.__db__.cursor()
                numTables=self.cursor.execute('''SELECT name FROM
                    sqlite_master WHERE type='table' ''')
                record=numTables.fetchall()
                newRecord=[str(x[0]) for x in record]
                if 'nimValues' not in newRecord:
                    sqlstr='CREATE TABLE nimValues(id text, value int)'
                    self.cursor.execute(sqlstr)
            except:
                print("Get Dictionary. Looks like no database. :-(")
            finally:
                self.__db__.close()
    def lookup_value(self):
        """Looks up the value of a previously computed game.

        If the game has not been computed already, then the function returns
        -1.

        :rtype : int
        Returns:
            The value of the game that is list in the database or -1 if it
            can't be found in the database.

        """
        if 'tinydb' in sys.modules:
            #print 'tinydb lookup'
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
                query=self.cursor.execute("SELECT value FROM nimValues WHERE id=:id", gamelookup)
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

    def __record_value__(self, game_id, ans):
        """Store values in the database.

        Args:
            game_id: is a string that can be used to uniquely identify each game.
            ans: is an integer that represents its the nim value of the game.
        """
        #game_id=self.__db_repr__()
        if 'tinydb' in sys.modules:
            #try:
            self.__db__.insert({'id': game_id, 'value':ans})
            #except Exception:
            #    print Exception
            #   pass
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
        """A string representation that will be unique and used as the lookup in the database.
        Returns:
            A unique string that identifies the game as an identification in the database
        """
        pass

    @property
    def nim_value(self):
        """Utilize a database of previously constructed values to speed computation.

        When the database does not have the answer it uses a depth search of other games
        to compute the value of the game.

        Returns:
            Then nim value of the game. If it can't find the value in the database it
            tries to find the value by calculating the nim values of all possible moves
            from the given game.
        """
        # look up in db
        return  -1

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A set of the games that are all the possible moves from the given
            game."""

        return set([])

    def __tree_search__(self):
        """A function that does the depth search when we are calculating nim
        values.

        Returns:
            Then nim value of the game, found by calculating the nim values of
            all possible moves.

        """
        moves=self.possible_moves()
        values=[i.nim_value for i in moves]
        result=mex(values)
        return result

    def __repr__(self):
        '''How the game will be represented in python print statements.'''
        return str(self.__db_repr__())

    def find_move_with_value(self, n):
        """Look at the possible moves of this move, and find a move that has value
        equal to n.
        Args:
            n: is the nim value we are interested in finding a move from the
                current game.
        Returns:
            A game of the that has the given value.
        """
        if n < self.nim_value:

            moves=self.possible_moves()
            for move in moves:
                if move.nim_value == n:
                    assert isinstance(move, CombinatorialGame)
                    return move
        else:
            return None




