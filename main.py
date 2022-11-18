import time
import csv
from costraint_propagation import solve_cp
from simulated_annealing import solve_sa
from utils import createBoard, checkSolution, writeBoard, printBoard

l = ["easy", "medium", "normal", "hard"]
i = 1
cp_results = []
sa_results = []

# for item in l:
#     board_collection = []
#     for i in range(1, 6):
#         file = f"boards/{item}/{item + str(i)}.txt"
#         board_collection.append(createBoard(file))
#     i = 1
#     for board in board_collection:
#         start_time = time.time()
#         solved, board, back = solve_cp(board, 0)
#         execution_time = time.time() - start_time
#         if solved and checkSolution(board):
#             writeBoard("cp", f"{item + str(i)}.txt", board)
#             cp_results.append((solved,f"{item + str(i)}.txt", execution_time, back))
#             i += 1
#         else:
#             print("SUDOKU NON RISOLTO_BACKPROPAGATION")

for item in l:
    board_collection = []
    for i in range(1, 6):
        file = f"boards/{item}/{item + str(i)}.txt"
        board_collection.append(createBoard(file))
    i = 1
    for board in board_collection:
        start_time = time.time()
        res = solve_sa(board)
        execution_time = time.time() - start_time
        if res:
            solved = res[0]
            iterations = res[1]
            if solved and checkSolution(board):
                writeBoard("annealing", f"{item + str(i)}.txt", board)
                sa_results.append((solved,f"{item + str(i)}.txt", execution_time, iterations))
                i += 1
            else:
                if solved:
                    print("SUDOKU RISOLTO IN MANIERA ERRATA_SIMULATED ANNEALING")
                    printBoard(board)
                else:
                    print("Sudoku non risolto!")
        else:
            print("SUDOKU NON RISOLTO_SIMULATED ANNEALING")            

# header = ['solved','filename', 'execution_time', 'backpropagation']
# with open('./results/cp/results.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)
#     for elem in cp_results:
#         writer.writerow(elem)