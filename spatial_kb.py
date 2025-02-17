# -*- coding: utf-8 -*-
"""
@author: asenic co-jointly with GPT-4o
"""
from psychopy import visual, event, core, data, gui
import random
import csv
import pandas as pd
import os

class Experiment:
    def __init__(self, win_color, txt_color):
        self.win_color = win_color
        self.txt_color = txt_color

    def settings(self):
        experiment_info = {'Subid': '', 'Age': '', 'Experiment Version': 1,
                           'Sex': ['Male', 'Female'],
                           u'date':
                               data.getDateStr(format="%Y-%m-%d_%H:%M"), 'Inversion': ['No', 'H', 'V', 'HV']}

        info_dialog = gui.DlgFromDict(title='Spatial Test', dictionary=experiment_info, fixed=['Experiment Version'])
        experiment_info[u'DataFile'] = u'Data' + os.path.sep + u'spatial_kbrt.csv'

        if info_dialog.OK:
            return experiment_info
        else:
            core.quit()
        return 'Cancelled'

if __name__ == "__main__":
    background = "Gray"
    back_color = (0, 0, 0)
    textColor = "Silver"
    experiment = Experiment(win_color=background, txt_color=textColor)    
    settings = experiment.settings()
    
    # Create a list to store results
    results = []
    
    # Screen settings
    win = visual.Window(fullscr=True, color='gray', units='pix')

    # Circle parameters
    circle_radius = 0.05 * win.size[0] / 2  # radius of the circle (5% of screen width)
    circle_color = 'white'

   # Define circle positions on sides of the screen with offsets    
    offset_pixels = 50

    positions = {
        'left': (-win.size[0] / 2 + circle_radius + offset_pixels, 0),  # Left side
        'right': (win.size[0] / 2 - circle_radius - offset_pixels, 0),  # Right side
        'top': (0, win.size[1] / 2 - circle_radius - offset_pixels),  # Top side
        'bottom': (0, -win.size[1] / 2 + circle_radius + offset_pixels)  # Bottom side
    }

    # Main experiment loop    
    for _ in range(100):  # Number of repetitions
        
        # Check for exit keys before showing stimuli
        keys = event.getKeys()
        if 'escape' in keys or 'q' in keys:  # Allow exit with Esc or Q
            break
    
        # Fixation stimulus
        fixation = visual.TextStim(win, text='+', color='black', height=50)
        fixation.draw()
        win.flip()

        # Move the mouse cursor to the fixation point
        fixation_pos = (0, 0)  # Center of the screen
        event.Mouse(win=win).setPos(fixation_pos)

        core.wait(1)  # Wait for 1 second

        # Select a random stimulus
        target_stimulus = random.choice(list(positions.keys()))
        target_pos = positions[target_stimulus]

        # Create target circle
        target_circle = visual.Circle(win, radius=circle_radius, fillColor=circle_color, lineColor=circle_color)
        target_circle.pos = target_pos

        # Display the circle and measure reaction time
        target_circle.draw()
        win.flip()
        
        start_time = core.getTime()
        
        # Wait for keyboard input
        while True:
            keys = event.getKeys()
            if 'escape' in keys or 'q' in keys:  # Allow exit with Esc or Q
                win.close()
                core.quit()
            if keys:
                reaction_time = core.getTime() - start_time
                
                # Check correctness of the choice based on the key pressed
                correct_choice = (target_stimulus == 'left' and 'left' in keys) or (target_stimulus == 'right' and 'right' in keys) or (target_stimulus == 'top' and 'up' in keys) or (target_stimulus == 'bottom' and 'down' in keys)

                results.append({
                    "stimulus": target_stimulus,
                    "Accuracy": int(correct_choice),
                    "RT": reaction_time,
                    "inversion": settings['Inversion'],
                    'subid': settings['Subid'],
                    'age': settings['Age'],
                    'sex': settings['Sex'],
                    "date": settings['date']
                })    
                break
    
    # Close the window
    win.close()

# Create DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv('spatial_rt.csv', index=False)
print("Results saved to spatial_kbrt.csv")
