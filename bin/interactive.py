#!/usr/bin/env python
import os,sys

import pandas as pd

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import argparse
import time

from scipy.spatial import distance

from multiagent.environment import MultiAgentEnv
from multiagent.policy import InteractivePolicy
import multiagent.scenarios as scenarios

import pdb 

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
    from multiagent.environment import MultiAgentEnv

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
                            scenario.observation, discrete_action=discrete_action,shared_viewer=False)
    return env

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description=None)
    env = make_env('drones_wind_battery_a4_v2_battery03')
    # print(env.landmarks)
    env.render()
    # create interactive policies for each agent
    policies = [InteractivePolicy(env,i) for i in range(env.n)]
    # execution loop
    obs_n = env.reset()
    while True:
        start = time.time()
        # query for action from each agent's policy
        act_n = []
        for i, policy in enumerate(policies):
            act_n.append(policy.action(obs_n[i]))
        # step environment
        print('===> Observations:')
        print(obs_n[0])
        obs_n, reward_n, done_n, _ = env.step(act_n)
        print('===> Rewards:')
        print(format(reward_n))
        # render all agent views
        env.render()
        end = time.time()
        elapsed = end - start
        time.sleep(max(1 / 30 - elapsed, 0))
        # display rewards
        #for agent in env.world.agents:
        #    print(agent.name + " reward: %0.3f" % env._get_reward(agent))
        for rew in reward_n:
            if rew < -40:
                print(" ===> Collision happened! press c t continue")
                # pdb.set_trace()
