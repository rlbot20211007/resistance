from typing import List
from resistance.game import Game
from resistance.random_agent import RandomAgent

def test(n_game, players:List[RandomAgent]):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)
        game.play()
        for agent in players:
            if agent.is_spy():
                scoreboard[agent.name]['spy'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost >= 3:
                    scoreboard[agent.name]['spy'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            else:
                scoreboard[agent.name]['resistance'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost >= 3:
                    scoreboard[agent.name]['resistance'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            
            print(agent.name, scoreboard[agent.name])

agents = [RandomAgent(name='r1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7')]

test(2, agents)                



