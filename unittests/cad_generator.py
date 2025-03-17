# import FreeCAD, Part
from requirements_parser import parse_user_input
#FREECADPATH = '/opt/FreeCAD/lib' # path to your FreeCAD.so or FreeCAD.dll file
#FREECADPATH = '/opt/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
#FREECADPATH = 'C:/Users/samatya/AppData/Local/Programs/FreeCAD 1.0/bin/FreeCAD.pyd' # path to your FreeCAD.so or FreeCAD.dll file
#FREECADPATH = 'C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\bin\\FreeCAD.pyd'

# FREECADPATH = 'C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\lib'
#
# import sys
# sys.path.append(FREECADPATH)
# sys.path.append("C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\bin")
''' this is to test if we can use the new version of free cad 1.0'''
# import sys
# sys.path.insert(0, "C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\lib")
# sys.path.insert(0, "C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\bin")
# # sys.path.insert(0, "C:\\Users\\samatya\\AppData\\Local\\FreeCAD 0.18\\lib")
# # sys.path.insert(0, "C:\\Users\\samatya\\AppData\\Local\\FreeCAD 0.18\\bin")
# try:
#     #print("we are here")
#     import FreeCAD, Part
#     #import freecad
# except ValueError:
#     print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')

# def generate_baseplate(design_constraints, material):
#     doc = FreeCAD.newDocument("Baseplate")
#
#     # Create baseplate
#     plate = Part.makeBox(design_constraints["width"], design_constraints["length"], design_constraints["thickness"])
#
#     # Add mounting holes (M10 bolts)
#     for x in [20, design_constraints["width"] - 20]:
#         for y in [20, design_constraints["length"] - 20]:
#             hole = Part.makeCylinder(5, design_constraints["thickness"])
#             hole.translate(FreeCAD.Vector(x, y, 0))
#             plate = plate.cut(hole)
#
#     Part.show(plate)
#     output_path = "outputs/baseplate.stp"
#     Part.export([plate], output_path)
#
#     print(f"CAD Model saved at {output_path}")
#     return output_path

import subprocess

subprocess.run(["C:\\FreeCAD\\bin\\python.exe", "freecad_script.py"])


def generate_baseplate(design_constraints):
    doc = FreeCAD.newDocument("Baseplate")

    width = design_constraints["width"]
    length = design_constraints["length"]
    thickness = design_constraints["thickness"]
    hole_diameter = design_constraints["mounting_holes"]["diameter"] / 2  # Radius
    spacing_x = design_constraints["mounting_holes"]["spacing_x"]
    spacing_y = design_constraints["mounting_holes"]["spacing_y"]

    # Create baseplate
    plate = Part.makeBox(width, length, thickness)

    # Calculate hole positions
    hole_positions = [
        (-spacing_x / 2, -spacing_y / 2),
        (-spacing_x / 2, spacing_y / 2),
        (spacing_x / 2, -spacing_y / 2),
        (spacing_x / 2, spacing_y / 2)
    ]

    for pos in hole_positions:
        hole = Part.makeCylinder(hole_diameter, thickness)
        hole.translate(FreeCAD.Vector(pos[0] + width / 2, pos[1] + length / 2, 0))
        plate = plate.cut(hole)

    Part.show(plate)
    output_path = "outputs/baseplate.stp"
    Part.export([plate], output_path)

    print(f"✅ CAD Model saved at {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    constraints = parse_user_input("design_requirements.json")
    if constraints:
        generate_baseplate(constraints)
