"""
drones_wind_battery_a4_v4

IN v2 agents can see always see their targets and other agents if they fall 
in the vision range
"""
import numpy as np
from multiagent.core import World, Agent, Landmark
from multiagent.scenario import BaseScenario
from random import shuffle
import copy
from scipy.spatial import distance

class Scenario(BaseScenario):
    def make_world(self):
        world = World()
        # set any world properties first
        world.dim_c = 2
        world.alpha = 1.e-2
        world.beta = 1.e-3

        max_vision = 1
        value_outvision = 7

        self.num_agents = 4
        self.num_landmarks = self.num_agents
        self.max_wind_speed = 0.1
        self.wind_speed = None
        self.wind_direction = None

        self.r_target_reached = 0
        self.p_collision = 50
        self.p_battery_out = 0
        self.p_battery_distance = True
        self.p_collision_distance = True



        # generate random colors
        rcolor = lambda: list(np.random.uniform(0, 1, 3))
        self.colors = [rcolor() for _ in range(self.num_agents)]
        # add agents
        world.agents = [Agent() for i in range(self.num_agents)]
        for i, agent in enumerate(world.agents):
            agent.name = 'agent %d' % i
            agent.collide = True
            agent.silent = True
            agent.size = 0.07
            agent.max_vision = max_vision
            agent.value_outvision = value_outvision
            agent.id = i
        # add landmarks
        world.landmarks = [Landmark() for i in range(self.num_landmarks)]
        for i, landmark in enumerate(world.landmarks):
            landmark.name = 'landmark %d' % i
            landmark.collide = False
            landmark.movable = False
            landmark.id = i

        # make initial conditions
        self.reset_world(world)
        return world

    def reset_world(self, world):
        # random properties for agents

        # set random initial states
        for agent in world.agents:
            agent.state.p_pos = np.random.uniform(-4.5, +4.5, world.dim_p)
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.c = np.zeros(world.dim_c)
            agent.state.energy = 1.0  # could be also random!
        for i, landmark in enumerate(world.landmarks):
            landmark.state.p_pos = np.random.uniform(-4.5, +4.5, world.dim_p)
            landmark.state.p_vel = np.zeros(world.dim_p)

        # Landmark - Agent random assignment 
        randi = list(range(self.num_agents))
        shuffle(randi)
        for i in range(len(randi)):
            world.landmarks[i].color = self.colors[i]
            world.agents[i].color = self.colors[i]
            world.agents[i].target = world.landmarks[i].id


        # random wind
        if self.wind_speed is None:
            world.wind_speed = np.random.uniform(0., self.max_wind_speed)

        if self.wind_direction is None:
            world.wind_direction = np.random.uniform(0., 360.)

    def benchmark_data(self, agent, world):
        collisions = 0
        landmark_reached = 0
        landmark_pos = []

        # calculate distange between agent and target
        tdistance = world.distance_to_target(agent)

        # if target is reached assign high reward
        rew = 0

        # agent has arrived (i.e., is on ground)
        if tdistance < agent.size * 2:
            rew += self.r_target_reached
            landmark_reached = True
        else:
            # agent has not arrived
            if agent.state.energy == 0:
                rew -= self.p_battery_out
                if self.p_battery_distance:
                    rew -= tdistance
            else:
                collides = False

                # penalize in case of collisions with another agent (both must be airborne)
                if agent.collide:
                    for a in world.agents:
                        if a.id != agent.id and a.collide:
                            if self.is_collision(a, agent):
                                collides = True
                                collisions += 1
                                rew -= self.p_collision

                if not collides or self.p_collision_distance:
                    rew -= tdistance

        for i, landmark in enumerate(world.landmarks):
            landmark_pos.append(landmark.state.p_pos.tolist())

        return rew, collisions, landmark_reached, landmark_pos

    def reward(self, agent, world):
        # REWARD IS NOT SHARED HERE, NEEDS TO BE SHARED LATER IN THE CODE

        # calculate distange between agent and target
        tdistance = world.distance_to_target(agent)

        # if target is reached assign high reward
        rew = 0

        # agent has arrived (i.e., is on ground)
        if tdistance < agent.size * 2:
            rew += self.r_target_reached
        else:
            # agent has not arrived to the target
            if agent.state.energy == 0:
                rew -= self.p_battery_out
                if self.p_battery_distance:
                    rew -= tdistance
            else:
                collides = False

                if agent.collide:
                    for a in world.agents:
                        if a.id != agent.id and a.collide:
                            if self.is_collision(a, agent):
                                collides = True
                                rew -= self.p_collision

                if not collides or self.p_collision_distance:
                    rew -= tdistance

        return rew

    def is_collision(self, agent1, agent2):
        delta_pos = agent1.state.p_pos - agent2.state.p_pos
        dist = np.sqrt(np.sum(np.square(delta_pos)))
        dist_min = agent1.size + agent2.size
        return True if dist < dist_min else False

    def observation(self, agent, world):
        # landmark position in dataframe
        # get positions of all entities in this agent's reference frame
        entity_pos = []
        for entity in world.landmarks:  # world.entities:
            if entity.id == agent.target:
                entity_pos.append(entity.state.p_pos - agent.state.p_pos)



        # other agents' positions in vision range
        other_pos = []
        for other in world.agents:
            if other is agent: continue
            rpos = other.state.p_pos - agent.state.p_pos
            d = distance.euclidean(other.state.p_pos,agent.state.p_pos)
            if np.abs(d) > agent.max_vision:
                for i in range(rpos.shape[0]):
                    rpos[i] = agent.value_outvision
            other_pos.append(rpos)


        # wind
        wind = np.append(world.wind_components, world.wind_speed)

        return np.concatenate([agent.state.p_vel] +  # speed
                              [np.array([agent.state.energy])] +  # energy
                              [wind] +  # wind
                              entity_pos  + # relative position of target
                              other_pos
                              )
