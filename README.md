
# Multi-agent particle env for aerial unmanned vehicles

  This repository is built upon on [multiagent-particle-envs](https://github.com/openai/multiagent-particle-envs) and provides a set of environments with a variety of realistic constraints to simulate aerial anmanned vehicles settings with realistic constraints.

## Scenarios

The goal of all the scenarios is to have each drones reaching their targets under certain conditions:

- drones_wind_battery_a4.py: normal battery and wind conditions
- drones_wind_battery_a4_battery02.py: starting battery capacity is very low
- drones_wind_battery_a4_wind1.py: very strong wind conditions
- drones_wind_battery_moving_a4.py: targets are not static but are randomly moving around
- drones_wind_battery_po_a4.py: agents have limited vision
- drones_wind_battery_moving_a4_hard.py: all the previous constraints are mixed together


  

## Set environment

1. Create conda env

`conda create -y -n auv python=3.9 anaconda `

2. Enable conda env

` conda activate auv`

3. Install possible dependencies

1.  `pip install PyHamcrest==1.9.0`

2.  `pip install install gym==0.7.3`

4. Install drones env

1.  `cd unmanned-aerial-vehicles-marl-env`

2.  `pip install -e .`

  

## Testing

- Interactive testing:

`python bin/interactive.py`

- Random generated episodes:

`python example_env_interaction.py`
