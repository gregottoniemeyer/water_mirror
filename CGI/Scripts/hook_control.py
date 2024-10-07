import bpy
import csv

# Load the data from the CSV file
data_file_path = 'Documents/WaterProjects/WeatherMirror/github/water_mirror/data/generated.csv'

# Extract water column data
water_column = []
with open(data_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        water_column.append(float(row['water']))

# Ensure we are in object mode and working with the 3D cursor pivot
bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

# Get the hooks from the collection (replace 'HooksCollection' with the actual name of the collection)
hook_collection_name = "HooksCollection"  # Replace with the actual name of the collection
hook_collection = bpy.data.collections.get(hook_collection_name)

# Parameters
hook_count = 68  # Number of hooks
frames_total = len(water_column) - hook_count  # Total number of frames to animate

if hook_collection and frames_total > 0:
    # Iterate through each frame of the animation
    for frame in range(frames_total):
        # Iterate over all hooks, from the first to the last
        for hook_idx in range(hook_count):
            if hook_idx == hook_count - 1:
                # The last hook gets the new data from the current row
                water_value = water_column[frame + hook_count - 1]
            else:
                # All other hooks take the water value from the next hook (shift down by one index)
                water_value = water_column[frame + hook_idx + 1]
            
            # Get the hook object for this span
            hook = hook_collection.objects[hook_idx]
            
            # Set the Z-scale for the hook to 1.0 + water_value
            hook.scale.z = 1.0 + water_value
            
            # Insert a keyframe for the Z-scale
            hook.keyframe_insert(data_path="scale", index=2, frame=frame + 1)  # Index 2 is for Z-axis
    
    print("Keyframes set for all hooks.")
else:
    print(f"Collection '{hook_collection_name}' not found or insufficient data.")
