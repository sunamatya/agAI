# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from requirements_parser import parse_user_input
from unittests.tester_cad import generate_baseplate
#from fea_simulator import run_fea_analysis
from fea_simulator import FEA
from material_selector import select_best_material
from optimizer import optimize_design
from report_generator import generate_report


def main():
    print("📌 Welcome to the Local Agentic AI Baseplate Designer")

    # Step 1: Get user input (CLI for now, can be extended to GUI)
    user_input = input("Enter design requirements (JSON format or interactive mode): ")
    requirements = parse_user_input(user_input)

    # Step 2: Select best material
    material = select_best_material(requirements)

    # Step 3: Generate CAD model
    cad_file = generate_baseplate(requirements, material)

    # Step 4: Run FEA simulation
    #fea_results = run_fea_analysis(cad_file, material) #use CALLAX or use the ANN part of the code
    FEA.init(requirements,material)
    fea_results = FEA.run_fea_analysis()

    # Step 5: Optimize design if needed
    optimized_design = optimize_design(fea_results, requirements)

    # Step 6: Generate final report
    generate_report(optimized_design)

    print("✅ Design process complete! Check the 'outputs/' folder for results.")


if __name__ == "__main__":
    main()