import bpy
import csv

# Load the data from the CSV file
data_file_path = '/Volumes/Consulting/Salesforce Tower/data/interpolated_salesforce_data.csv'

# Extract water column data (scaled by 0.1)
water_column = []
with open(data_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        water_column.append(float(row['temp']) * 0.2)  # Scale the values by 0.1

# Ensure we are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Get the curve object by name (replace 'birdCurve' with the actual name of your curve)
curve = bpy.data.objects.get("pelicanCurve")
if curve is None:
    raise ValueError("Object 'birdCurve' not found.")

# Parameters
cv_count = len(curve.data.splines[0].bezier_points) if curve.data.splines[0].type == 'BEZIER' else len(curve.data.splines[0].points)
frames_total = min(2100, len(water_column) - cv_count)  # Total number of frames to animate, but limited to available data

if curve and frames_total > 0:
    # Switch to edit mode to manipulate the CVs
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Access the splines and control points (CVs)
    spline = curve.data.splines[0]  # Assuming we're working with the first spline of the curve

    if spline.type == 'BEZIER':
        points = spline.bezier_points
    else:
        points = spline.points

    # Iterate through each frame of the animation, up to frames_total
    for frame in range(frames_total):
        # Shift the Z positions of all points up the chain, except the first one
        for cv_idx in range(cv_count - 1):
            # Copy the Z position from the next point to the current point
            points[cv_idx].co.z = points[cv_idx + 1].co.z
            # Insert a keyframe for the shifted Z position
            points[cv_idx].keyframe_insert(data_path="co", index=2, frame=frame + 1)

        # Set the Z position of the last point to the new data from the water column (scaled by 0.1)
        points[cv_count - 1].co.z = water_column[frame]  # Last point gets new water column value
        points[cv_count - 1].keyframe_insert(data_path="co", index=2, frame=frame + 1)

    # Switch back to object mode when done
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("Keyframes set for all curve CVs up to frame", frames_total)
else:
    print(f"Object 'birdCurve' not found or insufficient data.")
