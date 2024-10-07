import bpy
import random

# Specify the name of the collection containing the hooks
hook_collection_name = "sapn_hooks"  # Replace with the actual collection name

# Get the collection by name
hook_collection = bpy.data.collections.get(hook_collection_name)

# Ensure the collection exists
if hook_collection:
    # Set the pivot point to the 3D cursor
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    
    # Iterate over all objects in the collection
    for obj in hook_collection.objects:
        if obj.type == 'EMPTY':  # Hooks are typically Empty objects
            # Set a random Z-scale between 1.0 and 2.0
            random_scale_z = random.uniform(1.0, 2.0)
            
            # Apply the scale to the Z-axis only
            obj.scale.z = random_scale_z
            
            # Set keyframes (optional), here on frame 1
            obj.keyframe_insert(data_path="scale", index=2, frame=1)  # Index 2 corresponds to Z-axis
            
    print("Z-scale for hooks updated with random values.")
else:
    print(f"Collection '{hook_collection_name}' not found.")
