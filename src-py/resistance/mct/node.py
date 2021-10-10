import copy
from math import log, sqrt


def getIndexOfList(l):
    k = 1
    ret = 0
    for s in l:
        ret += s * k
        k *= 10
    return str(ret)


def getPropose(childrenDict, startIndex, playerSize, prefix, missionSize):
    if startIndex + missionSize > playerSize:
        return
    elif missionSize == 0:
        childrenDict[getIndexOfList(prefix)] = [0, 0]
        return
    else:
        for i in range(startIndex, playerSize):
            newPrefix = copy.deepcopy(prefix) + (i,)
            getPropose(childrenDict, i+1, playerSize, newPrefix, missionSize-1)


class BaseNode:

    @staticmethod
    def chooseAction(children, c):
        n = 0
        for key in children:
            if children[key][1] == 0 :
                return key, 0
            n += children[key][1]
        log_n = log(n)
        l = [((children[key][0] / children[key][1] + c * sqrt(log_n /  children[key][1])), key) for key in children]
        l.sort()
        action = l[-1][1]
        return action, children[key][0] / children[key][1]

    @staticmethod
    def createVoteNode():
        children = {
            True: [0, 0],
            False: [0, 0]
        }

        return children

    @staticmethod
    def createProposeNode(missionSize, playerSize):
        children = {}
        getPropose(children, 0, playerSize, (), missionSize)
        return children

    @staticmethod
    def createBetrayNode():
        children = {
            True: [0, 0],
            False: [0, 0]
        }
        return children



            