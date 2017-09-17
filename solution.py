assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagon_units = [[rows[i]+cols[i] for i in range(len(rows))],[rows[-1-i]+cols[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diagon_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
def check(values):
    """
        Check if the sudoku is completed
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            blooean: True if the sudoku is solved
    """ 
    s = 0
    for box in unitlist:
        if ''.join(sorted(list(map(lambda a:values[a],box)))) == '123456789':
            s += 1
    return s == 27
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for u in row_units + column_units + square_units:
        unitvalue = [values[b] for b in u]
        for box in u:
            cnt = unitvalue.count(values[box])
            if cnt < 3 and cnt > 1 and unitvalue.count(values[box]) == len(values[box]):
                for key2 in u:
                    if  values[key2] != values[box]:
                        for i in range(len(values[box])):
                             values[key2] = values[key2].replace(values[box][i],'')
    return values
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict(zip(boxes,map(lambda a:a.replace('.','123456789'),list(grid))))
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print('Completed units',check(values))
    return

def eliminate(values):
    """
        Foe each box with only one value, remove that value from all other boxes in the same unit.
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            values(dict): The eliminated sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
        For each unit, if ceratin value can only fit one box, fill it in that box. 
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            values(dict): The filled sudoku in dictionary form
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
        Repeated apply eliminate and reduce_puzzle until no improvement can be made.
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            values(dict): The reduced sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
        Using depth-first search and propagation, create a search tree and solve the sudoku.
        Args:
            values(dict): The sudoku in dictionary form
        Returns:
            values(dict): The solved sudoku in dictionary form
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[k]) == 1 for k in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,box  = min([(len(values[b]),b) for b in boxes if len(values[b])>1])
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for s in values[box]:
        newvalue = values.copy()
        newvalue[box] = s
        newvalue = search(newvalue)
        if newvalue:
            return newvalue
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
