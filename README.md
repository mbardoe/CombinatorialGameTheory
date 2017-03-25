# Combinatorial Game Theory
Programs to help compute Nim values for Spoke and Hub Nim, End Nim and Gales Nim.

The storage mechanisms require TinyDB. You can download and install it here: https://tinydb.readthedocs.io/en/latest/index.html

## Gale's Nim

### Gale's Nim positions with value 0
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
 2 7 9 12
 2 11 13 14 *
 
 
## Dependencies
TinyDB - https://tinydb.readthedocs.io/en/latest/index.html

## References

http://library.msri.org/books/Book63/files/131106-Nowakowski.pdf
