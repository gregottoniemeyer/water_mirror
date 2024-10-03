import bpy
import csv

# Path to the CSV file
csv_file_path = "/Volumes/Consulting/Salesforce Tower/data/precipitation.csv"  # Update with the actual path

# Parameters
scale_factor = 20.0  # Scale factor for scaling the polygons on the Z-axis
plane_count = 256
max_frames = 3000  # Stop after 3000 frames

# Load data from the CSV file
def load_precipitation_data(file_path):
    precipitation_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            precipitation_data.append(float(row['HourlyPrecipitation']))
    return precipitation_data

# Set keyframes for the polygons
def set_keyframes():
    # Load the precipitation data from CSV
    precipitation_data = load_precipitation_data(csv_file_path)

    # Total frames is limited by the minimum of the data length and the max_frames
    total_frames = min(max_frames, len(precipitation_data) - plane_count)

    # Get all the planes in the scene (assuming they're the only objects in the scene)
    planes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    # Sort the planes based on their X-axis location to ensure proper order
    planes.sort(key=lambda p: p.location.x)

    # Make sure we have the correct number of planes
    if len(planes) < plane_count:
        print(f"Warning: Expected {plane_count} planes, but found {len(planes)}.")
        return

    # Set keyframes for each frame up to the max_frames
    for frame in range(total_frames):
        bpy.context.scene.frame_set(frame + 1)
        for i, plane in enumerate(planes):
            # Set the Z-axis scale based on precipitation data for the current frame
            z_scale = precipitation_data[frame + i] * scale_factor
            plane.scale[2] = z_scale  # Adjust the Z-axis scale (height)

            # Insert keyframes for scale on the Z-axis
            plane.keyframe_insert(data_path="scale", index=2)  # Z-axis scale keyframe

# Call the function to set keyframes
set_keyframes()
