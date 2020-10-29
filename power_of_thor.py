'''
autor = Michał Kosiński
problem = https://www.codingame.com/ide/puzzle/power-of-thor-episode-1
'''

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# ---
# Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

# light_x: the X position of the light of power
# light_y: the Y position of the light of power
# initial_tx: Thor's starting X position
# initial_ty: Thor's starting Y position
light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

thor_x_position = initial_tx
thor_y_position = initial_ty
# game loop
while True:
    remaining_turns = int(input())  # The remaining amount of turns Thor can move. Do not remove this line.

    if thor_x_position > light_x and thor_y_position > light_y:
        thor_x_position = thor_x_position - 1
        thor_y_position = thor_y_position - 1
        direction = 'NW'
    elif thor_x_position > light_x and thor_y_position < light_y:
        thor_x_position = thor_x_position - 1
        thor_y_position = thor_y_position + 1
        direction = 'SW'
    elif thor_x_position < light_x and thor_y_position < light_y:
        thor_x_position = thor_x_position + 1
        thor_y_position = thor_y_position + 1
        direction = 'SE'
    elif thor_x_position < light_x and thor_y_position > light_y:
        thor_x_position = thor_x_position + 1
        thor_y_position = thor_y_position - 1
        direction = 'NE'
    elif thor_x_position > light_x:
        thor_x_position = thor_x_position - 1
        direction = 'W'
    elif thor_x_position < light_x:
        thor_x_position = thor_x_position + 1
        direction = 'E'
    elif thor_y_position > light_y:
        thor_y_position = thor_y_position - 1
        direction = 'N'
    elif thor_y_position < light_y:
        thor_y_position = thor_y_position + 1
        direction = 'S'



    # A single line providing the move to be made: N NE E SE S SW W or NW
    print(direction)
