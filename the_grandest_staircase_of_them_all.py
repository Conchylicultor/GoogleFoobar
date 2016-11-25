import math


def memoize(f):
    """ Memoization decorator
    """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


@memoize
def build_stair(reserve, previous_step):
    """ Recursive function to compute the solution
    Args:
        reserve: reserve of bricks
        previous_step: previous step size (for
        debugging purpose (bad perfs), could be replaced by
        the list of all previous steps, so we can see the
        stair configurations [1])
    Return:
        the number of possible solution given the reserve
    """

    # End of recurence if no more bricks to use
    if reserve == 0:
        # print previous_steps  # [1]
        return 1

    # Otherwise, we continue building the stair

    # With the given constraints, the greatest stair we could eventually do
    # with the current reserve is:
    # 0
    # 00
    # 00..0
    # 00..00
    # 00..000
    # 00..0000
    # n...4321
    # with 1+2+3+...+n = n(n+1)/2 = reserve
    # This mean the minimum number of bricks for the current step
    # is n (using a smaller number, we will have too many bricks
    # left to finish the stair)
    #
    # Solving (n^2 +n -2*reserve = 0) gives us

    min_brick = (-1+math.sqrt(1+8*reserve)) / 2 # >0
    min_brick = int(math.ceil(min_brick)) # float to int

    if previous_step == -1:  # First step
        max_bricks = reserve  # We can't use all our bricks at once
    else:
        max_bricks = previous_step
    max_bricks = min(max_bricks, reserve+1)  # We can only build if we put a smaller number of bricks than the previous one

    nb_stairs = 0
    for i in range(min_brick, max_bricks):  # Nb of brick for the current step
            nb_stairs += build_stair(reserve-i, i)
    return nb_stairs


def answer(n):
    return build_stair(n, -1)


if __name__ == "__main__":
    for i in range(201):
        print ''
        ans = answer(i)
        print i, '->', ans
