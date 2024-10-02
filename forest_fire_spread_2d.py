import numpy as np
import sys
import inspect
import math
import random

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils

'''Constants'''

SCALE_FACTOR = 0.2  # A scaling factor for some probabilities
P_0 = 0.58 * SCALE_FACTOR  # Base ignition probability
P_W = 1.0  # Wind factor (can be adjusted)
P_VEG = {'chaparral': 0.2, 'canyon': 1.0, 'forest': -0.5, 'lake': -1.0, 'town': 1.0,
         'fire_break': -1.0}  # Ignition probabilities for different terrain types

C_1 = 0.045  # Wind effect constant
C_2 = 0.131  # Wind effect constant

V = 1  # Wind velocity (can be adjusted)
WIND_DIR = 'N'  # Wind direction (can be adjusted)
COS_VALS = {'NW': [1.0, 0.707107, 0, 0.707107, -0.707107, 0, -0.707107, -1.0],
            'N': [0.707107, 1.0, 0.707107, 0, 0, -0.707107, -1.0, -0.707107],
            'NE': [0, 0.707107, 1.0, -0.707107, 0.707107, -1.0, -0.707107, 0],
            'W': [0.707107, 0, -0.707107, 1.0, -1.0, 0.707107, 0, -0.707107],
            'E': [-0.707107, 0, 0.707107, -1.0, 1.0, -0.707107, 0, 0.707107],
            'SW': [0, -0.707107, -1.0, 0.707107, -0.707107, 1.0, 0.707107, 0],
            'S': [-0.707107, -1.0, -0.707107, 0, 0, 0.707107, 1.0, 0.707107],
            'SE': [-1.0, -0.707107, 0, -0.707107, 0.707107, 0, 0.707107, 1.0]}
             # Cosine values corresponding to wind directions

'''Start of the ignition control'''

POWERPLANT_IGNITE = 0  # if only powerplant ignites
INCINERATOR_IGNITE = 1  # if only incinerator ignites
BOTH_IGNITE = 2  # if both ignite similtanously

CHOSEN_START_IGNITION = INCINERATOR_IGNITE  # adjust to change start of ignition

'''Short intervention control'''

WATER_DROP_INCINERATOR = 0
WATER_DROP_TOWN = 1

CHOSEN_SHORT_TERM_INT = WATER_DROP_TOWN  # Choose the short term intervention to run from the
                                        # list above

SHORT_TERM_INTERVENTION = False  # false : OFF, true : ON (ADJUST TO CHANGE)

INTERVENTION_TIME_INCINERATOR = 15  # Time step for intervention (can be adjusted)
INTERVENTION_TIME_TOWN = 300  # Time step for intervention (can be adjusted)

WATER_DROP_COORDS_INCINERATOR = [0, 14, 186, 200]
WATER_DROP_COORDS_TOWN = [160, 190, 45, 52]

'''Long intervention control'''

# All possible long term interventions
EXTEND_FOREST_1 = 0
EXTEND_FOREST_2 = 1
EXTEND_FOREST_3 = 2
FIRE_BREAK = 3

CHOSEN_LONG_TERM_INT = EXTEND_FOREST_1  # Choose the long term intervention to run from the
                                        # list above

LONG_TERM_INTERVENTION = False  # false : OFF, true : ON (ADJUST TO CHANGE)


def report_outcome(counter):
    """Prints information about the simulation outcome."""
    print('Wind directions:', WIND_DIR,
          'Wind velocity:', V,
          'Town reached at:', int(counter[0]))

def is_town_reached(grid):
    """Checks if the town has been reached based on the grid state."""
    town = grid[175:185, 35:45]
    return np.any(town == 5)

