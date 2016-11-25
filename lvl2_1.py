def answer(l, t):
    # Searching solution
    for start, _ in enumerate(l):
        sum = 0
        for end, value in enumerate(l[start:]):
            sum += value
            if sum == t:
                return [start, end]
            elif sum > t: # No need to search further (no negative number)
                break

    # If we reach this code, the solution does not exist
    return [-1,-1]
