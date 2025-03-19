#
# import sys
#
# FREECADPATH = 'C:\\Users\\samatya\\AppData\\Local\\Programs\\FreeCAD 1.0\\lib'
# sys.path.append(FREECADPATH)
# import FreeCAD
# import Part
# doc = FreeCAD.newDocument()
# box = Part.makeBox(10, 10, 10)
# Part.show(box)
# doc.recompute()
#issue windows is 32 bit, free cad is 64 bit
import sys

# # Add FreeCAD's necessary paths
# FREECADPATH = "C:\\Users\\samatya\\AppData\\Local\\FreeCAD 0.18\\lib"
# import sys
# sys.path.append(FREECADPATH)
# import FreeCAD, Part
# import cadquery as cq
#
# result = cq.Workplane("XY").box(10, 20, 5)
# cq.exporters.export(result, "output.stl")
#
# print("STL file generated successfully!")

# import sys
#
# # Manually specify FreeCAD's library path
# sys.path.append(r"C:\Users\samatya\AppData\Local\FreeCAD 0.18\lib")
#
# try:
#     import FreeCAD
#     print("FreeCAD imported successfully!")
# except ImportError:
#     print("Failed to import FreeCAD.")
# sys.path.insert(0, FREECAD_BASE + "\\lib")
# sys.path.insert(0, FREECAD_BASE + "\\bin")
# sys.path.insert(0, FREECAD_BASE + "\\bin\\Lib\\site-packages")
# import struct
# print("Python Architecture:", struct.calcsize("P") * 8, "bit")
#
# try:
#     import FreeCAD, Part
#     print("✅ FreeCAD imported successfully!")
# except ImportError as e:
#     print(f"❌ Error importing FreeCAD: {e}")
#     print("Check if the FreeCAD paths are correctly set.")


import cadquery as cq
import matplotlib.pyplot as plt

def generate_baseplate(design_constraints):
    width = design_constraints["width"]
    length = design_constraints["length"]
    thickness = design_constraints["thickness"]
    hole_diameter = design_constraints["mounting_holes"]["diameter"]
    spacing_x = design_constraints["mounting_holes"]["spacing_x"]
    spacing_y = design_constraints["mounting_holes"]["spacing_y"]

    # Create the baseplate
    baseplate = cq.Workplane("XY").box(width, length, thickness)

    # Calculate hole positions
    hole_positions = [
        (-spacing_x / 2, -spacing_y / 2),
        (-spacing_x / 2, spacing_y / 2),
        (spacing_x / 2, -spacing_y / 2),
        (spacing_x / 2, spacing_y / 2)
    ]

    # Add holes
    for pos in hole_positions:
        baseplate = baseplate.faces(">Z").workplane().pushPoints([pos]).hole(hole_diameter)

    # Export as STEP & STL
    cq.exporters.export(baseplate, "outputs/baseplate.step")
    cq.exporters.export(baseplate, "outputs/baseplate.stl")

    # Generate a 2D projection
    plt.figure(figsize=(5, 5))
    cq.exporters.export(baseplate, "baseplate.svg")  # Save as vector image

    # Save STL file
    cq.exporters.export(baseplate, "output.stl")

    # # Generate a 2D projection for visualization
    # plt.figure(figsize=(5, 5))
    # cq.exporters.export(baseplate, "output.svg")  # Save as vector image
    # plt.imshow(plt.imread("output.svg"))
    # plt.axis("off")
    # plt.savefig("output_view.png")  # Save the view as PNG
    # plt.show()


    # from PIL import Image
    # from io import BytesIO
    # # Convert SVG to PNG
    # img_png = cairosvg.svg2png('baseplate.svg')
    # img = Image.open(BytesIO(img_png))
    # plt.imshow(img)
    # plt.savefig("output_view.png")  # Save the view as PNG
    from pixels2svg import pixels2svg
    output_path = 'baseplate.png'
    input_path = 'baseplate.svg'
    try:
        result = pixels2svg(input_path, output_path)
        if output_path is None:
            return result
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")


    print("✅ STL and snapshot saved.")


    print("✅ CAD Model saved as 'baseplate.step' and 'baseplate.stl'")
    return "outputs/baseplate.step"


if __name__ == "__main__":
    # Example Constraints
    design_constraints = {
        "width": 200,
        "length": 200,
        "thickness": 10,
        "mounting_holes": {
            "diameter": 10,
            "spacing_x": 100,
            "spacing_y": 100
        }
    }

    generate_baseplate(design_constraints)