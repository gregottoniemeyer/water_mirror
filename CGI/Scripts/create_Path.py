import bpy
import math

# Create a new curve data block
curve_data = bpy.data.curves.new(name='MyCurve', type='CURVE')
curve_data.dimensions = '3D'
curve_data.resolution_u = 2

# Create a new spline (poly spline for straight lines between points)
spline = curve_data.splines.new(type='POLY')
spline.points.add(511)  # 512 points total (add() adds to the 1 default point)

# Set the X range
x_start = -1.3725
x_end = 1.3725
x_values = [x_start + i * (x_end - x_start) / (512 - 1) for i in range(512)]

# Assign coordinates to each point (x, y, z, w)
for i, x in enumerate(x_values):
    spline.points[i].co = (x, 0, 0, 1)  # (x, y, z, w) w is set to 1 for proper weighting

# Create a new curve object and link it to the scene
curve_object = bpy.data.objects.new('MyCurveObject', curve_data)
bpy.context.collection.objects.link(curve_object)
