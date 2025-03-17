import os


def run_fea_analysis(cad_file, material):
    fea_input = f"""
    *NODE
    1, 0, 0, 0
    *ELEMENT, TYPE=C3D8, ELSET=PLATE
    1, 1, 2, 3, 4, 5, 6, 7, 8
    *MATERIAL, NAME={material['name']}
    *ELASTIC
    {material['elastic_modulus']}, {material['poisson_ratio']}
    *STEP
    *STATIC
    *CLOAD
    1, 3, -{3000}  # Vertical Load
    2, 1, {300}   # Horizontal Load
    *END STEP
    """

    fea_file = "outputs/baseplate.inp"
    with open(fea_file, "w") as file:
        file.write(fea_input)

    # Run CalculiX (Assuming CalculiX installed locally)
    os.system(f"ccx {fea_file}")

    print(f" FEA Simulation completed. Results stored in outputs/")
    return "outputs/baseplate.dat"