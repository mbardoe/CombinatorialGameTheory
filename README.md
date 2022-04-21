# Combinatorial Game Theory
Programs to help compute Nim values for Spoke and Hub Nim, End Nim, Gales Nim, Two Dimensional Toppling Dominoes.

The storage mechanisms require TinyDB. You can download and install it here: https://tinydb.readthedocs.io/en/latest/index.html

The package defaults to TinyDB, but will also uses sqlite3 if available.

## Games supported:

* Impartial Games
    * Nim
    * End-Nim
    * Gale's Nim
    * Spoke and Hub Nim
    * Two Dimensional Toppling Dominoes

* Partizan Games
    * Red-Blue Cherries

## Two Dimensional Toppling Dominoes

Here are the values of L-shaped formations. Then up value is the number of dominoes going up along the L 
and the right is number going to the right. So a up=2 and right=3 looks like 

+
+ + + + 

| row/col | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 |
|---------|----|----|----|----|----|----|----|----|----|----|
| 1       | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |
| 2       | 3  | 4  | 1  | 6  | 7  | 8  | 5  | 10 | 11 | 12 |
| 3       | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 |
| 4       | 5  | 6  | 7  | 8  | 1  | 2  | 3  | 12 | 13 | 14 |
| 5       | 6  | 7  | 8  | 9  | 2  | 3  | 12 | 13 | 14 | 15 |
| 6       | 7  | 8  | 5  | 10 | 3  | 12 | 1  | 14 | 15 | 16 |
| 7       | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| 8       | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 1  | 2  |
| 9       | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 2  | 3  |
| 10      | 11 | 12 | 9  | 14 | 15 | 16 | 13 | 18 | 3  | 4  |## Gale's Nim

You can access Gale's Nim calculations by

```python
from combogames import *
g=GalesNim([3,4,5,8])
g.nim_value
17
```

### Gale's Nim Conjectures
 #### Two Pile games
 
 (Conjecture) The value of a two pile game a b is (a-1)^(b-1)+1
 
 There are no two pile games with value 0.
 
 #### Three pile games with value 0
 1 a a
 
 2 3 4
 
 2 5 6
 
 2 7 8
 
 2 9 10
 
 ....
 
 3 5 7
 
 3 6 8
 
 3 9 11
 
 3 10 12
 
 3 13 15
 
 ...
 
 #### Four Pile games with value 0
 All specific values with a * have NOT been verified by calculations using these programs.
 
 a a b b
 
 1 1 2 3
 
 1 3 5 6
 
 1 1 4 5
 
 Conj: 1 a b c where a^b^c=0 (^ := Nim-sum)
 
 Also
 
 2 3 5 8
 
 2 3 9 12

## Red-Blue Cherries

The game red-blue cherries is a partizan game which is played on a two color
graph. On their turn players can only take nodes of minimum degree in the graph.
The nodes they take should only be of their own color. It was thought that
every game of this type had an integers, switch, or star value, but Scott Herman
discovered games with values that were half integers.

```python
from combogames import *
redblue = RedBlueCherries(6, [(0,1),(1,2),(2,3),(3,4),(4,5),(0,5)],['b','r','b','r','b','b'])
redblue.value
2
```

There are also special classes for RedBlueCycle and RedBluePath.


 
 
 
 
## Dependencies
TinyDB - https://tinydb.readthedocs.io/en/latest/index.html

## References

http://library.msri.org/books/Book63/files/131106-Nowakowski.pdf
