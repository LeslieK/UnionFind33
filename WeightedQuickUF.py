class QuickFind(object):
    def __init__(self, N):
        self._N = N
        self._id = [i for i in range(N)]
        self._count = N
        self._accesscnt = 0

    def find(self, p):
        "return component id"
        self._accesscnt += 1
        return self._id[p]

    def count(self):
        return self._count

    def union(self, p, q):
        self._accesscnt = 0  # reset cost
        if self.connected(p, q):
            return
        qid = self._id[q]
        pid = self._id[p]
        self._accesscnt += 2
        for i in range(self._N):
            if self._id[i] == pid:
                self._id[i] = qid
                self._accesscnt += 1
            self._accesscnt += 1
        self._count -= 1

    def connected(self, p, q):
        self._accesscnt += 2
        return self._id[p] == self._id[q]

    def accesscnt(self):
        return self._accesscnt


class QuickUnion(object):
    """
    id[p] contains parent of p
    """
    def __init__(self, N):
        self._N = N
        self._id = [i for i in range(N)]
        self._count = N
        self._accesscnt = 0

    def find(self, p):
        "return component of id"
        while p != self._id[p]:
            p = self._id[p]
            self._accesscnt += 2
        self._accesscnt += 1
        return p

    def union(self, p, q):
        self._accesscnt = 0
        pid = self.find(p)
        qid = self.find(q)
        if pid == qid:
            return
        # connect p's component to q's component
        self._accesscnt += 1
        self._id[pid] = qid
        self._count -= 1

    def connected(self, p, q):
        self._accesscnt += 2
        return self._id[p] == self._id[q]

    def count(self):
        return self._count

    def accesscnt(self):
        return self._accesscnt


class WeightedQuickUnionUF(object):
    def __init__(self, N):
        self._id = [i for i in range(N)]
        self._size = [1 for i in range(N)]
        self._count = N
        self._accesscnt = 0

    def newSite(self):
        new_site = sum(self._size)
        self._id.append(new_site)
        self._size.append(1)
        self._count += 1
        return new_site

    def count(self):
        return self._count

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    # def find(self, p):
    #     """
    #     returns component id (root)
    #     """
    #     if p == self._id[p]:
    #         self._accesscnt += 1
    #         return p
    #     else:
    #         self._accesscnt += 2
    #         return self.find(self._id[p])

    def find(self, p):
        """
        returns component id (root)
        """
        while p != self._id[p]:
            p = self._id[p]
            self._accesscnt += 2
        self._accesscnt += 1
        return p

    def union(self, p, q):
        self._accesscnt = 0
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._size[i] < self._size[j]:
            self._id[i] = j
            self._size[j] += self._size[i]
            self._size[i] = 0
        else:
            self._id[j] = i
            self._size[i] += self._size[j]
            self._size[j] = 0
        self._count -= 1
        self._accesscnt += 5

    def accesscnt(self):
        return self._accesscnt


class WeightedQuickUnionUFHeight(object):
    """
    tracks tree height; moves shorter tree to point to taller tree
    """
    def __init__(self, N):
        self._id = [i for i in range(N)]
        self._height = [0 for i in range(N)]
        self._count = N
        self._accesscnt = 0

    def count(self):
        return self._count

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, p):
        """
        returns component id (root)
        """
        while p != self._id[p]:
            p = self._id[p]
            self._accesscnt += 2
        self._accesscnt += 1
        return p

    def union(self, p, q):
        self._accesscnt = 0
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._height[i] < self._height[j]:
            self._id[i] = j
            self._height[i] = 0
            self._accesscnt += 5
            # height of self._id[j] is unchanged
        elif self._height[i] == self._height[j]:
            self._id[j] = i
            self._height[j] = 0
            self._height[i] += 1
            self._accesscnt += 6
        else:
            self._id[j] = i
            self._height[j] = 0
            self._accesscnt += 6
        self._count -= 1

        #print self._height

    def accesscnt(self):
        return self._accesscnt


