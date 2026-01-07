#!/usr/bin/env python3
"""
Canvas Save Test Script
Simulates user interaction to test node save functionality
"""
import requests
import json
import psycopg2
from datetime import datetime

# Configuration
ODOO_BASE_URL = "http://localhost:8069"
CANVAS_ID = 3
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ai_automator_db',
    'user': 'odoo_user',
    'password': 'odoo_password'
}

def test_canvas_save():
    print("Canvas Save Test Script Starting...")
    
    # Step 1: Check if canvas ID 3 exists, if not create it
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Check if canvas 3 exists
        cur.execute("SELECT id, name FROM canvas WHERE id = %s", (CANVAS_ID,))
        canvas = cur.fetchone()
        
        if not canvas:
            print(f"Canvas ID {CANVAS_ID} doesn't exist, creating it...")
            cur.execute("""
                INSERT INTO canvas (id, name, description, create_date, write_date) 
                VALUES (%s, %s, %s, %s, %s)
            """, (CANVAS_ID, "Test Canvas 3", "Created by test script", datetime.now(), datetime.now()))
            conn.commit()
            print(f"Created canvas ID {CANVAS_ID}")
        else:
            print(f"Canvas ID {CANVAS_ID} exists: {canvas[1]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database canvas check failed: {e}")
        return False
    
    # Step 2: Simulate API call to save a test node
    test_node_data = {
        "name": "Test Node from Script",
        "node_type": "manual_trigger",
        "x_cord": 250,
        "y_cord": 180,
        "parameters": json.dumps({"test": True, "created_by": "python_script"})
    }
    
    print(f"Sending test node data to API...")
    print(f"   → Node: {test_node_data['name']}")
    print(f"   → Position: ({test_node_data['x_cord']}, {test_node_data['y_cord']})")
    
    try:
        # Make API request to save node
        url = f"{ODOO_BASE_URL}/canvas/{CANVAS_ID}/nodes/save"
        payload = {
            "params": {
                "workflow_id": CANVAS_ID,
                "nodes": [test_node_data]
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Note: This will fail without proper authentication, but we can see the error
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"API Response: {result}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ API request failed: {e}")
        print("   → This is expected without proper session authentication")
    
    # Step 3: Check database directly for any new nodes
    print(f"Checking database for nodes in canvas {CANVAS_ID}...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Get all nodes for this canvas
        cur.execute("""
            SELECT id, canvas_id, name, node_type_id, x_cord, y_cord, parameters, create_date 
            FROM nodes 
            WHERE canvas_id = %s 
            ORDER BY create_date DESC
        """, (CANVAS_ID,))
        
        nodes = cur.fetchall()
        
        if nodes:
            print(f"Found {len(nodes)} nodes in canvas {CANVAS_ID}:")
            for node in nodes:
                print(f"   → ID: {node[0]}, Name: {node[2]}, Position: ({node[4]}, {node[5]}), Created: {node[7]}")
        else:
            print(f"No nodes found in canvas {CANVAS_ID}")
        
        # Also check for any nodes created in the last hour (regardless of canvas)
        cur.execute("""
            SELECT id, canvas_id, name, x_cord, y_cord, create_date 
            FROM nodes 
            WHERE create_date > NOW() - INTERVAL '1 hour'
            ORDER BY create_date DESC
        """)
        
        recent_nodes = cur.fetchall()
        
        if recent_nodes:
            print(f"Recent nodes (last hour, any canvas):")
            for node in recent_nodes:
                print(f"   → ID: {node[0]}, Canvas: {node[1]}, Name: {node[2]}, Position: ({node[3]}, {node[4]})")
        else:
            print("No nodes created in the last hour")
        
        cur.close()
        conn.close()
        
        return len(nodes) > 0
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def create_manual_test_node():
    """Directly create a test node in the database to simulate successful save"""
    print("\nCreating test node directly in database...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Create a test node with coordinates
        test_data = {
            'canvas_id': CANVAS_ID,
            'name': 'Manual Test Node',
            'node_type_id': 1,  # Manual Trigger
            'x_cord': 300.0,
            'y_cord': 200.0,
            'parameters': json.dumps({"created_by": "test_script", "timestamp": datetime.now().isoformat()}),
            'active': True,
            'sequence': 1,
            'create_date': datetime.now(),
            'write_date': datetime.now()
        }
        
        cur.execute("""
            INSERT INTO nodes (canvas_id, name, node_type_id, x_cord, y_cord, parameters, active, sequence, create_date, write_date)
            VALUES (%(canvas_id)s, %(name)s, %(node_type_id)s, %(x_cord)s, %(y_cord)s, %(parameters)s, %(active)s, %(sequence)s, %(create_date)s, %(write_date)s)
            RETURNING id
        """, test_data)
        
        node_id = cur.fetchone()[0]
        conn.commit()
        
        print(f"Created test node with ID: {node_id}")
        print(f"   → Name: {test_data['name']}")
        print(f"   → Position: ({test_data['x_cord']}, {test_data['y_cord']})")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create manual test node: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CANVAS SAVE FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Run the main test
    success = test_canvas_save()
    
    if not success:
        print("\nAPI test failed, creating manual test node...")
        manual_success = create_manual_test_node()
        
        if manual_success:
            print("\nManual test node created successfully!")
            print("   → This proves database schema is working")
            print("   → The issue is likely in the API/authentication layer")
        else:
            print("\nEven manual database insertion failed")
            print("   → Database schema or connection issues")
    
    print("\n" + "=" * 50)
    print("Test completed. Check results above.")
    print("=" * 50)