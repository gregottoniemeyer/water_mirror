import bpy

# Parameters
plane_width = 0.0285  # The width of each polygon
start_xpos = -3.65  # Starting x position
plane_count = 256  # Number of polygons to create
z_top = 1  # The z-coordinate for the top of each polygon

# Create polygons with given vertices, origin at top-left, and save them as separate meshes
def create_polygons(plane_count, plane_width, start_xpos, z_top):
    
    for i in range(plane_count):
        xpos = start_xpos + i * plane_width  # Calculate x position for each polygon

        # Define the vertices for the polygon with the top at z = 1 and bottom at z = 0.9
        vertices = [
            (xpos, 0, z_top),  # Top-left (first vertex)
            (xpos + plane_width, 0, z_top),  # Top-right
            (xpos, 0, z_top - 0.1),  # Bottom-left
            (xpos + plane_width, 0, z_top - 0.1)  # Bottom-right
        ]

        # Define the face using vertex indices
        faces = [(0, 1, 3, 2)]  # Create a single face connecting the 4 vertices

        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name=f"polygon_{i+1:03d}")
        obj = bpy.data.objects.new(name=f"polygon_{i+1:03d}", object_data=mesh)

        # Link the object to the current collection
        bpy.context.collection.objects.link(obj)

        # Create the mesh from vertices and faces
        mesh.from_pydata(vertices, [], faces)
        mesh.update()

        # Set the origin to the first vertex (top-left)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Set the 3D cursor to the first vertex (top-left corner)
        bpy.context.scene.cursor.location = (xpos, 0, z_top)

        # Set the origin to the 3D cursor location (which is now at the top-left vertex)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Deselect all objects for the next iteration
        bpy.ops.object.select_all(action='DESELECT')

# Call the function to create the polygons
create_polygons(plane_count, plane_width, start_xpos, z_top)
