import ErdosRenyi as ER
import time
import re
from decimal import Decimal
INF = Decimal('infinity')

ALGOS = ["QF", "QU", "WQU", "WQUH", "WQUPC"]
DEFAULT_ALGO_0 = ALGOS[3]
DEFAULT_ALGO_1 = ALGOS[4]
DEFAULT_N = 64
DEFAULT_T = 8


def check_algo_input(algo, index):
    if algo in ALGOS:
        return algo.upper()
    if index == 0:
        return DEFAULT_ALGO_0
    else:
        return DEFAULT_ALGO_1


def check_N_input(n):
    """
    n is a string from raw_input
    """
    pat = re.compile(r'[2-9][0-9]*')
    m = pat.match(n)
    if not m:
        return DEFAULT_N
    else:
        return int(n)


def check_T_input(t):
    """
    t is a string from raw_input
    """
    pat = re.compile(r'[1-5][0-9]*')
    m = pat.match(t)
    if not m:
        return DEFAULT_T
    else:
        return int(t)


def performance(algo=""):
    """
    algo: the UnionFind algorithm: QF, QU, WQU, WQUH, WQUPC
    T: the number of trials
    N: the starting number of sites
    """
    if algo is "":
        algo = DEFAULT_ALGO_0
    T = input("Enter number of trials: ")
    T = check_T_input(T)
    N = input("Enter starting N: ")
    N = check_N_input(N)
    start = time.time()
    connections, avg_connections = ER.main(N, algo)
    prev_elapsed_time = time.time() - start
    T -= 1
    print()
    print('algo:', algo)
    print("{:<10}{:<18}{:<18}{:<10}".format("N", "num_connections",
                                            "avg_connections",
                                            "curr_time : prev_time"))
    while T > 0:
        N = 2 * N
        start = time.time()
        connections, avg_connections = ER.main(N, algo)
        elapsed_time = time.time() - start

        if prev_elapsed_time == 0:
            time_ratio = INF
        else:
            time_ratio = elapsed_time / prev_elapsed_time
        print("{:<10}{:<18}{:<18}{:<10}".
              format(N, connections, avg_connections, time_ratio))
        prev_elapsed_time = elapsed_time
        T -= 1


def compare_algos(algo="", algo2=""):
    if algo is "":
        algo = "WQUH"
    if algo2 is "":
        algo2 = "WQUPC"
    T = input("Enter number of trials: ")
    T = check_T_input(T)
    N = input("Enter starting N (64 - 500): ")
    N = check_N_input(N)
    print()
    print('algo1:', algo, 'algo2:', algo2)
    print("{:<10}{:<18}".format("N", "algo1:algo2"))
    print()
    while T > 0:
        N, algo_to_algo2_ratio = ER.main(N, algo, algo2)
        print("{:<10}{:<18}".format(N, algo_to_algo2_ratio))
        N = 2 * N
        T -= 1


def main(func_num=""):
    test = {"1": performance, "0": compare_algos}
    if func_num is "":
        func_num = "1"
    if func_num == "0":
        algo = input("Enter algo: ")
        algo = check_algo_input(algo.upper(), 0)
        algo2 = input("Enter another algo: ")
        check_algo_input(algo2.upper(), 1)
        test[func_num](algo, algo2)
    else:
        algo = input("Enter algo: ")
        algo = check_algo_input(algo.upper(), 0)
        test[func_num](algo)

########################################################
if __name__ == "__main__":
    print('algorithms:')
    for algo in ALGOS:
        print(algo, end=' ')
    print()
    num = input("Enter test: \
     [0: compare algos  1: test single algo]: default is 1: ")
    main(num)

