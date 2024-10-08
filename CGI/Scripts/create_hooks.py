import bpy
import bmesh

# Switch to object mode to ensure we're not in edit mode initially
bpy.ops.object.mode_set(mode='OBJECT')

# Select the object by name (assuming "data_cylinder" exists in the scene)
obj = bpy.data.objects.get("data_cylinder")
if obj is None:
    raise ValueError("Object 'data_cylinder' not found.")

# Switch to edit mode
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')

# Get the BMesh representation of the object
mesh = bmesh.from_edit_mesh(obj.data)

# Get the unique Z values (rounding to avoid floating-point precision issues)
z_values = sorted(set(round(vert.co.z, 5) for vert in mesh.verts))

# Loop over each unique Z value (which represents each span along the Z-axis)
for i, z_value in enumerate(z_values):
    # Re-fetch BMesh after switching back to edit mode to avoid reference issues
    mesh = bmesh.from_edit_mesh(obj.data)
    
    # Deselect all vertices before each span selection
    bpy.ops.mesh.select_all(action='DESELECT')

    # Select vertices with the current Z value (within a small tolerance for precision)
    for vert in mesh.verts:
        if round(vert.co.z, 5) == z_value:
            vert.select = True
    
    # Update the mesh to reflect the selection
    bmesh.update_edit_mesh(obj.data)
    
    # Switch to object mode to create and assign the hook
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create an empty object for the hook control, name it uniquely
    empty_name = f"Hook_Empty_{i}"
    empty = bpy.data.objects.new(empty_name, None)
    bpy.context.collection.objects.link(empty)

    # Add the hook modifier and assign the empty to it
    hook_modifier = obj.modifiers.new(name=f"Hook_{i}", type='HOOK')
    hook_modifier.object = empty
    
    # Switch back to edit mode to bind the selected vertices to the hook
    bpy.ops.object.mode_set(mode='EDIT')

    # Re-fetch the BMesh again after switching to edit mode to ensure data integrity
    mesh = bmesh.from_edit_mesh(obj.data)
    
    # Assign the selected vertices to the hook
    bpy.ops.object.hook_assign(modifier=hook_modifier.name)

# Finally, return to object mode after all hooks are created
bpy.ops.object.mode_set(mode='OBJECT')

print(f"Created hooks for {len(z_values)} Z-axis spans on 'data_cylinder'.")
