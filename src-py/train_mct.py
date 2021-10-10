"""
run the file by `python3 src-py/train_mct.py`
"""

from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
import json
import time

def mix_pretrain(n_game):

    shared_dict = {}
    # 4 of players boost by greedy
    players = [MCTAgent(name='m1', sharedMctNodes=shared_dict, isTest=True), 
        MCTAgent(name='m2', sharedMctNodes=shared_dict, isTest=True),  
        MCTAgent(name='m3', sharedMctNodes=shared_dict, isTest=True),  
        MCTAgent(name='m4', sharedMctNodes=shared_dict),  
        MCTAgent(name='m5', sharedMctNodes=shared_dict)]

    last_save = time.time()

    

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    for game_ind in range(n_game):
        game = Game(players)

        # before play, recovery from copy.deepcopy of agent
        for agent in game.agents:
            agent.mctNodes = shared_dict

        game.play()

        # update score board
        for agent in game.agents:
            if agent.is_spy():
                scoreboard[agent.name]['spy'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost >= 3:
                    scoreboard[agent.name]['spy'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            else:
                scoreboard[agent.name]['resistance'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost < 3:
                    scoreboard[agent.name]['resistance'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            
            if ((game_ind+1) % 50 == 0):
                print(agent.name, scoreboard[agent.name])

        if time.time() - last_save > 60:
            last_save = time.time()
            MCTAgent.save('mctnodes_dict.json', shared_dict)
    
    MCTAgent.save('mctnodes_dict.json', shared_dict)






mix_pretrain(100000)