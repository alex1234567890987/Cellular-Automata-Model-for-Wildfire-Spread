# Simulating the spread of the forest fire in CAPyLE

Added new cellular automata description for `forest_fire_spread.py` that simulates spread of forest fire caused by incinerator or/and powerplant.


![Gif1_north_prevailing ](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/6d381b87-80c3-4918-a7dd-ba70782ddcaf)


Simulation of the fire spreading on a 2D grid with the prevailing north wind effect. (Wind direction set to North and wind velocity set to 1)

Our model defines terrain types with different propabilities of catching a fire and different burn times.

- Dense forest (dark green colour), difficult to ignite but can burn for up to one month (30 days = 180 generations). 
- Chaparral (light green colour), catches fire quite easily, can burn for a period of several days (7 days = 42 generations).
- Canyon (yellow colour), very easy to catch fire, but burns for only several hours (12 hours = 3 generations).
- Lake (blue colour), can't be ignited.
- Fire break (brown colour), can't be ignited.

## Instructions to run the forest_fire_spread.py

### 1. How to select the start point of the fire
The model can be used to explore different scenarios of the starting point of the fire ignition. Set the `CHOSEN_START_IGNITION` to `POWERPLANT_IGNITE` (to simulate the fire starting at the powerplant) or `INCINERATOR_IGNITE` (to simulate the fire starting at the incinerator) or `BOTH_IGNITE` (to simulate the fire starting at both powerplant and the incinerator). (line 46)

The section of code responsible to adjust the short term intervention:
![image](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/0c9d7200-82c6-4370-8d6d-6ee8598b618b)

After setting the desired values run the code as usual.

### 2. How to set the wind direction and velocity
Our model takes into acount wind direction and velocity affecting spread of fire. In forest_fire_spread.py there are the velocity constant `V` and the wind direction constant `WIND_DIR` that can be adjusted simulationg different wind effect. After setting the constants to their new values make sure to save and open the file in Capyle again. 

The lines of code to adjust the wind direction and velocity:
![image](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/5247fae2-c451-4383-a4b4-3bfff331326a)

After setting the desired values run the code as usual.

### 3. How to set and run the short term intervention  
The model can simulate short intervention of dropping 12.5 km^2 of water in the different intervention times and different areas. The short intervention can be activated by setting the boolean constant `SHORT_TERM_INTERVENTION` to True in line 56. 

Set the `CHOSEN_SHORT_TERM_INT` to `WATER_DROP_INCINERATOR` (drops water on to the incinerator on `INTERVENTION_TIME_INCINERATOR = 15`) or to 
`WATER_DROP_TOWN` (drops water close to the town on `INTERVENTION_TIME_INCINERATOR = 300`). The intervention time and coordinates can be also adjusted for each short term intervention. (Set different coordinates for `WATER_DROP_COORDS_INCINERATOR` and `WATER_DROP_COORDS_TOWN` to change the water drop place)

The section of code responsible to adjust the short term intervention:
![image](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/4cc86c90-31ed-41b6-955b-f7b544d35dd8)

After setting the desired values run the code as usual.

### 4. How to set the long intervention
The short intervention can be activated by setting the boolean constant `LONG_TERM_INTERVENTION` to True in line 75. 

The model includes 2 types of possible intervention:
- Replacing three different areas with the dense forest to slow down the possible fire spread. In our model we suggest to extend the dense forest in three different areas. The first is to extend the alreasdy existing one to surround the town completly (To choose this intervention set the `CHOSEN_LONG_TERM_INT` to `EXTEND_FOREST_1`). The second option is to surround the incinerator wiht the dense forest (To choose this intervention set the `CHOSEN_LONG_TERM_INT` to `EXTEND_FOREST_2`). The thirs option is to surround the canyon with the dense forest (To choose this intervention set the `CHOSEN_LONG_TERM_INT` to `EXTEND_FOREST_3`)
  
The section of code responsible to adjust the long term intervention:
![image](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/03df31ac-c32e-486a-a3d2-07100d740c05)

After setting the desired values run the code as usual.

### 5. How to look for the results of each simulation

Once the CA configuration is applied the program reports the results (how many generation it took for the fire to reach the town) in the command promt:

![image](https://github.com/Anastasiia66/bioinspired_ca_forest_fire_spread/assets/84929481/02dc8944-6426-4b96-a50c-2d496661fce0)

# CAPyLE
CAPyLE is a cross-platform teaching tool designed and built as part of a final year computer science project. It aims to aid the teaching of cellular automata and how they can be used to model natural systems.

It is written completely in python with minimal dependencies.

![CAPyLE Screenshot on macOS](http://pjworsley.github.io/capyle/sample.png)

## Installation
The installation guide can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/installationguide.html)

## Usage
Detailed usage can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/).

See below for a quickstart guide:

1. `git clone https://github.com/pjworsley/capyle.git [target-directory]`
2. `cd [target-directory]`
3. Execute main.py either by:
    * `run.bat` / `run.sh`
    * `python main.py`
2. Use the menu bar to select File -> Open. This will open in the folder `./ca_descriptions`.
3. Open one of the example files;
  - `wolframs_1d.py` is Wolfram's elementary 1D automata
  - `gol_2d.py` is Conway's 2D game of life
4. The main GUI elements will now load, feel free to customise the CA parameters on the left hand panel
5. Run the CA with your parameters by clicking the bottom left button 'Apply configuration & run CA'
6. The progress bar will appear as the CA is run
7. After the CA has been run, use the playback controls at the top and the slider at the bottom to run through the simulation.
8. You may save an image of the currently displayed output using the 'Take screenshot' button

## Acknowledgements
Special thanks to [Dr Dawn Walker](http://staffwww.dcs.shef.ac.uk/people/D.Walker/) for proposing and supervising this project.

Also thanks to the COM2005 2016/2017 cohort for being the guinea-pigs!

## Licence
CAPyLE is licensed under a BSD licence, the terms of which can be found in the LICENCE file.

Copyright 2017 Peter Worsley
