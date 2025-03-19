import sqlite3
'''
TODO: eventually use official dataset, current setup for testing
Use official material databases like MatWeb, ASM Handbooks, or CES EduPack.
Check supplier datasheets (e.g., from ArcelorMittal, Alcoa, or local distributors).
'''

# Connect to (or create) the materials database
conn = sqlite3.connect("materials.db")
cursor = conn.cursor()

# Create table with additional fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        density REAL NOT NULL,
        cost REAL NOT NULL,
        elastic_modulus REAL NOT NULL,
        poisson_ratio REAL NOT NULL
    )
''')

# Sample material data
materials = [
    ("Aluminum", 2.7, 10, 69e9, 0.33),
    ("Steel", 7.8, 5, 200e9, 0.30),
    ("Titanium", 4.5, 50, 116e9, 0.34),
    ("Copper", 8.9, 8, 110e9, 0.35),
    ("Plastic", 1.2, 2, 3e9, 0.40)
]

# Insert data (ignores duplicates)
cursor.executemany('''
    INSERT OR IGNORE INTO materials (name, density, cost, elastic_modulus, poisson_ratio)
    VALUES (?, ?, ?, ?, ?)
''', materials)

# Commit and close
conn.commit()
conn.close()

print("✅ materials.db created with sample data!")
