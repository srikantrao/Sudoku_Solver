# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The problem can be broken down into identification of naked twins in a (row, column, square or diagonal) unit, followed by the enforcing the constraint on the values of the other elements in the unit.

Identification of Naked twins -
```Python
# Find all instances of naked twins
    for unit in unitlist:
        two_places = [box for box in unit if len(values[box]) == 2]
        # Cut short if there are less than two elements with only 2 values
        if(len(two_places) < 2):
            continue
            for elem in two_places:
                naked_twin = [twin for twin in two_places if values[twin] == values[elem]]
                if(len(naked_twin) == 2): # you have found naked twins
```

Application of Constraints imposed by the values of the naked twins

```Python
# Eliminate the naked twins as possibilities for their peers
                    # Remove the values from other cells in the unit
                    for box in unit:
                        # Do not edit the digits of the naked twins
                        if(box == naked_twin[1] or box == naked_twin[0]):
                            continue
                        # Use assign_values to update values
                        for digit in values[naked_twin[0]]:
                            new_value = values[box].replace(digit, '')
                            assign_value(values, box, new_value)
    return values
```

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The constraints have been applied in the form of units (row, column, square). To add diagonal constraints, the diagonal units need to be added to the unit list and these will alter the peers for the corresponding diagonal elements.

These additional constraints can be addded by adding the two diagonal units  to the unit list as shown below -

```Python
# Create a list of the two diagonal units
diagonal_units = [[rows[i]+cols[i] for i in range(9)]]
diagonal_units.append([rows[i]+cols[8-i] for i in range(9)])
```
These are then added to the rest of the units -

```Python
# Create the unit list
unitlist = row_units + col_units + square_units + diagonal_units
```

# Final Result

All three test cases passed for the naked twins and the diagonal sudoku.

![Completed Sudoku](images/completed_sudoku_1.png?raw=true "Completed Sudoku")

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
