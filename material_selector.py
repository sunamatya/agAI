import sqlite3
from requirements_parser import parse_user_input

def select_best_material(requirements):
    conn = sqlite3.connect("database/materials.db")
    cursor = conn.cursor()

    query = "SELECT * FROM materials WHERE cost <= 20 AND density <= 3"
    cursor.execute(query)

    materials = cursor.fetchall()
    best_material = min(materials, key=lambda m: m[1])  # Minimize weight

    conn.close()
    print ("name:", best_material[1], "elastic_modulus:", best_material[2], "poisson_ratio:", best_material[3])
    return {"name": best_material[1], "elastic_modulus": best_material[2], "poisson_ratio": best_material[3]}
    #return {"name": best_material[0], "elastic_modulus": best_material[1], "poisson_ratio": best_material[2]}

def main():
    print("📌 Welcome to the Local Agentic AI Baseplate Designer")

    # Step 1: Get user input (CLI for now, can be extended to GUI)
    # user_input = input("Enter design requirements (JSON format or interactive mode): ")
    requirements = parse_user_input("inputs/json_tester.json")
    material = select_best_material(requirements)

if __name__ == "__main__":
    main()