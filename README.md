# Tkinter-DataStructures

E-SPORTS Results Tracker using custom built data structures in Python. Uses csv filing as the source of database and Tkinter as the GUI.

## Table of Contents

1. [Setup](#setup)
2. [Usage](#usage)
3. [Code Structure](#code-structure)
4. [Main Components](#main-components)
5. [Functionality](#functionality)
6. [Code Explanation](#code-explanation)

## Setup

1. Create a new Python virtual environment:

```bash
python3 -m venv esr_tracker_env
```

2. Activate the virtual environment:

3. Install required packages:

```bash
sudo apt install python3-tk
pip install tk
```

4. Clone the repository or create a new directory for your project.

## Usage

1. Navigate to the project directory in your terminal/command prompt.
2. Activate the virtual environment if not already active.
3. Run the application:

```bash
python esr_tracker.py
```

## Code Structure

The main file `esr_tracker.py` contains the following classes and functions:

- `ESRTracker`: The main application class
- `CustomDictionary`: A custom dictionary-like class for data storage
- Various methods for data manipulation and GUI creation

## Main Components

1. Admin Mode:
   - View, add, remove teams
   - View, add, remove games
   - Record match results

2. Non-Admin Mode:
   - View last 5 matches
   - View overall scoreboard
   - View game-specific scoreboard

## Functionality

- Data persistence using CSV files
- In-memory data storage using custom dictionary
- GUI implementation using tkinter
- CRUD operations for teams, games, and matches
- Score calculation and display

## Code Explanation

### Import Statements

```python
import csv
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
```

These imports are necessary for the GUI, CSV operations, and date handling.

### ESRTracker Class

#### Initialize data structures

```python
self.teams = {}  # Dictionary of team names
self.games = {}  # Dictionary of game names
self.matches = []  # List of match dictionaries
```

#### Load initial data

```python
self.load_data()
```

#### Create main menu and tkinter frame

```python
self.main_menu()

tk.Button(main_frame, text="Admin Mode", command=self.admin_mode).pack(pady=20)
tk.Button(main_frame, text="Non-Admin Mode", command=self.non_admin_mode).pack(pady=20)
```

### CRUD Operations

#### Create

The create operation typically involves:

1. User input through a GUI form
2. Validation of input data
3. Adding the new data to the in-memory structure
4. Saving the updated data to the corresponding CSV file
5. Updating the GUI to reflect the new data

```python
# Add to in-memory structure
self.teams.append([team_name, score])

# Save to CSV
self.save_data()

# Update GUI
self.view_teams()
```

#### Read

The read operation typically involves:

1. Loading data from the CSV file into the in-memory structure
2. Displaying the data in a GUI component (e.g., Treeview)

Example:

```python
# Insert new data
for team in self.teams:
    tree.insert('', 'end', values=(team[0], team[1]))
```

#### Update

The update operation typically involves:

1. Finding the item to update in the in-memory structure
2. Modifying the item
3. Saving the updated data to the CSV file
4. Updating the GUI to reflect the changes

Example:

```python
def update_team_score(self, team_name, new_score): 
    for i, team in enumerate(self.teams): 
        if team[0] == team_name: 
            self.teams[i][1] = new_score 
            break 
        self.save_data()
```

#### Delete

The delete operation typically involves:

1. Finding and removing the item from the in-memory structure
2. Saving the updated data to the CSV file
3. Updating the GUI to reflect the deletion

Example:

```python
def remove_team(self, team_name): 
    self.teams = [team for team in self.teams if team[0] != team_name] 
    self.save_data() 
    self.view_teams()
```

### Common Patterns

1. **Data Loading**: All data is loaded into memory when the application starts.
2. **GUI Updates**: After each CRUD operation, the relevant GUI component is updated to reflect the changes.
3. **CSV Operations**: Data is saved to CSV files after each create, update, or delete operation.
4. **Error Handling**: Basic error handling is implemented to manage invalid inputs or missing data.
5. **Consistent Naming**: Methods follow a consistent naming convention (e.g., `add_team`, `view_teams`, `remove_team`).

This consistent approach to CRUD operations makes the code more maintainable and easier to understand. It also allows for easy extension of functionality to other data sources if needed in the future.

### GUI Creation

The application uses tkinter for creating the GUI. Various methods create frames, buttons, labels, and treeviews to display data and provide user interaction.

### Data Manipulation

Methods like `add_team`, `remove_team`, `record_match`, etc., handle the logic for manipulating the data structures and updating the GUI accordingly.

This README provides a high-level overview of the E-Sports Results Tracker application. For a more detailed explanation of each method and its implementation, please refer to the comments in the `esr_tracker.py` file.

## Contributing

Contributions are welcome! Please submit a pull request with your changes and a brief explanation of what you've added or modified.
