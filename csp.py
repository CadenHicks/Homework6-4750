import time

class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.assignments = []

    def is_valid_assignment(self, row, col, num):
        """check if its valid to place num at specified position"""
        for x in range(9):
            if self.grid[row][x] == num: # row check
                return False
            if self.grid[x][col] == num: # col check
                return False
        # box check
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + startRow][j + startCol] == num:
                    return False
        return True

    def find_empty_location(self):
        """find an empty location in the grid, None on error"""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def mrv_heuristic(self):
        """Use MRV heuristic to find the next empty location, considering degree, position for tie-breaking."""
        min_domain_size = float('inf')
        max_degree = -1  # For tie-breaking
        min_domain_row, min_domain_col = -1, -1
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    # determine domain size, the MRV heuristic
                    domain_size = sum([self.is_valid_assignment(i, j, num) for num in range(1, 10)])
                    degree = self.degree_heuristic(i, j) # fetch degree
                    # determine if this is the best variable so far
                    if domain_size < min_domain_size or (domain_size == min_domain_size and degree > max_degree):
                        min_domain_size = domain_size
                        max_degree = degree
                        min_domain_row, min_domain_col = i, j
        # If no valid variable found, solution does not exist
        if min_domain_row == -1:
            return None, None
        return min_domain_row, min_domain_col

    def degree_heuristic(self, row, col):
        """Return the degree of a variable (number of constraints it is involved in)."""
        count = 0
        # Count non-assigned cells in the same row
        count += sum([1 for x in range(9) if self.grid[row][x] == 0 and x != col])
        # Count non-assigned cells in the same column
        count += sum([1 for x in range(9) if self.grid[x][col] == 0 and x != row])
        # Count non-assigned cells in the same 3x3 box
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + startRow][j + startCol] == 0 and (i + startRow != row or j + startCol != col):
                    count += 1
        return count

    def solve(self):
        """solve the sudoku using backtracking and forward checking"""
        if not self.find_empty_location():
            return True # done, grid full
        row, col = self.mrv_heuristic()
        # if no valid variable found, solution does not exist
        if row is None:
            return False
        # Calculate the domain (valid numbers) for the cell, its size, and the degree
        valid_numbers = [num for num in range(1, 10) if self.is_valid_assignment(row, col, num)]
        domain_size = len(valid_numbers)
        degree = self.degree_heuristic(row, col)
        for num in valid_numbers:
            if self.is_valid_assignment(row, col, num):
                self.grid[row][col] = num # assign num
                # record assignment
                self.assignments.append((row, col, domain_size, degree, num, valid_numbers))
                if self.solve(): # recur to place next number
                    return True
                # backtrack if there's no solution
                self.grid[row][col] = 0
                self.assignments.pop()
        return False

# problem instance strings
grids_text = [
    "001002000005006030460005000000104000600800143000090508800049050100320000009000300",
    "005010000002004030109000206200030000040000700500007001000603000060100000000070050",
    "670000000025000000090560200300080900000000801000470000008600090000000010106050070"
]

# convert raw strings to grid representations for sudoku instances
grids = [ [ [int(ch) for ch in list(grid_text[i:i+9])] for i in range(0, 81, 9) ] for grid_text in grids_text ]

# solve instances and display results
results = []
for grid in grids:
    sudoku = Sudoku(grid.copy())
    start_time = time.time()
    sudoku.solve()
    end_time = time.time()
    execution_time = end_time - start_time
    results.append((sudoku.grid, sudoku.assignments[:4], execution_time))

# print out results in a nice format
for i, result in enumerate(results):
    grid, assignments, execution_time = result
    print("Sudoku instance %d:" % (i + 1))
    print("Execution time: %.3f seconds" % execution_time)
    print("First 4 Variable-Value Assignments:")
    for assignment in assignments:
        row, col, domain_size, degree, num, domain = assignment
        print("Variable: (%d, %d), Domain size: %d, Degree: %d, Assigned Value: %d" % (row, col, domain_size, degree, num))
    print("Solution:")
    for row in grid:
        print(row)
    print()