"""
    Example file to interact with environments
"""
import numpy as np
import time
from make_env import make_env

def make_env(scenario_name, benchmark=False, discrete_action=True):
    '''
    Creates a MultiAgentEnv object as env. This can be used similar to a gym
    environment by calling env.reset() and env.step().
    Use env.render() to view the environment on the screen.

    Input:
        scenario_name   :   name of the scenario from ./scenarios/ to be Returns
                            (without the .py extension)
        benchmark       :   whether you want to produce benchmarking data
                            (usually only done during evaluation)
        discrete_action :    discrete actions

    Some useful env properties (see environment.py):
        .observation_space  :   Returns the observation space for each agent
        .action_space       :   Returns the action space for each agent
        .n                  :   Returns the number of Agents
    '''
    from multiagentsha.environment import MultiAgentEnv
    import multiagentsha.scenarios as scenarios

    # load scenario from script
    scenario = scenarios.load(scenario_name + ".py").Scenario()
    # create world
    world = scenario.make_world()
    # create multiagent environment
    if benchmark:        
        env = MultiAgentEnv(world, scenario.reset_world, scenario.reward,
                            scenario.observation, scenario.benchmark_data,
                             discrete_action=discrete_action)
    else:
        env = MultiAgentEnv(world, scenario.reset_world, scenario.reward,
                            scenario.observation, discrete_action=discrete_action)
    return env

# inizialize the environment object
env  = make_env('drones_wind_battery_a4')

# get some env properties
n_agents          = env.n                 # number of agents
observation_space = env.observation_space # observation space
action_space      = env.action_space      # action space

# print them to see their format
print("n_agents: {}".format(n_agents))
print("observation_space: {}".format(observation_space))
print("action_space: {}".format(action_space))


# This is the scheleton of a training process
# Each episode is composed by a specified number of time-steps (which
# so represent the length of each episode)
# At each time-step 
# - agents access to their current observations
# - chose the actions (in this case random) to do
# - send these actions to the environment which in return will send
# the current reward and the next observation

n_episodes  = 10
n_timesteps = 75

for e in range(n_episodes): # episodes start here
    # resetting the environement will give a new starting state
    # (we do this at the beginning of each episode)
    observation = env.reset()
    for t in range(n_timesteps): 
        # this is to render and it's completely optional
        # is not needed during the training
        env.render()            
        # import pdb

        # pdb.set_trace()

        # now we are going to take the actions for each agent
        agent_actions = [] # list containing the actions of all agents
        for i_agent in range(n_agents):

            # here i_agent will produce a random action
            # (in the real system this would done by our algo) 
            agent_action_space = env.action_space[i_agent]
            action             = agent_action_space.sample()    
            action_vec         = np.zeros(agent_action_space.n)
            action_vec[action] = action
            agent_actions.append(action_vec)

        # At this point we send the actions of all the agent to the
        # environment and in return he will return us:
        # observation: list of next observations (an observation for each agent)
        # reward: list of current reward (a reward for each agent)
        # done: list flags (1: episode finished, 0 episode not finished),
        # info: additional infos (can be optional)
        observation, reward, done, info = env.step(agent_actions)
        time.sleep(0.1)
