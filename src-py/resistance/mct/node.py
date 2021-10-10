from copy import copy
from math import log, sqrt


def getPropose(childrenDict, startIndex, playerSize, prefix, missionSize):
    if startIndex + missionSize > playerSize:
        return
    elif missionSize == 0:
        childrenDict[prefix] = (0,0)
        return
    else:
        for i in range(startIndex, playerSize):
            newPrefix = copy.deepcopy(prefix) + (i,)
            getPropose(childrenDict, i+1, playerSize, newPrefix, missionSize-1)


class BaseNode:
    def __init__(self):
        # action: (count of win, count of visit)
        # cannot use the next state as index, for that is not sure
        self.children = {}


    
    def chooseAction(self, c):
        n = 0
        for key in self.children:
            if self.children[key][1] == 0 :
                return key, 0
        log_n = log(n)
        l = [((self.children[key][0] / self.children[key][1] + c * sqrt(log_n /  self.children[key][1])), key) for key in self.children]
        l.sort()
        action = l[-1][1]
        return action, self.children[key][0] / self.children[key][1]

    @staticmethod
    def createVoteNode():
        voteNode = BaseNode()
        voteNode.children = {
            True: (0,0),
            False: (0,0)
        }

        return voteNode

    @staticmethod
    def createProposeNode(missionSize, playerSize):
        proposeNode = BaseNode()
        getPropose(proposeNode.children, 0, playerSize, (), missionSize)
        return proposeNode

    @staticmethod
    def createBetrayNode():
        betrayNode = BaseNode()
        betrayNode.children = {
            True: (0,0),
            False: (0,0)
        }
        return betrayNode



            