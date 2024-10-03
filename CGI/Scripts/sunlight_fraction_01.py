import bpy
import csv

# Path to your CSV file
csv_file_path = "/Volumes/Consulting/Salesforce Tower/data/sunlight_fraction.csv"  # Update with the actual path


# Define the sun objects and materials
sun_object_01 = bpy.data.objects["Sun_Up"]
sun_object_02 = bpy.data.objects["Sun_Down"]
sun_material_01 = bpy.data.materials["sun_up_material"]
sun_material_02 = bpy.data.materials["sun_down_material"]



# Read the CSV data
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        frame = i  # Frame corresponding to the row (you can scale this for slower animations)
        sunlight_fraction = float(row['sunlight_fraction'])
        
        up_sun= float(row['increasing_sunlight']) 
        down_sun= float(row['decreasing_sunlight']) 

        # Set emission for sun materials and keyframe it
        sun_material_01.node_tree.nodes["Emission"].inputs[1].default_value = sunlight_fraction * 5.0
        sun_material_01.node_tree.nodes["Value"].outputs[0].default_value = sunlight_fraction * 1.1
        sun_material_01.node_tree.nodes["Emission"].inputs[1].keyframe_insert(data_path="default_value", frame=frame)
        sun_material_01.node_tree.nodes["Value"].outputs[0].keyframe_insert(data_path="default_value", frame=frame)

        sun_material_02.node_tree.nodes["Emission"].inputs[1].default_value = sunlight_fraction * 5.0
        sun_material_02.node_tree.nodes["Value"].outputs[0].default_value = sunlight_fraction * 1.1
        sun_material_02.node_tree.nodes["Emission"].inputs[1].keyframe_insert(data_path="default_value", frame=frame)
        sun_material_02.node_tree.nodes["Value"].outputs[0].keyframe_insert(data_path="default_value", frame=frame)
        
        
        sun_object_01.location[2]= up_sun
        sun_object_01.keyframe_insert(data_path="location", index=2, frame=frame)
        
        sun_object_02.location[2] = down_sun
        sun_object_02.keyframe_insert(data_path="location", index=2, frame=frame)

