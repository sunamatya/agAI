import sqlite3

# Connect to (or create) the materials database
conn = sqlite3.connect("materials.db")
cursor = conn.cursor()

# Create table for material properties
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    density REAL,           -- g/cm³
    cost REAL,       -- $/kg
    yield_strength REAL,    -- MPa
    elastic_modulus REAL    -- GPa
);
""")

# Insert sample materials
materials_data = [
    ("Aluminum 6061", 2.7, 3.5, 275, 69),
    ("Steel A36", 7.85, 0.8, 250, 200),
    ("Titanium Ti-6Al-4V", 4.43, 20.0, 830, 110),
    ("Carbon Fiber", 1.6, 50.0, 600, 230)
]

cursor.executemany("""
INSERT OR IGNORE INTO materials (name, density, cost, yield_strength, elastic_modulus)
VALUES (?, ?, ?, ?, ?);
""", materials_data)

# Commit and close connection
conn.commit()
conn.close()

print("✅ materials.db created successfully!")