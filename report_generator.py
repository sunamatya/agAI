from fpdf import FPDF


def generate_report(cadfile, fea_file, optimizer_file ):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Baseplate Design Report", ln=True, align="C")

    #design constraints
    #cad file
    #fea_file and output

    #results from optimizer_files

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Final Thickness: {optimizer_file['thickness']} mm", ln=True)
    pdf.cell(200, 10, f"Selected Material: {optimizer_file['material']}", ln=True)

    output_path = "outputs/design_report.pdf"
    pdf.output(output_path)

    print(f"✅ Report saved at {output_path}")