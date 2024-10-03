import bpy
import csv

# Define the path to your CSV file
file_path = 'Documents/WaterProjects/WeatherMirror/github/water_mirror/data/normalized_sun_altitude_data_jun2023_to_jun2024.csv'
scale = 0.83

# Ensure the object "Sun" exists in the scene
sun_obj = bpy.data.objects.get("Sun")
if not sun_obj:
    raise Exception('The object "Sun" does not exist in the scene.')

# Ensure the materials "sun_material" and "sky_material" exist and have the necessary nodes
sun_material = bpy.data.materials.get("sun_material")
sky_material = bpy.data.materials.get("sky_material")

if not sun_material:
    raise Exception('The material "sun_material" does not exist.')

if not sky_material:
    raise Exception('The material "sky_material" does not exist.')

# Access the "Value" node, "Emission" node, and other nodes within the materials
value_node_sun = sun_material.node_tree.nodes.get("Value")
emission_node_sun = sun_material.node_tree.nodes.get("Emission")

value_node_sky = sky_material.node_tree.nodes.get("Value")
emission_node_sky = sky_material.node_tree.nodes.get("Emission")

if not value_node_sun or not emission_node_sun:
    raise Exception('Required nodes missing in "sun_material".')

if not value_node_sky or not emission_node_sky:
    raise Exception('Required nodes missing in "sky_material".')

# Open and read the CSV file
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)

    # Iterate through each row in the CSV
    for row in reader:
        # Parse the necessary values from the row
        frame = int(row['index'])  # Assuming 'index' column is the frame number
        change = row['change'].lower() == 'true'  # Check if the 'change' column is True
        z_value = float(row['normalized_sun_altitude'])  # Get the Z location value
        
        # If 'change' is True, set keyframes for the object and materials
        if change:
            # Set keyframe for Z location of "Sun" object
            sun_obj.location[2] = z_value
            sun_obj.keyframe_insert(data_path="location", index=2, frame=frame)

            # Set keyframe for the "Value" node's output value in "sun_material"
            value_node_sun.outputs[0].default_value = z_value
            value_node_sun.outputs[0].keyframe_insert(data_path="default_value", frame=frame)

            # Set keyframe for the "Emission" node's strength in "sun_material"
            sun_energy = z_value * scale  # Scale the sun energy if needed
            emission_node_sun.inputs[1].default_value = sun_energy
            emission_node_sun.inputs[1].keyframe_insert(data_path="default_value", frame=frame)

            # Set keyframe for the "Value" node's output value in "sky_material"
            value_node_sky.outputs[0].default_value = z_value
            value_node_sky.outputs[0].keyframe_insert(data_path="default_value", frame=frame)

            # Set keyframe for the "Emission" node's strength in "sky_material"
            sky_energy = z_value * scale  # Scale the sky energy if needed
            emission_node_sky.inputs[1].default_value = sky_energy
            emission_node_sky.inputs[1].keyframe_insert(data_path="default_value", frame=frame)

print("Keyframes set for 'Sun' object, 'Value' and 'Emission' nodes in 'sun_material' and 'sky_material'.")