def short_term_intervention(counter, grid):
    """Performs short-term interventions."""
    if SHORT_TERM_INTERVENTION == True:
        if CHOSEN_SHORT_TERM_INT == WATER_DROP_INCINERATOR:
            if CHOSEN_START_IGNITION == INCINERATOR_IGNITE:
                if counter[0] == INTERVENTION_TIME_INCINERATOR:
                    water_grid = np.full(grid.shape, False)
                    water_grid[WATER_DROP_COORDS_INCINERATOR[0]:WATER_DROP_COORDS_INCINERATOR[1],
                    WATER_DROP_COORDS_INCINERATOR[2]:WATER_DROP_COORDS_INCINERATOR[3]] = True
                    grid[water_grid] = 3
        elif CHOSEN_SHORT_TERM_INT == WATER_DROP_TOWN:
            if counter[0] == INTERVENTION_TIME_TOWN:
                water_grid = np.full(grid.shape, False)
                water_grid[WATER_DROP_COORDS_TOWN[0]:WATER_DROP_COORDS_TOWN[1],
                WATER_DROP_COORDS_TOWN[2]:WATER_DROP_COORDS_TOWN[3]] = True
                grid[water_grid] = 3

def long_term_intervention(grid):
    """Performs long-term interventions."""
    if LONG_TERM_INTERVENTION == True:
        grid_array = grid

        if CHOSEN_LONG_TERM_INT == EXTEND_FOREST_1:
            # if forest_extended (1200 cells)
            grid_array[140:200, 60:80] = 2  # 60x20 = 1200 cells

        if CHOSEN_LONG_TERM_INT == EXTEND_FOREST_2:
            # if forest_extended (1200 cells)
            grid_array[0:39, 159:179] = 2  # 40x20 = 800 cells
            grid_array[19:39, 179:200] = 2  # 20x20 = 400 cellss

        if CHOSEN_LONG_TERM_INT == EXTEND_FOREST_3:
            # if forest_extended (1280 cells)
            grid_array[10:190, 137:140] = 2  # 180x3 = 540 cells
            grid_array[10:190, 150:153] = 2  # 180x3 = 540 cells
            grid_array[10:20, 140:150] = 2  # 10x10 = 100 cells
            grid_array[180:190, 140:150] = 2  # 10x10 = 100 cells

        elif CHOSEN_LONG_TERM_INT == FIRE_BREAK:

            # if fire_breaks
            grid_array[0:40, 160:161] = 7
            grid_array[40:41, 160:200] = 7
            # grid_array[40, 161] = 2


def transition_func(grid, neighbourstates, neighbourcounts, fuel_grid, reached_town, counter):
    """Transition rules for the cellular automaton."""
    counter += 1
    # Update burning cells and fuel grid
    burning_cells = (grid == 5)
    fuel_grid[burning_cells] -= 1

    # Set up grid with base burn probabilities for each cell
    ignite_prob_grid = setup_ignite_probabilities_grid(grid)

    # Calculate wind effect
    wind_prob_grid = calculate_wind_effect(grid, neighbourstates)

    # Update ignite probabilities grid based on wind effect
    ignite_prob_grid *= wind_prob_grid

    # Generate random numbers to test against probabilities
    random_grid = np.random.rand(*grid.shape)

    # Identify cells to ignite and set them to burning state
    cells_to_ignite = random_grid < ignite_prob_grid
    grid[cells_to_ignite] = 5

    # Identify cells which ran out of fuel and set them to dead state
    dead_cells = (fuel_grid == 0)
    grid[dead_cells] = 6

    # Do water drop at intervention time if it's active
    if SHORT_TERM_INTERVENTION == True:
       short_term_intervention(counter, grid)

    # Check if we reached the town
    if not np.any(reached_town):
        reached_town[0] = is_town_reached(grid)
        if np.any(reached_town):
            report_outcome(counter)

    return grid

