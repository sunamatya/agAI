from fpdf import FPDF


def generate_report(design_constraints, material, optimizer_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Baseplate Design Report", ln=True, align="C")
    # design constraints
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "Baseplate Requirements", ln=True, align="C")
    width = design_constraints["width"]
    length = design_constraints["length"]
    thickness = design_constraints["thickness"]
    hole_diameter = design_constraints["mounting_holes"]["diameter"]
    spacing_x = design_constraints["mounting_holes"]["spacing_x"]
    spacing_y = design_constraints["mounting_holes"]["spacing_y"]
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"width: {width} mm", ln=True)
    pdf.cell(200, 10, f"length: {length}mm", ln=True)
    pdf.cell(200, 10, f"thickness: {thickness}mm", ln=True)
    pdf.cell(200, 10, f"mounting hole diameter: {hole_diameter}mm", ln=True)
    pdf.cell(200, 10, f"mounting hole spacing x: {spacing_x}mm", ln=True)
    pdf.cell(200, 10, f"mounting hole spacing x: {spacing_y}mm", ln=True)

    #material selection
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "Initial Material Selection", ln=True, align="C")
    #selection constrain
    #selected material


    #cad file
    pdf.image("image.jpg", x=10, y=30, w=100, h=100)
    pdf.cell(200, 10, f"Cadquery view of the CAD file generated", ln=True)


    #fea_file and output
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "FEA Report and learning", ln=True, align="C")
    pdf.image("unittests/plot_1.jpg", x=10, y=30, w=100, h=100)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"PINN Learning Loss for specified model", ln=True)

    pdf.image("unittests/plot_2.jpg", x=10, y=30, w=100, h=100)
    pdf.cell(200, 10, f"Deflection analysis for the lateral force", ln=True)

    pdf.image("unittests/plot_3.jpg", x=10, y=30, w=100, h=100)
    pdf.cell(200, 10, f"Deflection analysis for the horizontal force", ln=True)



    #results from optimizer_files

    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "Baseplate Optimization Report", ln=True, align="C")
    # pdf.cell(200, 10, f"Final Thickness: {optimizer_file['thickness']} mm", ln=True)
    # pdf.cell(200, 10, f"Selected Material: {optimizer_file['material']}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Optimized Thickness: {optimizer_file.get('optimized_thickness')} mm", ln=True)
    pdf.cell(200, 10, f"Deflection Computed: {optimizer_file.get('deflection')}", ln=True)
    pdf.cell(200, 10, f"Optimized Final Weight: {optimizer_file.get('weight')}", ln=True)
    pdf.cell(200, 10, f"Optimized Cost: {optimizer_file.get('cost')}", ln=True)

    output_path = "outputs/design_report.pdf"
    pdf.output(output_path)

    print(f"✅ Report saved at {output_path}")