'''
Extra Credit Task-

Tic tac toe input
Here's the backstory for this challenge: imagine you're writing a tic-tac-toe game, where the board looks like this:

1:  X | O | X
   -----------
2:    |   |  
   -----------
3:  O |   |
    A   B   C
The board is represented as a 2D list:

board = [
    ["X", "O", "X"],
    [" ", " ", " "],
    ["O", " ", " "],
]
Imagine if your user enters "C1" and you need to see if there's an X or O in that cell on the board. To do so, you need to translate from the string "C1" to row 0 and column 2 so that you can check board[row][column].

Your task is to write a function that can translate from strings of length 2 to a tuple (row, column). Name your function get_row_col; it should take a single parameter which is a string of length 2 consisting of an uppercase letter and a digit.

For example, calling get_row_col("A3") should return the tuple (2, 0) because A3 corresponds to the row at index 2 and column at index 0in the board.
'''

def get_row_col(position):
    position = position.upper()
    col_mapping = {'A': 0, 'B': 1, 'C': 2}
    if position[0] in col_mapping:
        col = col_mapping[position[0]]

    # return the tuple (row, col)
    return (int(position[1])-1, col)

if __name__ == '__main__':
    # Initialize board
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
    ]

    # Print the board
    for i in range(3):
        print(f"{i+1}:  {board[i][0]} | {board[i][1]} | {board[i][2]}")
        if i < 2:
            print("   -----------")
    print("    A   B   C")


    for turn_num in range(9):
        # Initialize player symbol
        player = "O"
        # Switch player symbol by turn
        if turn_num % 2 == 0:
            player="O"
        else:
            player="X"

        while(1):
            # Get user input 
            position = input(f"Player {player}: Enter position(ColRow): ")

            # Check user input
            # Check length of the input
            if len(position) != 2:
                print("Invalid input: your input should be a letter(col) followed by an integer(row)\n")
                continue

            isValid = True

            # Check range of col and row
            if position[0] >= '1' and position[0] <= '3':
                print("Invalid input: The first char is col which should be a letter from A to C")
                isValid = False
            elif position[0].upper() < 'A' or position[0].upper() > 'C':
                print("Invalid input: col should be a letter from A to C")
                isValid = False

            if position[1].upper() >= 'A' and position[1].upper() <= 'C':
                print("Invalid input: The second char is row which should be an integer from 1 to 3")
                isValid = False
            elif position[1] < '1' or position[1] > '3':
                print("Invalid input: row should be an integer from 1 to 3")
                isValid = False

            if not isValid:
                print("\n")
                continue

            # Get row and col
            row, col = get_row_col(position)

            # Check if the cell is free
            if board[row][col] != ' ':
                print(f"There's an {board[row][col]} in the cell {position} on the board.")
                continue
            else:
                print("\n")
                break

        # Set row and col
        board[row][col] = player

        # Print the board
        for i in range(3):
            print(f"{i+1}:  {board[i][0]} | {board[i][1]} | {board[i][2]}")
            if i < 2:
                print("   -----------")
        print("    A   B   C")
        

