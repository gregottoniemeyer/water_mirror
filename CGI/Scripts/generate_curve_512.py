import bpy
import math

# Create a new curve object
curve_data = bpy.data.curves.new(name='data_electric_curve', type='CURVE')
curve_data.dimensions = '3D'
curve_data.resolution_u = 2

# Create a new spline in the curve
spline = curve_data.splines.new(type='POLY')
spline.points.add(511)  # Create 512 points in total (add() starts from 0)

# Define the X-axis distribution for vertices between -1.7 and 1.7
x_values = [i * (2.0 / 511) - 1.0 for i in range(512)]

# Set each point's location
for i, point in enumerate(spline.points):
    point.co = (x_values[i], -1.0, 0.2, 1.0)  # (x, y, z, w) where w is the weight

# Create a new object with the curve
curve_object = bpy.data.objects.new("data_electric", curve_data)

# Link the object to the scene collection
bpy.context.collection.objects.link(curve_object)

# Select and activate the new object
bpy.context.view_layer.objects.active = curve_object
curve_object.select_set(True)