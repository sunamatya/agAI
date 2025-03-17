def optimize_design(fea_results, constraints):
    print("🔍 Checking if design meets constraints...")

    # Simulated analysis check
    max_deflection = 0.45  # Replace with actual result from FEA
    if max_deflection > constraints["deflection_limit"]:
        print("⚠️ Deflection exceeds 0.5mm. Adjusting thickness...")
        constraints["thickness"] += 1
        return optimize_design(fea_results, constraints)

    print("Design is optimal!")
    return constraints