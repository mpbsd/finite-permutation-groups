#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from functools import reduce
from itertools import permutations


def PermutationFromList(X, permutation_of_X):
    return dict(zip(X, permutation_of_X))


def SymmetricGroup(X):
    SX = []
    for p in permutations(X):
        SX.append(dict(zip(X, list(map(lambda x: p[x], X)))))
    return SX


def Product(X, p, q):
    return dict(zip(X, list(map(lambda x: p[q[x]], X))))


def Orbit(X, x, p):
    orb = [x]
    if p[x] != x:
        q = p
        while q[x] != x:
            orb.append(q[x])
            q = Product(X, q, p)
    return orb


def Union(orbits):
    X0 = []
    for orbit in orbits:
        for x in orbit:
            if x not in X0:
                X0.append(x)
    return sorted(X0)


def Orbits(X, p):
    orbits = [Orbit(X, 0, p)]
    if Union(orbits) != X:
        x = [x for x in X if x not in Union(orbits)][0]
        orbits.append(Orbit(X, x, p))
    return orbits


def PrettyPrint(X, orbits):
    re_1 = re.compile(r"^\[\[")
    re_2 = re.compile(r"\]\]$")
    re_3 = re.compile(r"\], \[")
    re_4 = re.compile(r"\([0-9]\)")
    re_5 = re.compile(r"^$")
    representation = str(orbits)
    representation = re_1.sub(r"(", representation)
    representation = re_2.sub(r")", representation)
    representation = re_3.sub(r")(", representation)
    representation = re_4.sub(r"", representation)
    representation = re_5.sub(r"()", representation)
    return representation


def Signal(X, n, p):
    Y = reduce(
        lambda x, y: x * y,
        [
            reduce(lambda x, y: x * y, [X[j] - X[i] for j in range(i + 1, n)])
            for i in range(n - 1)
        ],
    )
    Z = reduce(
        lambda x, y: x * y,
        [
            reduce(
                lambda x, y: x * y,
                [X[p[j]] - X[p[i]] for j in range(i + 1, n)],
            )
            for i in range(n - 1)
        ],
    )
    return Z // Y


def main():
    n = 4
    X = list(range(n))
    G = SymmetricGroup(X)
    for p in G:
        A = PrettyPrint(X, Orbits(X, p))
        for q in G:
            B = PrettyPrint(X, Orbits(X, q))
            C = PrettyPrint(X, Orbits(X, Product(X, p, q)))
            print("%s * %s = %s" % (A, B, C))
        # print("%+d: %s" % (Signal(X, n, p), PrettyPrint(X, Orbits(X, p))))


if __name__ == "__main__":
    main()
