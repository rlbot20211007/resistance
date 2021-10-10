"""
run the file by `python src-py/test_1g6r.py`
the score board for 10 games 
('r5', {'spy': [2, 4], 'total': [6, 10], 'resistance': [4, 6]})
('r6', {'spy': [1, 5], 'total': [3, 10], 'resistance': [2, 5]})
('g1', {'spy': [1, 1], 'total': [7, 10], 'resistance': [6, 9]})
('r7', {'spy': [4, 6], 'total': [8, 10], 'resistance': [4, 4]})
('r3', {'spy': [0, 4], 'total': [2, 10], 'resistance': [2, 6]})
('r4', {'spy': [2, 4], 'total': [6, 10], 'resistance': [4, 6]})
('r2', {'spy': [2, 6], 'total': [4, 10], 'resistance': [2, 4]})
"""

from resistance.game import Game
from resistance.random_agent import RandomAgent
from resistance.mct.greedy_agent import GreedyAgent


def test(n_game, players):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)
        game.play()
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
            
            print(agent.name, scoreboard[agent.name])

agents = [GreedyAgent(name='g1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7')]

test(10, agents)                



