import bpy
import csv

# Define the path to your CSV file
file_path = '/Users/gregniemeyer/Documents/WaterProjects/WeatherMirror/github/water_mirror/data/normalized_sun_altitude_data_jun2023_to_jun2024.csv'
scale = 0.83
# Ensure the object "Sun" exists in the scene
sun_obj = bpy.data.objects.get("Sun")
if not sun_obj:
    raise Exception('The object "Sun" does not exist in the scene.')

# Ensure the material "sun_material" exists and has the node "Value"
sun_material = bpy.data.materials.get("sun_material")
if not sun_material:
    raise Exception('The material "sun_material" does not exist.')

# Access the "Value" node within the material node tree
value_node = sun_material.node_tree.nodes.get("Value")
if not value_node:
    raise Exception('The node "Value" does not exist in the material "sun_material".')

# Open and read the CSV file
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)

    # Iterate through each row in the CSV
    for row in reader:
        # Parse the necessary values from the row
        frame = int(row['index'])  # Assuming 'index' column is the frame number
        change = row['change'].lower() == 'true'  # Check if the 'change' column is True
        z_value = float(row['normalized_sun_altitude'])  # Get the Z location value
        
        # If 'change' is True, set keyframes for both the object and material node
        if change:
            # Set keyframe for Z location of "Sun" object
            sun_obj.location[2] = z_value
            sun_obj.keyframe_insert(data_path="location", index=2, frame=frame)

            # Set keyframe for the "Value" node's default_value
            value_node.outputs[0].default_value = z_value*scale
            value_node.keyframe_insert(data_path="outputs[0].default_value", frame=frame)

print("Keyframes set for 'Sun' object and 'Value' node in 'sun_material'.")
