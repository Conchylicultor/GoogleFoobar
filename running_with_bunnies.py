import itertools


def get_best(current, candidate):
    """ Return the new bunnies saved if the given candidate did saved
    more bunnies than the current
    Args:
        current (list[int]): sorted list of bunnies
        candidate (set[int]): unordered collection of saved bunnies
    Return:
        list[int]: bunnies saved sorted by ids
    """
    if len(candidate) > len(current):  # Better state
        return sorted(list(candidate))
    elif len(candidate) == len(candidate):  # Should check the individuals ids
        candidate = sorted(list(candidate))
        for i in range(len(current)):
            if current[i] < candidate[i]:  # We stop at the first id we found
                return current
            elif current[i] > candidate[i]:
                return candidate
    return current


def answer(times, time_limit):
    nb_pos = len(times)
    nb_bunnies = nb_pos-2
    assert nb_bunnies > 0

    moves = [[None]*nb_pos for _ in xrange(nb_pos)]  # Will contains the optimal moves

    # Compute the optimal path for each moves
    paths = itertools.chain(*map(  # Possibles moves
        lambda path_length: itertools.permutations(range(nb_pos), path_length),
        range(2, nb_pos+1)
    ))
    for path in paths:
        origin = path[0]
        destination = path[-1]

        # Compute the time to reach the destination
        cost = 0
        prev_pos = origin
        for pos in path:  # No need to keep track of the visited bunnies here (will be reconstructed at the end)
            cost += times[prev_pos][pos]
            prev_pos = pos

        # Is this cost better than the previous one ?
        if moves[origin][destination] == None or cost < moves[origin][destination]:
            moves[origin][destination] = cost

        # What if we try to go back to our origin ?
        cost += times[destination][origin]
        if cost < 0:  # If we gain some time, it means we could retake this loop indefinitelly to have infinite time => All bunnies saved !!!
            #print 'Loop detected'
            return range(nb_bunnies)

    # Debugging: show the grid of the optimals moves
    #for l in moves:
    #    print l

    # Final path reconstruction. Starting with start -> end and see if we
    # can insert bunnies along this path
    # start -> bunny 4 -> bunny 2 -> end
    bunnies_saved = []
    paths = itertools.chain(*map(  # All bunnies combinations in all possibles orders
        lambda path_length: itertools.permutations(range(nb_bunnies), path_length),
        range(0, nb_bunnies+1)
    ))
    for path in paths:
        origin = 0
        destination = nb_pos-1

        # Compute the time to reach the destination
        time = time_limit
        prev_pos = origin
        for pos in path:
            time -= moves[prev_pos][pos+1]
            prev_pos = pos+1  # We shift the ids (bunnies 0 start at 1)
        time -= moves[prev_pos][destination]

         # Have we reached the destination in time ?
        if time >= 0:
            bunnies_saved = get_best(bunnies_saved, path)

    return bunnies_saved


if __name__ == "__main__":
    grid1 = [
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0]
    ]
    print answer(grid1, 3)  # [0, 1]

    grid2 = [
        [0, 2, 2, 2, -1],
        [9, 0, 2, 2, -1],
        [9, 3, 0, 2, -1],
        [9, 3, 2, 0, -1],
        [9, 3, 2, 2, 0]
    ]
    print answer(grid2, 1)  # [1, 2]

    grid3 = [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1]
    ]
    print answer(grid3, 1)  # Infinite loop [0, 1, 2, 3, 4]

    grid21 = [
        [0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0]
    ]
    print answer(grid21, 1)  # Only exit possible []

    grid23 = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 9, 9, 9, 9, 9],
        [1, 9, 0, 9, 9, 9, 9],
        [1, 9, 9, 0, 9, 9, 9],
        [1, 9, 9, 9, 0, 9, 9],
        [1, 9, 9, 9, 9, 0, 9],
        [1, 9, 9, 9, 9, 9, 0]
    ]
    print answer(grid23, 3)  # Should go by the start case each time

    grid4 = [
        [0, 1, 1, 1, 1, 99, 1],
        [1, 0, 1, 1, 1, 99, 1],
        [1, 1, 0, 1, 1, 99, 1],
        [1, 1, 1, 0, 1, 99, -3],
        [1, 1, 1, 1, 0, 99, 1],
        [1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 99, 0]
    ]
    print answer(grid4, 1)  # Should loop end->bunny2->end->... to gain enough time to reach bunny4 [0, 1, 2, 3, 4]

    grid23 = [
        [0, 9, 1, 9, 9, 9, 9],
        [9, 0, 9, 9, 9, 9, 1],
        [9, 9, 0, 9, -1, 9, 9],
        [9, 9, 9, 0, 9, 9, 9],
        [9, 1, 9, 9, 0, 9, 9],
        [9, 9, 9, 9, 9, 0, 9],
        [9, 9, 9, 9, 9, 9, 0]
    ]
    print answer(grid23, 3)  # Should loop end->bunny2->end->... to gain enough time to reach bunny4 [0, 1, 2, 3, 4]
