
def is_sudoku(l):
    T=list(map(list, zip(*l)))
    for i in range(9):
        if sorted(l[i]) != list(range(1, 10)):
            return False
        if sorted(T[i]) != list(range(1, 10)):
            return False
    return True           


"""
A = [
 [4,3,5,2,6,9,7,8,1],
 [6,8,2,5,7,1,4,9,3],
 [1,9,7,8,3,4,5,6,2],
 [8,2,6,1,9,5,3,4,7],
 [3,7,4,6,8,2,9,1,5],
 [9,5,1,7,4,3,6,2,8],
 [5,1,9,3,2,6,8,7,4],
 [2,4,8,9,5,7,1,3,6], 
 [7,6,3,4,1,8,2,5,9],
]
print(is_sudoku(A))

B = [
 [4,3,5,2,6,9,7,8,1],
 [6,8,2,5,7,1,4,9,3],
 [1,9,7,8,3,4,5,6,2],
 [8,2,6,1,9,5,3,4,7],
 [3,7,4,6,8,2,9,1,5],
 [9,5,1,7,4,3,6,2,8],
 [5,1,9,3,2,6,8,7,4],
 [2,4,8,9,5,7,1,3,6], 
 [7,6,3,4,1,8,2,5,0],
] # not a Sudoku; the last element is 0
print(is_sudoku(B))

B = [
 [4,3,5,2,6,9,7,8,1],
 [6,8,2,5,7,1,4,9,3],
 [1,9,7,8,3,4,5,6,2],
 [8,2,6,1,9,5,3,4,7],
 [3,7,4,6,8,2,9,1,5],
 [9,5,1,7,4,3,6,2,8],
 [5,1,9,3,2,6,8,7,4],
 [2,4,8,9,5,7,1,3,6], 
 [7,6,3,4,1,8,2,5,0],
] # not a Sudoku; the last element is 0
print(is_sudoku(B))

"""




    