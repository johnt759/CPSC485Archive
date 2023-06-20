# Edit Distance Program by John Tu
# CWID: 7462
#
# How to run the program on Windows/Mac/Linux:
# Open this file in any program that can run Python
# and execute this source code.
# OR
# Open Command Prompt/Terminal and type the following command line:
# python edit_dist.py [first_word] [second_word] (Windows)
# python3 edit_dist.py [first_word] [second_word] (Mac/Linux)

import sys # Needed to run Python via command lines
import time

def edit_distance(first, second):
    # Initialize the final edit distance to zero.
    final_dist = 0
    
    # Convert the words into lowercases if necessary.
    first = first.lower()
    second = second.lower()

    # Get the lengths of the two words.
    len_first = len(first)
    len_second = len(second)

    # Print out the length of the words.
    print("Length of first word: ", len_first)
    print("Length of second word: ", len_second)

    # If one word appears to be empty, then simply
    # return the length of the other word.
    # If both words are empty, then return zero.
    if (len_first == 0):
        final_dist = len_second
        print("Edit distance is ", final_dist)
        return
    elif (len_second == 0):
        final_dist = len_first
        print("Edit distance is ", final_dist)
        return
    elif (len_first == 0 and len_second == 0):
        print("Edit distance is ", final_dist)
        return

    # If two words are non-empty, set up a table of the two words.
    # First, assign the number of rows and columns.
    # Let the columns be length of the first word and the rows
    # be the length of the second word.
    col = len_first + 1
    row = len_second + 1

    # Create a table and populate all entries with zeroes.
    table = [[0 for y in range(col)] for x in range(row)]

    # Now fill in all the entries of the table.
    #
    # Here is how the edit distance algorithm works:
    # If x or y is zero, treat it as the outermost row or column and
    # simply add 1 due to insertion for empty character.
    # If the characters are the same, then get count from top-left entry.
    # If the characters are different, then take the minimum of the
    # top-left, top, and left entry of the table, and then add 1.
    # Top-left entry is table[x-1][y-1].
    # Top entry is table[x][y-1].
    # Left entry is table[x-1][y].
    for x in range(0, row):
        for y in range(0, col):
            if x == 0:
                table[x][y] = y
            elif y == 0:
                table[x][y] = x
            else:
                top_entry = table[x][y-1]
                left_entry = table[x-1][y]
                top_left_entry = table[x-1][y-1]
                if second[x-1] == first[y-1]:
                    table[x][y] = top_left_entry
                else:
                    table[x][y] = 1 + min(top_entry, left_entry, top_left_entry)

    # Use the bottom-right entry of the table as the final distance.
    final_dist = table[row-1][col-1]

    # Print out the edit distance between two words.
    print("Edit distance is ", final_dist)

    # Now create the final matrix for the edit distance results obtained above.
    # Create another table and initialize all the entries to whitespace.
    # Next, convert all of the values from table into strings.
    final_table = [["  " for y in range(col)] for x in range(row)]

    # Now obtain all of the values from table into final_table
    # and convert the numbers into strings.
    for x in range(0, row):
        for y in range(0, col):
            # Add a space for values less than 10 for consistent appearance.
            if table[x][y] < 10:
                final_table[x][y] = str(table[x][y]) + " "
            else:
                final_table[x][y] = str(table[x][y])

    # Print out the table and the alignment only if two words have equal lengths.
    if len_first == len_second:
        for i in range(col):
            print(final_table[i])
        print()
        print("Alignment of two words:")
        print(first)
        print(second)
        return
    else:
        for i in range(row):
            print(final_table[i])
    
    # Find the alignment between the two words if the lengths are unequal.
    # In case that the current pointer ends up at the bottom-most row or
    # the right-most column, the only valid direction is move right to the
    # next column if at bottom-most row or move down to the next row if at
    # the right-most column.

    # Create a matrix that will be the traceback path for the two words.
    traceback = [[0 for y in range(col)] for x in range(row)]
    first_align, second_align = "", ""

    loc_col, loc_row = col-1, row-1
    min_value = 0

    # Start at the bottom-right element in the traceback table.
    traceback[row-1][col-1] = table[row-1][col-1]

    # Now do the same process as generating the edit distance table,
    # except working backwards to the top-left element.
    while True:
        print("Current position: ", (loc_row, loc_col))
        if (loc_col == 0 and loc_row == 0):
            break
        elif loc_col == 0:
            traceback[loc_row][loc_col] = table[loc_row][loc_col]
            loc_row -= 1
        elif loc_row == 0:
            traceback[loc_row][loc_col] = table[loc_row][loc_col]
            loc_col -= 1
        else:
            left = table[loc_row][loc_col-1]
            top = table[loc_row-1][loc_col]
            top_left = table[loc_row-1][loc_col-1]
            print("(Left, Top, Top-Left): ", (left, top, top_left))
            min_value = min(left, top, top_left)
            if min_value == top_left:
                traceback[loc_row][loc_col] = min_value
                loc_row -= 1
                loc_col -= 1
            elif min_value == top:
                traceback[loc_row][loc_col] = min_value
                loc_row -= 1
            elif min_value == left:
                traceback[loc_row][loc_col] = min_value
                loc_col -= 1
        time.sleep(2.5)

    # Print out the completed traceback table.
    for i in range(row):
        print(traceback[i])

    # Begin aligning the words by using the traceback table.
    loc_col, loc_row = col-1, row-1
    max_value = 0
    while True:
        print("Current position: ", (loc_row, loc_col))
        if (loc_col == 0 and loc_row == 0):
            break
        elif loc_col == 0:
            second_align = "_" + second_align
            loc_row -= 1
        elif loc_row == 0:
            first_align = "_" + first_align
            loc_col -= 1
        else:
            left = traceback[loc_row][loc_col-1]
            top = traceback[loc_row-1][loc_col]
            top_left = traceback[loc_row-1][loc_col-1]
            print("(Left, Top, Top-Left): ", (left, top, top_left))
            max_value = max(left, top, top_left)
            if max_value == top_left:
                first_align = first[loc_col-1] + first_align
                second_align = second[loc_row-1] + second_align
                loc_row -= 1
                loc_col -= 1
            elif max_value == top:
                first_align = "_" + first_align
                second_align = second[loc_row-1] + second_align
                loc_row -= 1
            elif max_value == left:
                first_align = first[loc_col-1] + first_align
                second_align = "_" + second_align
                loc_col -= 1
        time.sleep(2.5)
    
    print("Alignment of two words:")
    print(first_align)
    print(second_align)

# Obtain the inputs via command arguments.
# Comment this out for user input style.
# Uncomment this out for command line style.
#first_word = sys.argv[1]
#second_word = sys.argv[2]
        
# Get the user prompt.
# Comment this out for command line style.
# Uncomment this out for user input style.
first_word = input("Enter the first word: ")
second_word = input("Enter the second word: ")

# Call the function.
edit_distance(first_word, second_word)
