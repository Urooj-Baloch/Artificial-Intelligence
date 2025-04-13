
def print_sudoku(grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] != 0 else ".", end=" ")
        print()

def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range(9)]:
        return False

    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[box_row + i][box_col + j] == num:
                return False

    return True

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def ac3(grid, domains):
    queue = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for k in range(9):
                    if k != j and grid[i][k] == 0:
                        queue.append(((i, j), (i, k)))
                    if k != i and grid[k][j] == 0:
                        queue.append(((i, j), (k, j)))

                box_row, box_col = i // 3 * 3, j // 3 * 3
                for x in range(3):
                    for y in range(3):
                        ni, nj = box_row + x, box_col + y
                        if (ni, nj) != (i, j) and grid[ni][nj] == 0:
                            queue.append(((i, j), (ni, nj)))

    while queue:
        (xi, xj), (yi, yj) = queue.pop(0)
        if revise(grid, domains, (xi, xj), (yi, yj)):
            if not domains[(xi, xj)]:
                return False
            for k in range(9):
                if k != xj and grid[xi][k] == 0 and (xi, k) != (yi, yj):
                    queue.append(((xi, k), (xi, xj)))
                if k != xi and grid[k][xj] == 0 and (k, xj) != (yi, yj):
                    queue.append(((k, xj), (xi, xj)))

            box_row, box_col = xi // 3 * 3, xj // 3 * 3
            for x in range(3):
                for y in range(3):
                    ni, nj = box_row + x, box_col + y
                    if (ni, nj) != (xi, xj) and (ni, nj) != (yi, yj) and grid[ni][nj] == 0:
                        queue.append(((ni, nj), (xi, xj)))

    return True


def revise(grid, domains, cell1, cell2):
    revised = False
    for num1 in domains[cell1]:
        if not any(num2 == num1 for num2 in domains[cell2]):
            domains[cell1].remove(num1)

def backtrack_with_ac3(grid, domains):
    cell = find_empty_cell(grid)
    if not cell:
        return True
    row, col = cell

    for num in domains[(row, col)]:
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            old_domains = {k: v[:] for k, v in domains.items()}

            domains[(row, col)] = [num]

            if ac3(grid, domains):
                if backtrack_with_ac3(grid, domains):
                    return True

            grid[row][col] = 0
            domains = old_domains

    return False

def solve_sudoku(grid):
    domains = {}
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domains[(i, j)] = [num for num in range(1, 10) if is_valid(grid, i, j, num)]
            else:
                domains[(i, j)] = [grid[i][j]]

    ac3(grid, domains)
    if backtrack_with_ac3(grid, domains):
        return grid
    else:
        return None

puzzle = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

print("Initial puzzle:")
print_sudoku(puzzle)

solution = solve_sudoku(puzzle)

if solution:
    print("\nSolution:")
    print_sudoku(solution)
else:
    print("No solution exists")