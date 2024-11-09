import bpy
import pandas as pd
from mathutils import Color

# Load the CSV file
file_path = "/Users/gregniemeyer/Documents/Art Projects/WaterMirror/github/data/sst_all.csv"
data = pd.read_csv(file_path)

# Access the color ramp elements
material = bpy.data.materials.get("sst_gradient")
if material is None:
    raise ValueError("Material 'sst_gradient' not found.")

color_ramp = material.node_tree.nodes["Color Ramp"].color_ramp

# Define a function to map values from 0-1 to colors between blue and red
def value_to_color(value):
    color = Color((0, 0, 0))  # Initialize as black
    if value <= 0.25:
        color.r = 0.0
        color.g = value / 0.25
        color.b = 1.0 - color.g
    elif value <= 0.5:
        color.r = (value - 0.25) / 0.25
        color.g = 1.0
        color.b = 0.0
    elif value <= 0.75:
        color.r = 1.0
        color.g = 1.0 - (value - 0.5) / 0.25
        color.b = 0.0
    else:
        color.r = 1.0
        color.g = (1.0 - value) / 0.25
        color.b = 0.0
    return color

# Iterate through the first 2000 rows of the data
num_rows = min(2000, len(data))
for frame in range(num_rows):
    # Get values from the CSV file (assuming they are in the first 4 columns for the 4 color stops)
    values = data.iloc[frame, :4]
    
    for i, val in enumerate(values):
        if i >= len(color_ramp.elements):
            break  # Ensure we don't exceed available color stops
            
        # Map the value to the color
        color = value_to_color(val)
        
        # Set the color for the color ramp element
        color_ramp.elements[i].color = (color.r, color.g, color.b, 1.0)  # RGBA
        
        # Insert a keyframe for the color at the specified frame
        color_ramp.elements[i].keyframe_insert(data_path="color", frame=frame)

print("Keyframes set for the color ramp from frame 0 to", num_rows - 1)
