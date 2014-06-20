import itertools
import random


def randomSwap(pair):
    r = random.randrange(2)
    if r:
        return pair
    else:
        return (pair[1], pair[0])


class randomizedStack(object):
    def __init__(self, *args):
        self.stack = list(itertools.chain(*args))
        self._size = len(self.stack)

    def push(self, item):
        self.stack.append(item)
        self._size += 1

    def pop(self):
        r = random.randrange(self._size)
        self.stack[self._size - 1], self.stack[r] = \
            self.stack[r], self.stack[self._size - 1]
        self._size -= 1
        return randomSwap(self.stack.pop())

    def isEmpty(self):
        return self._size == 0

    def size(self):
        return self._size


def randomGrid(N):
    """
    generates random pairs of connections for an NxN grid
    """
    cells = [(i / N, i % N) for i in range(N * N)]
    pairs_r = ((c, (c[0], c[1] + 1)) for c in cells if c[1] < N - 1)
    pairs_d = ((c, (c[0] + 1, c[1])) for c in cells if c[0] < N - 1)
    return randomizedStack(pairs_r, pairs_d)

