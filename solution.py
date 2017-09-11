# Encoding the board
## Board is encoded in two ways - String and Dictionary

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

# Creates a list of all the Sudoku cells based on the decided naming convention A1-I9
boxes  = cross(rows, cols)

# Create a list of all the row units
row_units = [cross(rows,c) for c in cols]
# Create a list of all the column units
col_units = [cross(r,cols) for r in rows]

# Create a list of all the square units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Create a list of the two diagonal units
diagonal_units = [[rows[i]+cols[i] for i in range(9)]]
diagonal_units.append([rows[i]+cols[8-i] for i in range(9)])


unitlist = row_units + col_units + square_units + diagonal_units

# Create a dictionary which has key = Cell and Value = [row_unit,col_unit,square_unit] that it belongs to
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# Create a dictionary which has key= Cell and Value = Peers ( all the other cells in the same unit)
peers = dict((s, set(sum(units[s],[]))-set([s]))  for s in boxes)

assignments = []

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
    for unit in unitlist:
        two_places = [box for box in unit if len(values[box]) == 2]
        # Cut short if there are less than two elements with only 2 values
        if(len(two_places) < 2):
            continue
    # Eliminate the naked twins as possibilities for their peers
        for elem in two_places:
            naked_twin = [twin for twin in two_places if values[twin] == values[elem]]
            if(len(naked_twin) == 2):
                # you have found naked twins
                    for box in unit:
                        # Do not edit the digits of the naked twins
                        if(box == naked_twin[1] or box == naked_twin[0]):
                            continue
                        for digit in values[naked_twin[0]]:
                            new_value = values[box].replace(digit, '')
                            assign_value(values, box, new_value)
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    assert(len(grid)==81)
    sudoku = {}
    for i in range(81):
        if(grid[i]=='.'):
            sudoku[boxes[i]] = digits
        else:
            sudoku[boxes[i]] = grid[i]
    return sudoku

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # A list of all the Cells which have already been solved
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        # Remove the cells value from the list of possible values in all the peers
        for peer in peers[box]:
            new_value = values[peer].replace(digit,'')
            assign_value(values,peer,new_value)
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # Check in each row, column and square unit
    for unit in unitlist:
        # Check how many occurences there are of each digit in the unit
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            # If a digit occurs only once - that is the only place where it can be placed in that unit
            if len(dplaces) == 1:
                assign_value(values, dplaces[0],digit)
    return values


def reduce_puzzle(values):
    stalled = False
    count = 0
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)

        values = only_choice(values)

        values = naked_twins(values)

        count +=1

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    #print("The number of iterations is:", count)
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    if not values:
        print("Could not find a solution")
        return False
    else:
        return values


before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}


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
