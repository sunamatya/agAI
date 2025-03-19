import sqlite3
from requirements_parser import parse_user_input

def select_best_material(requirements):
    conn = sqlite3.connect("database/materials.db")
    cursor = conn.cursor()
    weight = requirements["max_weight"]
    width = requirements["width"]
    length = requirements["length"]
    thickness = requirements["thickness"]
    density = weight*1000 / (length*0.1*width*0.1*thickness*0.1) #original in g/cm3
    #print(density)

    max_cost = requirements["max_cost"]
    cost_per_unit = max_cost/weight


    # query = "SELECT * FROM materials WHERE cost <= 20 AND density <= 3"
    # cursor.execute(query)
    # Use parameterized query (to prevent SQL injection)
    query = "SELECT * FROM materials WHERE cost <= ? AND density <= ?"
    #cursor.execute(query, (max_cost, density))
    cursor.execute(query, (cost_per_unit, density))

    materials = cursor.fetchall()
    best_material = min(materials, key=lambda m: m[1])  # Minimize weight

    conn.close()
    print ("name:", best_material[1], "density:", best_material[2], "cost:", best_material[3], "elastic_modulus:", best_material[4], "poisson_ratio:", best_material[5])
    return {"name": best_material[1], "density": best_material[2], "cost": best_material[3], "elastic_modulus": best_material[4], "poisson_ratio":best_material[5]}
    #return {"name": best_material[0], "elastic_modulus": best_material[1], "poisson_ratio": best_material[2]}

def main():
    print("📌 Welcome to the Local Agentic AI Baseplate Designer")

    # Step 1: Get user input (CLI for now, can be extended to GUI)
    # user_input = input("Enter design requirements (JSON format or interactive mode): ")
    requirements = parse_user_input("inputs/json_tester.json")
    material = select_best_material(requirements)

if __name__ == "__main__":
    main()