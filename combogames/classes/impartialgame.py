import sys
from combinatorialgame import CombinatorialGame
try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class ImpartialGame(CombinatorialGame):
    """A base class for impartial games. Currently sets up the database, but
    we should move this functionality back to CombinatorialGame. Includes
    calculation tools like mex function to make nim calculation easier.
    """

    def __get_dictionary__(self):
        """Set up the database file for this game. The path is stored
        as __filename__.
        """
        if 'tinydb' in sys.modules:
            #print "tinyDB"
            #print self.__filename__
            try:
                self.__db__=TinyDB(self.__filename__)
                #print "Made a db"
            except:
                print("Get Dictionary. Looks like no database. :-(")
        else:
            try:
                #print "filename: "+self.__filename__
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

        Returns:
            int: The value of the game that is list in the database or -1 if it
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
            game_id (str): is a string that can be used to uniquely identify each game.
            ans (int): is an integer that represents its the nim value of the game.
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


    @property
    def nim_value(self):
        """Utilize a database of previously constructed values to speed computation.

        When the database does not have the answer it uses a depth search of other games
        to compute the value of the game.

        Returns:
            int: Then nim value of the game. If it can't find the value in the database it
                tries to find the value by calculating the nim values of all possible moves
                from the given game.
        """
        # look up in db
        return  -1

    def __tree_search__(self):
        """A function that does the depth search when we are calculating nim
        values.

        Returns:
            int: Then nim value of the game, found by calculating the nim values of
                all possible moves.

        """
        moves=self.possible_moves()
        values=[i.nim_value for i in moves]
        result=self.mex(values)
        return result

    def mex(self, mylist):
        """mex computes the smallest positive integer that is missing from a list.

        mex is essential to calculations with impartial games. By finding the
        smallest excluded value it is possible to find the equivalent nim stack.

        Args:
            mylist (list): a list of of values of positive integers

        Returns:
            int: the smallest positive integer that is missing from the
                list

        Raises:
            ValueError: If the list is not all positive integers.
            TypeError: if you don't give it a list of integers
        """
        current=0
        mylist=list(mylist)
        mylist=sorted(mylist)
        mylist=[int(i) for i in mylist] # this helps sage do its thing
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



