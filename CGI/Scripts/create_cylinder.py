import bpy


# Set parameters for the small cylinders
diameter = 0.2  # Diameter of the cylinders
total_length = 2.7479  # Total length along the X-axis
spans = 512  # Number of small cylinders (spans)
vertices = 24  # Number of facets (vertices around the circumference)

# Calculate the length of each small cylinder
single_length = total_length / spans

# Create a collection to store individual cylinders (optional for organization)
cylinder_collection = bpy.data.collections.new("Cylinders")
bpy.context.scene.collection.children.link(cylinder_collection)

# Loop to create and position 512 adjacent cylinders
for i in range(spans):
    # Create a cylinder (default is along Z-axis)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter / 2,
        depth=single_length,
        vertices=vertices,
        end_fill_type='NGON',
        location=(single_length * i, 0, 0)  # Position each cylinder along the X-axis
    )
    
    # Get the created cylinder object
    new_cylinder = bpy.context.object
    
    # Rotate the cylinder to align its axis along the X-axis (rotate 90 degrees around Y-axis)
    new_cylinder.rotation_euler[1] = 1.5708  # 1.5708 radians = 90 degrees
    
    # Add the cylinder to the collection
    bpy.data.collections['Cylinders'].objects.link(new_cylinder)
    bpy.context.scene.collection.objects.unlink(new_cylinder)

# Join all cylinders into a single mesh
bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects first
for obj in bpy.data.collections['Cylinders'].objects:
    obj.select_set(True)  # Select all cylinders

# Join all selected objects into one
bpy.context.view_layer.objects.active = bpy.data.collections['Cylinders'].objects[0]
bpy.ops.object.join()

# Rename the final joined object
final_cylinder = bpy.context.object
final_cylinder.name = "Joined_Cylinder_X_Axis"

# Switch back to object mode (in case we're in edit mode)
bpy.ops.object.mode_set(mode='OBJECT')
