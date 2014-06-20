import WeightedQuickUF as UF
import randomGrid as RG
import random
import collections
import time


def genRandomPairs(N):
    """
    generate random pairs between 0 and N - 1
    """
    p = random.randrange(0, N)
    q = random.randrange(0, N)
    while p == q:
        q = random.randrange(0, N)
    yield (p, q)


def average(alist):
    return sum(alist) / float(len(alist))


def count(N, algo):
    """
    N: the number of sites

    returns the number of random connection attempts
    needed to connect all sites
    """
    uf = UF.algo_dict[algo](N)
    num_connections = 0
    while uf.count() > 1:
        for p, q in genRandomPairs(N):
            num_connections += 1
            if uf.connected(p, q):
                continue
            else:
                uf.union(p, q)
    return (num_connections, num_connections / float(N))


def generate_grid_pairs(N):
    """
    returns a stack of all grid pairs (in random order and random-within-tuple)
    """
    return RG.randomGrid(N)


def collect_pairs(N, algo1):
    """
    generates random pairs and saves them on a deque to replay
    with both algo1 and algo2 (to compare running times)
    """
    que = collections.deque()
    uf = UF.algo_dict[algo1](N)
    while uf.count() > 1:
        for p, q in genRandomPairs(N):
            que.append((p, q))  # put (p, q) on deque
            if uf.connected(p, q):
                continue
            else:
                uf.union(p, q)
                #print p, q
    return que


def compare_algos(N, algo1, algo2):
    """
    collect random pairs and run both algos against same pairs
    each algo uses the same set of instructions to get
    more accurate running time comparison
    """
    results = {}
    # collect pairs
    # generates just enough pairs so sites are connected
    que = collect_pairs(N, algo1)
    # generates random grid pairs
    #que = generate_grid_pairs(N)

    # use algo1 with pairs
    uf = UF.algo_dict[algo1](N)
    start = time.time()
    while uf.count() > 1:
        p, q = que.popleft()
        que.append((p, q))
        #p, q = que.pop()
        #que.push((p, q))

        if uf.connected(p, q):
            continue
        else:
            uf.union(p, q)
    elapsed_time = time.time() - start
    results[algo1] = elapsed_time

    # use algo2 with same pairs
    uf = UF.algo_dict[algo2](N)
    start = time.time()
    while uf.count() > 1:
        p, q = que.popleft()
        que.append((p, q))
        #p, q = que.pop()
        #que.push((p, q))
        if uf.connected(p, q):
            continue
        else:
            uf.union(p, q)
    elapsed_time = time.time() - start
    results[algo2] = elapsed_time
    return results


def main(N=64, algo="WQUH", algo2=None):
    """
    1 arg: returns number of connections to connect N sites
    2 arg: returns ratio of running times for the 2 algos
    """
    if algo2 is None:
        num_connections, avg_connections = count(N, algo)
        return num_connections, avg_connections
    else:
        result_dict = compare_algos(N, algo, algo2)
        return N, result_dict[algo] / result_dict[algo2]

import math


def model(N=64, algo="WQUH"):
    """
    returns:
    number of random connections needed to connect N sites
    model vs experiment
    """
    count = 20
    res = []
    while count > 0:
        num_connections, _ = main(N, algo)
        res.append(num_connections)
        count -= 1
    return N * math.log(N) / 2.0, average(res)

###############################################
if __name__ == "__main__":
    N = raw_input("Enter N: ")
    algo = raw_input("Enter algo: ")
    print(model(int(N), algo))
