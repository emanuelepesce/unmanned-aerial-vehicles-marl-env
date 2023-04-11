# Drone Visualisation Executables for Windows and Linux

To use either executable, you will need to unzip the files.
Once unzipped follow these instructions to load user episodes, depending on platform:

## Windows

- Run WMG_Drone_Visualisation.exe
- Navigate to the "AppData" folder
- Then navigate to the folder: AppData/LocalLow/WMG/WMG_Drone_Visualisation/UserData
- Once in this folder, you can drop any user created episodes.
- Then Click "Refresh Database" in the executable
- A list of episodes names should now present, click on one to run the episode visualisation

## Linux

- Run Drone_Visualisation_Linux.86_64
- Navigate to the ".config" folder
- Then navigate to the folder: .config/unity3d/WMG/WMG_Drone_Visualisation/UserData
- Once in this folder, you can drop any user created episodes.
- Then Click "Refresh Database" in the executable
- A list of episodes names should now present, click on one to run the episode visualisation

## Scene Controls

<img src='SceneInformation.png' width='360'>

- **1**: Play or Pause the Simulation at it's current step. Also displays the current step number and the total number of steps
- **2**: Sliders to change the step speed,(larger number = slower simulation) and also the drone scale.
- **3**: Current Wind Speed and Wind Direction Values
- **4**: The Drone battery level

## File Formatting
The files for user made episodes need to be in a .json format. The structure of which needs to look as follows. Any deviation from this will result in an error and not display in the list.
