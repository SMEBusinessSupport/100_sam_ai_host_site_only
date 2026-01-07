import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="odoo",
    user="odoo_user",
    password="odoo_password"
)

cur = conn.cursor()

# Update all tree view modes to list
cur.execute("UPDATE ir_act_window SET view_mode = REPLACE(view_mode, 'tree', 'list') WHERE view_mode LIKE '%tree%';")

# Commit changes
conn.commit()

# Show what was updated
cur.execute("SELECT id, name, view_mode FROM ir_act_window WHERE view_mode LIKE '%list%' LIMIT 10;")
print("Updated actions:")
for row in cur.fetchall():
    print(f"  ID {row[0]}: {row[1]} - {row[2]}")

# Close connection
cur.close()
conn.close()

print("\n✅ All 'tree' view modes updated to 'list'")
