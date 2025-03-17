import json


def parse_user_input(file_path):
    try:
        with open(file_path, "r") as file:
            design_constraints = json.load(file)

        # Validate constraints
        assert 0 < design_constraints["thickness"] <= 10, "Thickness must be ≤ 10 mm"
        assert design_constraints["load_vertical"] >= 3000, "Vertical load too low!"
        assert design_constraints["load_horizontal"] >= 300, "Horizontal load too low!"
        print("file loaded succesfully")

        return design_constraints

    except Exception as e:
        print(f" Input Error: {e}")
        return None

if __name__ == '__main__':
    parse_user_input("inputs/json_tester.json")