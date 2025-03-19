import numpy as np
from scipy.optimize import minimize

deflection_limit = 0.5  # mm
max_weight = 3  # kg
max_cost = 20  # USD

def compute_deflection(thickness, material, width=200e-3, length=200e-3, force=3000, lateral_force=300):
    #E = material["E"]  # Young's modulus in Pascals
    E = material['elastic_modulus']
    # Moment of inertia for a rectangular plate
    I = (width * thickness ** 3) / 12

    # Deflection for simply supported plate with center load
    deflection_vertical = (force * length ** 3) / (48 * E * I)

    # Deflection due to lateral force assuming a cantilevered post
    deflection_lateral = (lateral_force * length ** 3) / (3 * E * I)

    total_deflection = deflection_vertical + deflection_lateral
    return total_deflection * 1e3  # Convert to mm

def weight_function(thickness, material, width=200e-3, length=200e-3):
    density = material["density"]  # kg/m^3
    volume = thickness * (width * length)  # Volume in cubic meters
    return density * volume

def cost_function(thickness, material, width=200e-3, length=200e-3):
    return weight_function(thickness, material, width, length) * material["cost_per_kg"]

def objective(x, material, design_constraints):
    width = design_constraints.get("width", 200) * 1e-3  # Convert mm to meters
    length = design_constraints.get("length", 200) * 1e-3  # Convert mm to meters
    thickness = x[0]
    return weight_function(thickness, material, width, length)

def constraint_deflection(x, material, design_constraints):
    width = design_constraints.get("width", 200) * 1e-3  # Convert mm to meters
    length = design_constraints.get("length", 200) * 1e-3  # Convert mm to meters
    return deflection_limit - compute_deflection(x[0], material, width, length)

def constraint_weight(x, material, design_constraints):
    width = design_constraints.get("width", 200) * 1e-3  # Convert mm to meters
    length = design_constraints.get("length", 200) * 1e-3  # Convert mm to meters
    return max_weight - weight_function(x[0], material, width, length)

def optimize_design(design_constraints, material):
    x0 = [5e-3]  # Initial thickness guess in meters
    bounds = [(1e-3, 10e-3)]  # Thickness range from 1 mm to 10 mm
    constraints = [
        {"type": "ineq", "fun": constraint_deflection, "args": (material, design_constraints,)},
        {"type": "ineq", "fun": constraint_weight, "args": (material, design_constraints,)}
    ]

    result = minimize(objective, x0, args=(material, design_constraints,), bounds=bounds, constraints=constraints)

    if result.success:
        optimized_thickness = result.x[0]
        width = design_constraints.get("width", 200) * 1e-3  # Convert mm to meters
        length = design_constraints.get("length", 200) * 1e-3  # Convert mm to meters
        return {
            "optimized_thickness": optimized_thickness,
            "deflection": compute_deflection(optimized_thickness, material, width, length),
            "weight": weight_function(optimized_thickness, material, width, length),
            "cost": cost_function(optimized_thickness, material, width, length)
        }
    else:
        return None

# Example material properties (Steel)
material = {
    "elastic_modulus": 200e9,  # Young's modulus in Pascals
    "density": 7850,  # kg/m^3
    "cost_per_kg": 2  # USD/kg
}

design_constraints = {
    "width": 200,  # mm
    "length": 200,  # mm
    "thickness": 10,  # mm
    "mounting_holes": {
        "diameter": 10,  # mm
        "spacing_x": 100,  # mm
        "spacing_y": 100  # mm
    }
}

optimized_result = optimize_design(design_constraints, material)
print(optimized_result.get("optimized_thickness"))
