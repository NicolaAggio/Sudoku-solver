import copy
from utils import checkCostraints, getAllDomains, getMostConstrainedCell, DIMENSION

def solve_cp(board, back):
    # retrieves all the domains of the cells
    domains = getAllDomains(board)

    # gets the position of the most constrained cell 
    cell = getMostConstrainedCell(domains, board)
    if cell is None:
        return (True, board, back)
    row, col = cell
    pos = row * DIMENSION + col

    # for each value in the cell's domain
    for val in domains[pos]:

        # if the assignment of the value is consistent with the constraint
        if checkCostraints(val, row, col, copy.deepcopy(board)):

            # board update
            board[row][col] = val

            # recursive call on the the new board
            solved, bo, backpropagation = solve_cp(board, back)

            # if a solution is found, the state is correct
            if solved:
                return (True, bo, back + backpropagation)

        # otherwise, we check another value
        board[row][col] = 0
        back += 1
    
    # if no solution is found
    return (False, board, back)