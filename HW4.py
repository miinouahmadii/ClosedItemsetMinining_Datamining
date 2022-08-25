import numpy as np
from os import sys
from operator import or_, and_
from functools import reduce
from copy import deepcopy

def rep(P, item):
    for i in P:
        if i[0] == item[0]:
            i = item
            return
    P.append(item)

def charm(P: list, minsup: int, C: dict):

    inP = sorted(P, key=lambda k: len(k[1]))

    for i in range(0, len(inP)):
        if i >= len(inP):
            break
        inP_i = list()
        for j in range(i+1, len(inP)):
            X = [reduce(or_, [inP[i][0], inP[j][0]]), reduce(and_, [inP[i][1], inP[j][1]])]

            if len(X[1]) >= minsup:
                if inP[i][1] == inP[j][1]:
                    rep(inP, X)
                    rep(inP_i, X)
                    del inP[j]
                else:
                    if inP[i][1] in inP[j][1]:
                        rep(inP, X)
                        rep(inP_i, X)
                    else:
                        for iset in inP_i:
                            if iset[0] == X[0]:
                                iset = X
                                continue
                        inP_i.append(X)

        if len(inP_i):
            charm(inP_i, minsup, C)
        exist = False
        for key, value in C.items():
            if inP[i][0].issubset(set(map(int, list(key.split(' '))))) and inP[i][1] == value:
                exist = True
                break
        if not exist:
            C[' '.join(map(str, inP[i][0]))] = inP[i][1]

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Bad Call")
        exit(-1)

    data_path   =   sys.argv[1]
    MINSUP      =   int(sys.argv[2])

    data_file = open(data_path)
    data = data_file.readlines()
    data = [list(map(int, row.strip(' \n').strip('\n').split(' '))) for row in data]
    data_file.close()
    # data = np.loadtxt(data_path)

    items   =   set(list(np.concatenate(data).flat))

    C = dict()

    P = [ [ {key}, set([index+1 for index, row in enumerate(data) if key in row]) ] for key in items ]
    P = [row for row in P if len(row[1]) >= MINSUP]

    charm(P, MINSUP, C)

    for key, value in C.items():
        print(set(map(int, list(key.split(' ')))), '-', len(value))
    print(len(C))
