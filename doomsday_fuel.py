#import numpy as np
from fractions import Fraction  # Avoid float approximation, automatically simplify the fractions
from fractions import gcd

# Maths & utilities functions


def inv(A):
    """ Return the matrix inverse
    Uses Gauss-Jordan Elimination, seems the simplest
    to implement and gives exact values
    """
    n = len(A)  # The input matrix is squared

    table = [[0]*2*n for _ in xrange(n)]  # Create an empty table

    # Copy initial values
    for i in range(n):
        for j in range(n):
            table[i][j] = A[i][j]
        table[i][i+n] = 1  # Diagonal matrix

    # State: table = [A|I]
    #print(np.array(table))

    # Pivoting
    for i in range(n):  # For each row
        # First we normalize the current row (first idx = 1)
        scalar = table[i][i]  # We have guaranty that this value won't be 0 (otherwise
                              # proba=1.0 so it would  have been a stable state)
        for j in range(2*n):
            table[i][j] /= scalar

        # Then, we substract the row to all the next and previous ones
        for j in range(n):
            if j != i:
                scalar = table[j][i]
                for k in range(2*n):
                    table[j][k] -= scalar * table[i][k]

    # State: table = [I|A^-1]
    #print(np.array(table))

    B = [table[i][n:] for i in range(n)]  # Paste the result
    return B


def get_transition_matrix(m):
    """
    Compute the absorbsion transition matrix on
    its standard form:
    P= | Q | R |
       | 0 | I |

    Compute also the idx correspondances List[(int,int)] (mapping
    old_id -> new_id)
    The first line is always stayed intact (initial state)
    """
    n = len(m)

    P = [[0]*n for _ in xrange(n)]  # Initialize matrix

    map_states_tra = {}  # Transitional states
    map_states_abs = {}  # Finals states

    for i in range(n):
        total_weights = sum(m[i])
        if total_weights == 0:
            map_states_abs[i] = len(map_states_abs)

            pos = n - len(map_states_abs)  # Diagonal matrix
            P[pos][pos] = 1  # TODO: Use fraction instead ?
        else:
            map_states_tra[i] = len(map_states_tra)

            for j in range(n):  # Normalize the weights
                m[i][j] = Fraction(m[i][j],total_weights)

    len_tran = len(map_states_tra)
    for k, v in map_states_abs.iteritems():  # Shift the ids (keep the same order of final state so we don't have to resort the idx at the end)
        map_states_abs[k] += len_tran

    map_states_tra.update(map_states_abs)
    map_states = map_states_tra

    inv_map_states = {v: k for k, v in map_states.iteritems()}
    # We rewrite the matrix with the right ids
    for i in range(len_tran):
        for j in range(n):
            P[i][j] = m[inv_map_states[i]][inv_map_states[j]]

    Q = [x[0:len_tran] for x in P[0:len_tran]]
    R = [x[len_tran:] for x in P[0:len_tran]]

    return Q, R


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def normalize_probs(probs):
    """ Compute the global least common multiple and return the probabilities
    in the asked format
    """
    lcm_glob = reduce(lcm, [fract.denominator for fract in probs])

    normalized_probs = [fract.numerator * lcm_glob // fract.denominator for fract in probs]
    normalized_probs.append(lcm_glob)

    return normalized_probs



def answer(m):
    # The problem is equivalent to computing the absorbsion
    # probability of the markov chain

    # Case where the initial state is final (all state finals)
    if sum(m[0]) == 0:
        return [1, 1]

    ## The easiest way to get an approximation would
    ## be to run an important number of markov steps
    #P = get_transition_matrix(m)
    #p = np.array([
        #[ 1, 0, 0, 0, 0, 0]  # At time 0, we are 100% in the first state
    #])
    #for i in range(500):
        #p = np.dot(p,P) # Moving to the next state
    #print(p)  # We get a pretty good estimation of the final state


    # Analytic solving
    Q, R = get_transition_matrix(m)

    for i in range(len(Q)):
        Q[i][i] -= 1
    F = inv(Q)  # F = -(I-Q)^-1 (WARNING: Opposite sign)

    probs = []
    for i in range(len(R[0])):
        cell = 0
        for j in range(len(F)):
            cell += -F[0][j]*R[j][i]  # (WARNING: We correct the negative sign here)
        probs.append(cell)

    probs_normalized = normalize_probs(probs)
    return probs_normalized


if __name__ == "__main__":

    a = answer([
        [ 0, 1, 0, 0, 0, 1],  # If not final state, divide by sum of weights (prob sum to one)
        [ 4, 0, 0, 3, 2, 0],
        [ 0, 0, 0, 0, 0, 0],  # If si final state, P(i,i) = 1
        [ 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0]
    ])
    print(a)

    a = answer([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    print(a)