def setup(args):
    """Initializes the configuration for the cellular automaton."""
    config_path = args[0]
    config = utils.load(config_path)

    config.title = "The Spread of a Forest Fire"
    config.dimensions = 2
    
    # states:
    # 0 - chaparral
    # 1 - canyon
    # 2 - forest
    # 3 - lake
    # 4 - town
    # 5 - burning
    # 6 - burnt
    # 7 - fire break
    
    config.states = (0, 1, 2, 3, 4, 5, 6,7)
    config.grid_dims = (200, 200)

    colours = {
        "chaparral": (0.7, 0.7, 0.2),
        "canyon": (0.9, 1, 0),
        "forest": (0.3, 0.4, 0),
        "lake": (0.4, 0.8, 1),
        "town": (0, 0, 0),
        "burning": (0.7, 0, 0.1),
        "burned": (0.4, 0.4, 0.4),
        "fire_break": (0.3, 0.1, 0)
    }
    config.state_colors = list(colours.values())

    config.wrap = False
    config.num_generations = 500

    # Set up initial grid state based on terrain types and ignition sources
    grid_array = initialize_grid()

    config.set_initial_grid(grid_array)

    if len(args) == 2:
        config.save()
        sys.exit()

    return config

def setup_fuel_grid(grid):
    """Initializes the fuel grid based on terrain types."""
    fuel_grid = np.zeros(grid.shape)
    fuel_grid[grid == 0] = 42  # chaparral
    fuel_grid[grid == 1] = 3   # canyon
    fuel_grid[grid == 2] = 180  # forest
    fuel_grid[grid == 3] = -1  # lake
    fuel_grid[grid == 4] = 5   # town
    fuel_grid[grid == 7] = -1  # fire_break
    return fuel_grid

def setup_ignite_probabilities_grid(grid):
    """Initializes the ignition probabilities grid based on terrain types."""
    ignite_grid = np.zeros(grid.shape)
    ignite_grid[grid == 0] = P_VEG['chaparral']
    ignite_grid[grid == 1] = P_VEG['canyon']
    ignite_grid[grid == 2] = P_VEG['forest']
    ignite_grid[grid == 3] = P_VEG['lake']
    ignite_grid[grid == 4] = P_VEG['town']
    ignite_grid[grid == 7] = P_VEG['fire_break']
    ignite_grid += 1
    ignite_grid *= P_0
    return ignite_grid

def initialize_grid():
    """Sets up the initial grid state based on terrain types and ignition sources."""
    grid_array = np.zeros((200, 200))
    grid_array[100:140, 0:80] = 2  # forest
    grid_array[20:180, 140:150] = 1  # canyon
    grid_array[20:80, 60:80] = 3  # lake
    grid_array[175:185, 35:45] = 4  # town
    
    if CHOSEN_START_IGNITION == 0:
        grid_array[0][39] = 5  # initial burning cell (top left corner)
    elif CHOSEN_START_IGNITION == 1:
        grid_array[0][199] = 5  # initial burning cell (top right corner)
    else:
        grid_array[0][39] = 5  # initial burning cell (top left corner)
        grid_array[0][199] = 5  # initial burning cell (top right corner)

    # Set the long term intervention if it's active
    if LONG_TERM_INTERVENTION == True:
       long_term_intervention(grid_array)
    
    return grid_array

def calculate_wind_effect(grid, neighbourstates):
    """Calculates the wind effect on ignition probabilities."""

    wind_prob_grid = np.zeros(grid.shape)
    # For each direction calculate ignition probability depending on wind direction
    for (direction, cos_a) in zip(neighbourstates, COS_VALS[WIND_DIR]):
        curr_direction_burning = (direction == 5)
        # update wind probability grid
        # P_W = exp[V(c1 + c2(cos(a) - 1))]
        # where a is angle between wind direction and current burning direction
        wind_prob_grid[curr_direction_burning] += math.exp(V * (C_1 + C_2 * (cos_a - 1)))

    return wind_prob_grid

def main():
    """Orchestrates the setup, runs the cellular automaton, and saves results."""
    config = setup(sys.argv[1:])

    # Create fuel and ignite probabilities numpy arrays
    fuel_grid = setup_fuel_grid(config.initial_grid)

    # Create grid object
    reached_town = np.array([False])
    counter = np.array([0])
    grid = Grid2D(config, (transition_func, fuel_grid, reached_town, counter))

    # Run the cellular automaton and save results
    timeline = grid.run()

    # Save updated config to file
    config.save()
    # Save timeline to file
    utils.save(timeline, config.timeline_path)

if __name__ == "__main__":
    main()
