def answer(l):
    # Most extrem case: l = [1 for i in range(1,2000)]

    n = len(l)

    # First step: extract lucky doubles
    lucky_doubles_next = []  # Were to go from there
    lucky_doubles_count = {}  # Keep count of original
    # o(n*n) ~= 4000000 (still good)
    for i in xrange(0, n-1):
        for j in xrange(i+1, n):
            if l[j] % l[i] == 0:  # Lucky double found !
                lucky_doubles_next.append(j)
                lucky_doubles_count[i] = lucky_doubles_count.get(i, 0) + 1  # Counting how many double there is for the current id

    # Early exit
    #n_doubles = len(lucky_doubles_next)
    #if n_doubles < 2:  # Not enough tuples
    #    return 0

    # Then, combine lucky doubles together
    glob_sum = 0
    for v in lucky_doubles_next:  # Linear time :)
        glob_sum += lucky_doubles_count.get(v, 0)

    return glob_sum


if __name__ == "__main__":
    print answer([1,2,3,4,5,6])
    print answer([1,2,4,1,2,4])  # Warning: Remove doublons ??
    print answer([2,4,6,3,9,81])  #
    print answer([1,1,1])
    print answer([1,1])
    print answer([1, 4, 7, 13])
    print answer([4, 7, 13])

    # Some more extrem cases
    l = [1 for i in range(1,2000)]
    print answer(l)

    l = [i for i in range(1,5000)]
    print answer(l)
