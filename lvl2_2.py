n = 8  # Chessboard dimention


def int_to_pos(number):
    """ Convert cell id into chessboard position    """
    x = number % n
    y = int(number // n)
    return (x, y)


def pos_to_int(x, y):
    """ Convert chessboard pos into cell id
    """
    return y*n + x


def test_conversion():
    """ Sanity check for the conversions functions
    """
    for i in range(n*n):
        print(int_to_pos(i))

    for y in range(n):
        for x in range(n):
            print pos_to_int(x, y), ' ',
        print ''

    for i in range(n*n):
        (x,y) = int_to_pos(i)
        assert i == pos_to_int(x,y)


def is_on_board(x, y):
    """ Return True if the given position is on the board
    """
    if 0 <= x < n and 0 <= y < n:
        return True
    return False


def increment_knight_moves(chessboard, x, y):
    """ Update the chessboard by moving the knight
    to the available cell
    Return the number of modified cells
    """
    current_dist = chessboard[y][x]
    sum_modifs = 0

    # Compute all possible moves from the given pos (some moves will overlap)
    for y_direction in [+1, -1]:
        for x_direction in [+1, -1]:
            for x_travel, y_travel in [(1,2),(2,1)]:
                x_dest = x + x_direction*x_travel
                y_dest = y + y_direction*y_travel
                if is_on_board(x_dest, y_dest) and chessboard[y_dest][x_dest] != -1:  # Free cell, we can move here
                    chessboard[y_dest][x_dest] = current_dist+1
                    sum_modifs += 1

    return sum_modifs


def fill_chessboard_next(chessboard, current_dist):
    """ Fill the next case. Modify the given chessboard
    return False if they was no empty case (no changes)
    """
    sum_modifs = 0
    for y in range(n):
        for x in range(n):
            if chessboard[y][x] == current_dist:
                sum_modifs += increment_knight_moves(chessboard, x, y)

    return sum_modifs > 0  # We continue if there has been some modifs


def answer(src, dest):
    if src == dest:
        return 0

    (x_src, y_src) = int_to_pos(src)
    (x_dest, y_dest) = int_to_pos(dest)

    # Here, I'll try to recursivelly compute the result for each
    # case. Because speed is a constrait (and memory is not), I
    # precompute all extrem results with a naive algo, so at execution
    # time, the program simply has to look in the right array cell
    chessboard = [[-1]*n for x in xrange(n)]

    current_dist = 0
    chessboard[y_src][x_src] = current_dist  # Already in the initial cell

    while fill_chessboard_next(chessboard, current_dist):
        current_dist += 1

    return chessboard[y_dest][x_dest]


def print_chessboard(chessboard):
    for y in range(n):
        for x in range(n):
            print chessboard[y][x], ' ',
        print ''


if __name__ == "__main__":
    print answer(5,5)
    print answer(0,1)
    print answer(0,10)
    print answer(0,63)
    print answer(63,0)
    print answer(0,7)
    print answer(7,0)
    print answer(63,7)
    print answer(7,63)
