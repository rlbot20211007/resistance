from copy import copy


def getPropose(childrenDict:dict, startIndex:int, playerSize:int, prefix:tuple, missionSize:int):
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
    def __init__(self) -> None:
        # action: (count of resistantWin, count of visit)
        self.children = {}
        # true complete ; False incomplete
        self.state = False

    
    def get_unvisit(self):
        unvisit = []
        for key in self.children:
            if self.children[key][1] == 0 :
                unvisit.append(key)
        
        return unvisit, self.children.keys()

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
    def updateNode(nodeActionList, resistantWin):
        if resistantWin:
            for node, action in nodeActionList:
                node[action][0] += 1