class WeightedQuickUnionUFPC(object):
    def __init__(self, N):
        self._id = [i for i in range(N)]
        self._size = [1 for i in range(N)]
        self._count = N
        self._accesscnt = 0

    def newSite(self):
        new_site = sum(self._size)
        self._id.append(new_site)
        self._size.append(1)
        self._count += 1
        return new_site

    def count(self):
        return self._count

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, p):
        """
        returns component id (root)
        """
        if p == self._id[p]:
            self._accesscnt += 1
            return p
        else:
            self._accesscnt += 2
            self._id[p] = self.find(self._id[p])
            return self._id[p]

    def union(self, p, q):
        self._accesscnt = 0
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._size[i] < self._size[j]:
            self._id[i] = j
            self._size[j] += self._size[i]
            self._size[i] = 0
        else:
            self._id[j] = i
            self._size[i] += self._size[j]
            self._size[j] = 0
        self._count -= 1
        self._accesscnt += 5

    def accesscnt(self):
        return self._accesscnt

algo_dict = {"QF": QuickFind,
             "QU": QuickUnion,
             "WQU": WeightedQuickUnionUF,
             "WQUH": WeightedQuickUnionUFHeight,
             "WQUPC": WeightedQuickUnionUFPC}


def mainQF(filename):
    with open(filename) as f:
        N = f.readline()
        uf = QuickFind(int(N))
        total = 0
        i = 0

        lines = (line.strip().split() for line in f)
        sites = ((int(line[0]), int(line[1])) for line in lines)

        for p, q in sites:
            i += 1
            uf.union(p, q)
            total += uf.accesscnt()
            #print i, uf.accesscnt(), total / i
        print("total: ", total, "avg: ", total / i)


def mainQU(filename):
    with open(filename) as f:
        N = f.readline()
        uf = QuickUnion(int(N))
        total = 0
        i = 0

        lines = (line.strip().split() for line in f)
        sites = ((int(line[0]), int(line[1])) for line in lines)

        for p, q in sites:
            i += 1
            uf.union(p, q)
            total += uf.accesscnt()
            #print i, uf.accesscnt(), total / i
        print("total: ", total, "avg: ", total / i)


def mainWQU(filename):
    with open(filename) as f:
        N = f.readline()
        uf = WeightedQuickUnionUF(int(N))
        total = 0
        i = 0

        lines = (line.strip().split() for line in f)
        sites = ((int(line[0]), int(line[1])) for line in lines)

        for p, q in sites:
            i += 1
            uf.union(p, q)
            total += uf.accesscnt()
            #print i, uf.accesscnt(), total / i
        print("total: ", total, "avg: ", total / i)

import math
import matplotlib.pyplot as plt


def mainWQUH(filename):
    with open(filename) as f:
        N = f.readline()
        uf = WeightedQuickUnionUFHeight(int(N))
        total = 0
        i = 0
        totalcum = []
        accessnum = []

        lines = (line.strip().split() for line in f)
        sites = ((int(line[0]), int(line[1])) for line in lines)

        for p, q in sites:
            i += 1
            uf.union(p, q)
            total += uf.accesscnt()
            accessnum.append(uf.accesscnt())
            totalcum.append(total / i)
        #plt.plot(accessnum)
        #plt.plot(totalcum)
        #plt.show()

            #print i, uf.accesscnt(), total / i
        print("total: ", total, "avg: ", total / i, "height: ", \
            max(uf._height), math.log(float(N), 2), \
            max(uf._height) / math.log(float(N), 2))


def mainWQUPC(filename):
    with open(filename) as f:
        N = f.readline()
        uf = WeightedQuickUnionUFPC(int(N))
        total = 0
        i = 0

        lines = (line.strip().split() for line in f)
        sites = ((int(line[0]), int(line[1])) for line in lines)

        for p, q in sites:
            i += 1
            uf.union(p, q)
            total += uf.accesscnt()
            #print i, uf.accesscnt(), total / i
        print("total: ", total, "avg: ", total / i)
        #print uf._id

NEWLINE = "\n"


def writeWorseCaseData(filename, N):
    """
    generates long skinny tree; bad for QuickUnion
    """
    n = N
    with open(filename, "w") as f:
        f.write(str(n) + NEWLINE)
        for i in range(1, N):
            f.write("0 " + str(i) + NEWLINE)


def writeWorseCaseDataWUF(filename, height):
    """
    generates worse case trees for WUF (PC has no affect)
    """
    n = 2 ** height
    with open(filename, "w") as f:
        f.write(str(n) + NEWLINE)
        count = 0
        while count < height:
            delta = 2 ** count
            for i in range(0, n, 2 * delta):
                f.write(str(i) + " " + str(i + delta) + NEWLINE)
            count += 1

