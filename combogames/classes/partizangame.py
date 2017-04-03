import sys
from combinatorialgame import CombinatorialGame
try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass

class PartizanGame(CombinatorialGame):
    """A base class for investigating partizan combinatorial games.

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
                if 'values' not in newRecord:
                    sqlstr='CREATE TABLE values(id text, value int)'
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
                query=self.cursor.execute("SELECT value FROM values WHERE id=:id", gamelookup)
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
                sqlstring="INSERT INTO values VALUES('"+str(game_id)+"', "+str(ans)+")"
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
    def value(self):
        """Utilize a database of previously constructed values to speed computation.

        When the database does not have the answer it uses a depth search of other games
        to compute the value of the game.

        Returns:
            Then nim value of the game. If it can't find the value in the database it
            tries to find the value by calculating the nim values of all possible moves
            from the given game.
        """
        # look up in db
        return  None

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A set of the games that are all the possible moves from the given
            game."""

        return {'left':[None], 'right':[None]}

    def __tree_search__(self):
        """A function that does the depth search when we are calculating nim
        values.

        Returns:
            Then nim value of the game, found by calculating the nim values of
            all possible moves.

        """
        moves=self.possible_moves() # return a dictionay with keys 'right' and 'left'
        move_values={}
        move_values['right']=[i.value for i in moves['right']]
        move_values['left']=[i.value for i in moves['left']]
        result=self.simplest_number(move_values)
        return result

    def __repr__(self):
        '''How the game will be represented in python print statements.'''
        return str(self.__db_repr__())

    def simplest_number(self, move_dict):
        #print move_dict
        try:
            right_min=min(move_dict['right'])
        except:
            right_min=None
        try:
            left_max=min(move_dict['left'])
        except:
            left_max=None
        return self.simplest_between(left_max,right_min)

    def simplest_between(self, left,right):
        #print str(left) + ' ' +str(right)
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


