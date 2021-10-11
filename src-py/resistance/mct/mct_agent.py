from .greedy_agent import GreedyAgent
from ..random_agent import RandomAgent
from .node import BaseNode, getIndexOfList
import json

class MCTAgent(RandomAgent):        
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name='Mct', sharedMctNodes = None, isTest=False):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        RandomAgent.__init__(self, name)

        if sharedMctNodes:
            self.mctNodes = {}
        else:
            self.mctNodes = sharedMctNodes
        self.C = 1

        self.trajectory = []

        # use greedy if isTest
        self.isTest = isTest
        self.greedy = GreedyAgent()
    

    def get_state(self, mission):
        # while a trajectory is better, it is hard to store.
        currentstate = (getIndexOfList([self.number_of_players , self.round_index , self.mission_index]), getIndexOfList([self.player_number, ] + self.spy_list), getIndexOfList(mission))
        # save state string to self.currentstate
        self.currentstate = "-".join(currentstate)
        

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        # update greedy policy
        if (self.isTest):
            self.greedy.new_game(number_of_players, player_number, spy_list)

        # store game feature
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list

        # initial
        self.round_index = 0
        self.mission_index = 0
        return


    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list


    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        # update state
        self.get_state(mission=[self.player_number,])

        # get mct action
        if not self.currentstate in self.mctNodes:
            self.mctNodes[self.currentstate] = BaseNode.createProposeNode(team_size, playerSize=self.number_of_players)
        mct_action, win_rate =  BaseNode.chooseAction(self.mctNodes[self.currentstate], self.C)

        # if in test mode, and win_rate is ralatively low
        if self.isTest and (win_rate < 0.5):

            # get rule action
            rule_act = self.greedy.propose_mission(team_size, betrayals_required)
            rule_act.sort()
            self.trajectory.append((self.mctNodes[self.currentstate], getIndexOfList(rule_act)))
            return rule_act
        else:
            self.trajectory.append((self.mctNodes[self.currentstate], mct_action))

            # recover propose list from action string
            k = 1
            team = []
            action = int(mct_action)
            for _ in range(team_size):
                t = action % k
                team.append(t)
                k *= 10
                action = (action - t) // 10
                
            return team     

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        mission = list(mission)
        mission.sort()
        self.get_state(mission=[proposer,] + mission)
        if not self.currentstate in self.mctNodes:
            self.mctNodes[self.currentstate] = BaseNode.createVoteNode()
        mct_action, win_rate =  BaseNode.chooseAction(self.mctNodes[self.currentstate], self.C)   

        if self.isTest and (win_rate < 0.5):
            rule_act =  self.greedy.vote(mission, proposer)
            self.trajectory.append((self.mctNodes[self.currentstate], rule_act))
            return rule_act
        else:
            self.trajectory.append((self.mctNodes[self.currentstate], mct_action))
            return mct_action   


    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # update state
        votes.sort()        
        nodeIndex = self.currentstate + '-' +getIndexOfList(votes)
        self.mission_index += 1

        # if not a spy, store the node as a null node
        if not self.is_spy():
            if not nodeIndex in self.mctNodes:
                self.mctNodes[nodeIndex] = None
            self.trajectory.append((self.mctNodes[nodeIndex], None))
        
        # wait until betray node
        else:
            self.currentstate = nodeIndex
        return

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''

        # only spy need to deal with the action
        if self.is_spy():
            if not self.currentstate in self.mctNodes:
                self.mctNodes[self.currentstate] = BaseNode.createBetrayNode()
            mct_action, win_rate =  BaseNode.chooseAction(self.mctNodes[self.currentstate], self.C)   

            if self.isTest and (win_rate < 0.5):
                rule_act =  self.greedy.betray(mission, proposer)
                self.trajectory.append((self.mctNodes[self.currentstate], rule_act))
                return rule_act
            else:
                self.trajectory.append((self.mctNodes[self.currentstate], mct_action))
                return mct_action  

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        # get state, store the node as a null node
        nodeIndex = self.currentstate + '-' + getIndexOfList((betrayals, 1 if mission_success else 0),)
        if not nodeIndex in self.mctNodes:
            self.mctNodes[nodeIndex] = None
        self.trajectory.append((self.mctNodes[nodeIndex], None))
        return

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        # update mission_index, round_index
        self.mission_index = 0
        self.round_index = rounds_complete
        return
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail--> a.game_outcome(self.missions_lost<3, self.spies)
        spies, a list of the player indexes for the spies.    
        '''
        spies_win = not spies_win
        win = (self.is_spy and spies_win) or ((not self.is_spy()) and (not spies_win))

        # update node
        for node, act in self.trajectory:
            if node:
                node[act][0] += (1 if win else 0)
                node[act][1] += 1
        return

    @staticmethod
    def load(path = 'mctnodes_dict.json'):
        f = open(path, 'r')
        content = f.read()
        mctnodes = json.loads(content)
        for state in mctnodes:
            if (mctnodes[state]) and ('true' in mctnodes[state]):
                previous = mctnodes[state]
                mctnodes[state] = {
                    True: previous['true'],
                    False: previous['false']
                }
        return mctnodes
    
    @staticmethod
    def save(path, mctnodes):
        print('save!')
        b = json.dumps(mctnodes)
        f2 = open(path, 'w')
        f2.write(b)
        f2.close()
        return


