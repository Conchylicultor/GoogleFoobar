import cv2
import numpy as np
import copy

from fractions import gcd


def is_power_of_two(x):
    """ Quick hack to check if x==2^n
    """
    return (x & (x - 1)) == 0 and x != 0  # The second condition is useless here (nb of bananas never 0)


def has_exit(i, j):
    """ Check if the sequence starting with the given numbers
    will reach an exit point.
    """
    return is_power_of_two((i+j) / gcd(i,j))


def write_grid_img():
    """ Record the nice fractal-like motif of the
    exit states

    |x   x       x               x
    |  x       x               x
    |x   x   x       x       x
    |      x               x
    |    x   x           x       x
    |  x       x       x               x
    |x           x   x
    |              x
    |    x       x   x           x
    |          x       x
    |        x           x
    |      x               x
    |    x                   x           x
    |  x                       x       x
    |x       x       x           x   x
    |                              x
    |                            x   x
    |          x               x       x
    |                        x           x

    The fast formula found with the help of this figure is then
    used to optimize the figure computation itself.

    """
    dim = 500
    img = np.zeros((dim, dim))
    for i in range(1, dim):
        for j in range(i, dim):
            if has_exit(i, j):
                img[i,j] = 255
                img[j,i] = 255
    cv2.imwrite('fractal.png', img)


class Guard:
    """ Node of the graph
    Is connected to the other guards for which
    it would ends and those for which it would
    loop
    """
    def __init__(self, bananas):
        self.bananas = bananas  # Not necessary but useful for to show the final pairs
        self.exit = []
        self.loop = []


def disconnect_node(list_nodes, node):
    """ Remove the node from the graph
    """
    # Update the other nodes on the graph
    for n in node.exit:
        n.exit.remove(node)
    for n in node.loop:
        n.loop.remove(node)
    # Removing the node
    list_nodes.remove(node)


def disconnect_pair(list_nodes, node1, node2):
    """ Remove the pair from the Graph
    """
    disconnect_node(list_nodes, node1)
    disconnect_node(list_nodes, node2)


def answer(banana_list):
    """
    Iterativelly forms pairs with the guards whose seems the
    more promising to minimize the final score.

    Not completly sure it always gives the optimal
    analytic solution, but surelly a fairly good approximation
    in most cases, pass all test cases and gives exactly
    the pairs associated with the result
    """

    nb_guard = len(banana_list)

    # Undirected graph construction
    guards = [Guard(banana_list[i]) for i in xrange(nb_guard)]
    for i in xrange(0, nb_guard-1):
        for j in xrange(i+1, nb_guard):
            if has_exit(banana_list[i], banana_list[j]):
                guards[i].exit.append(guards[j])
                guards[j].exit.append(guards[i])
            else:
                guards[i].loop.append(guards[j])
                guards[j].loop.append(guards[i])

    counter = 0  # Final result
    pairs = []  # Not necessary for the task but easy to obtain

    # In case of odd number of guard, we add an additional guard linked
    # with everyone else (Not necessary to pass the foobar test cases
    # but is useful in the case if the current_guard should better as a
    # the singleton connected to a pair, ex: [7,1,21]-> ([1,21],[7])
    # instead of ([7,21], [1]))
    if nb_guard % 2 == 1:
        singleton_guard = Guard(-1)
        for guard in guards:
            singleton_guard.exit.append(guard)
            guard.exit.append(singleton_guard)
        guards.append(singleton_guard)
        counter -= 1  # The added node don't count in the final counter

    while len(guards) > 0:
        guards.sort(key=lambda x: len(x.exit), reverse=True)  # The guards with the most exits come first

        current_guard = guards[0]  # We select the guard for which it will be hard to get rid off
        found_good = False
        for candidate_pair in guards[1:]:  # We loop over the most promising guards
            if candidate_pair in current_guard.loop:
                pairs.append((current_guard, candidate_pair))
                disconnect_pair(guards, current_guard, candidate_pair)
                found_good = True
                break
        if not found_good:
            counter += 2  # Penalty: We linked two bad guards together
            pairs.append((current_guard, guards[1]))
            disconnect_pair(guards, current_guard, guards[1])  # We pop the two first guards (Could use collections.deque instead of List)

    # Finals pairs
    #for pair in pairs:
    #    print pair[0].bananas, pair[1].bananas

    return counter


if __name__ == "__main__":
    print answer([1, 1])
    print answer([1, 7, 3, 21, 13, 19])
    print answer([3, 3, 2, 6, 6])
    print answer([1, 7, 21])
