#!/usr/bin/env python3
"""
Odoo Development Toolbox
=========================

Universal debugging and inspection tool for Odoo development.
Consolidates: check_action, check_menu, check_menu_sql

Usage:
    # Via Odoo shell
    python odoo_toolbox.py shell --check menu --name "SAM AI"

    # Via direct SQL
    python odoo_toolbox.py sql --check menu --name "SAM AI"

    # Interactive mode
    python odoo_toolbox.py interactive

Author: Better Business Builders
Date: October 2025
"""

import argparse
import sys
import os
from pathlib import Path

# Try to import psycopg2 for direct SQL access
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
    print("[!] psycopg2 not installed - SQL mode unavailable")


class OdooToolbox:
    """Universal Odoo inspection and debugging tool"""

    def __init__(self, db_name="ai_automator_db", db_user="postgres", db_password="odoo_password", db_host="localhost"):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.conn = None

    # ========================================================================
    # SQL MODE - Direct database access
    # ========================================================================

    def connect_sql(self):
        """Connect to PostgreSQL database"""
        if not HAS_PSYCOPG2:
            print("[!] Cannot use SQL mode - psycopg2 not installed")
            print("    Install: pip install psycopg2-binary")
            return False

        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host
            )
            return True
        except Exception as e:
            print(f"[!] Database connection failed: {e}")
            return False

    def check_menu_sql(self, menu_name):
        """Check menu via SQL"""
        if not self.connect_sql():
            return

        cur = self.conn.cursor()

        print("=" * 80)
        print(f"Checking menu: {menu_name}")
        print("=" * 80)

        # Query menu
        cur.execute("""
            SELECT m.id, m.name, m.parent_id, m.action, m.sequence, m.active, m.web_icon,
                   p.name as parent_name
            FROM ir_ui_menu m
            LEFT JOIN ir_ui_menu p ON m.parent_id = p.id
            WHERE m.name ILIKE %s
        """, (f"%{menu_name}%",))

        menus = cur.fetchall()

        if not menus:
            print(f"[!] No menus found matching '{menu_name}'")
        else:
            for menu in menus:
                print(f"\n[*] MENU FOUND:")
                print(f"    ID: {menu[0]}")
                print(f"    Name: {menu[1]}")
                print(f"    Parent: {menu[7]} (ID: {menu[2]})")
                print(f"    Action: {menu[3]}")
                print(f"    Sequence: {menu[4]}")
                print(f"    Active: {menu[5]}")
                print(f"    Icon: {menu[6]}")

                # Check groups
                cur.execute("""
                    SELECT g.name
                    FROM res_groups g
                    JOIN ir_ui_menu_group_rel r ON r.gid = g.id
                    WHERE r.menu_id = %s
                """, (menu[0],))
                groups = cur.fetchall()
                print(f"    Groups: {[g[0] for g in groups] if groups else 'All users'}")

        self.conn.close()
        print("\n" + "=" * 80)

    def check_action_sql(self, action_name):
        """Check action via SQL"""
        if not self.connect_sql():
            return

        cur = self.conn.cursor()

        print("=" * 80)
        print(f"Checking action: {action_name}")
        print("=" * 80)

        # Query action
        cur.execute("""
            SELECT id, name, type, res_model, view_mode
            FROM ir_actions
            WHERE name ILIKE %s
        """, (f"%{action_name}%",))

        actions = cur.fetchall()

        if not actions:
            print(f"[!] No actions found matching '{action_name}'")
        else:
            for action in actions:
                print(f"\n[*] ACTION FOUND:")
                print(f"    ID: {action[0]}")
                print(f"    Name: {action[1]}")
                print(f"    Type: {action[2]}")
                print(f"    Model: {action[3]}")
                print(f"    View Mode: {action[4]}")

                # Check if model exists
                cur.execute("""
                    SELECT id, model, name
                    FROM ir_model
                    WHERE model = %s
                """, (action[3],))
                model = cur.fetchone()
                if model:
                    print(f"    Model Status: [OK] '{model[2]}'")
                else:
                    print(f"    Model Status: [!] Model not found!")

        self.conn.close()
        print("\n" + "=" * 80)

    def check_model_sql(self, model_name):
        """Check if model exists via SQL"""
        if not self.connect_sql():
            return

        cur = self.conn.cursor()

        print("=" * 80)
        print(f"Checking model: {model_name}")
        print("=" * 80)

        # Query model
        cur.execute("""
            SELECT id, model, name, state
            FROM ir_model
            WHERE model ILIKE %s
        """, (f"%{model_name}%",))

        models = cur.fetchall()

        if not models:
            print(f"[!] No models found matching '{model_name}'")
        else:
            for model in models:
                print(f"\n[*] MODEL FOUND:")
                print(f"    ID: {model[0]}")
                print(f"    Technical Name: {model[1]}")
                print(f"    Display Name: {model[2]}")
                print(f"    State: {model[3]}")

                # Count fields
                cur.execute("""
                    SELECT COUNT(*)
                    FROM ir_model_fields
                    WHERE model_id = %s
                """, (model[0],))
                field_count = cur.fetchone()[0]
                print(f"    Fields: {field_count}")

                # Count records (if table exists)
                try:
                    table_name = model[1].replace('.', '_')
                    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    record_count = cur.fetchone()[0]
                    print(f"    Records: {record_count}")
                except:
                    print(f"    Records: Unable to query")

        self.conn.close()
        print("\n" + "=" * 80)

    # ========================================================================
    # SHELL MODE - Generate Odoo shell commands
    # ========================================================================

    def generate_shell_command(self, check_type, name):
        """Generate Odoo shell command"""
        print("=" * 80)
        print("ODOO SHELL COMMAND")
        print("=" * 80)
        print("\nRun this in Odoo shell:")
        print("  odoo-bin shell -d your_database_name")
        print("\nThen execute:\n")

        if check_type == "menu":
            print(f"""
menu = env['ir.ui.menu'].search([('name', 'ilike', '{name}')])
if not menu:
    print('[!] Menu not found')
else:
    for m in menu:
        print(f'[*] Menu: {{m.name}} (ID: {{m.id}})')
        print(f'    Parent: {{m.parent_id.name if m.parent_id else "None"}}')
        print(f'    Action: {{m.action}}')
        print(f'    Active: {{m.active}}')
        print(f'    Groups: {{m.groups_id.mapped("name") or "All users"}}')
""")

        elif check_type == "action":
            print(f"""
action = env['ir.actions.act_window'].search([('name', 'ilike', '{name}')])
if not action:
    print('[!] Action not found')
else:
    for a in action:
        print(f'[*] Action: {{a.name}} (ID: {{a.id}})')
        print(f'    Model: {{a.res_model}}')
        print(f'    View Mode: {{a.view_mode}}')

        # Check model
        model = env['ir.model'].search([('model', '=', a.res_model)])
        if model:
            print(f'    Model Status: [OK] {{model.name}}')
        else:
            print(f'    Model Status: [!] Not found')
""")

        elif check_type == "model":
            print(f"""
model = env['ir.model'].search([('model', 'ilike', '{name}')])
if not model:
    print('[!] Model not found')
else:
    for m in model:
        print(f'[*] Model: {{m.name}} ({{m.model}})')
        print(f'    Fields: {{len(m.field_id)}}')

        # Try to count records
        try:
            records = env[m.model].search_count([])
            print(f'    Records: {{records}}')
        except:
            print(f'    Records: Unable to query')
""")

        print("\n" + "=" * 80)

    # ========================================================================
    # INTERACTIVE MODE
    # ========================================================================

    def interactive(self):
        """Interactive mode"""
        print("=" * 80)
        print("ODOO TOOLBOX - Interactive Mode")
        print("=" * 80)
        print("\nWhat would you like to check?")
        print("  1. Menu")
        print("  2. Action")
        print("  3. Model")
        print("  4. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            name = input("Menu name (or partial): ").strip()
            mode = input("Mode (sql/shell): ").strip().lower()
            if mode == "sql":
                self.check_menu_sql(name)
            else:
                self.generate_shell_command("menu", name)

        elif choice == "2":
            name = input("Action name (or partial): ").strip()
            mode = input("Mode (sql/shell): ").strip().lower()
            if mode == "sql":
                self.check_action_sql(name)
            else:
                self.generate_shell_command("action", name)

        elif choice == "3":
            name = input("Model name (or partial): ").strip()
            mode = input("Mode (sql/shell): ").strip().lower()
            if mode == "sql":
                self.check_model_sql(name)
            else:
                self.generate_shell_command("model", name)

        elif choice == "4":
            print("Goodbye!")
            return

        # Continue interactive mode
        if input("\nCheck something else? (y/n): ").lower() == 'y':
            self.interactive()


def main():
    parser = argparse.ArgumentParser(description="Odoo Development Toolbox")
    parser.add_argument("mode", choices=["sql", "shell", "interactive"], help="Operation mode")
    parser.add_argument("--check", choices=["menu", "action", "model"], help="What to check")
    parser.add_argument("--name", help="Name to search for")
    parser.add_argument("--db", default="ai_automator_db", help="Database name")

    args = parser.parse_args()

    toolbox = OdooToolbox(db_name=args.db)

    if args.mode == "interactive":
        toolbox.interactive()

    elif args.mode == "sql":
        if not args.check or not args.name:
            print("[!] SQL mode requires --check and --name")
            sys.exit(1)

        if args.check == "menu":
            toolbox.check_menu_sql(args.name)
        elif args.check == "action":
            toolbox.check_action_sql(args.name)
        elif args.check == "model":
            toolbox.check_model_sql(args.name)

    elif args.mode == "shell":
        if not args.check or not args.name:
            print("[!] Shell mode requires --check and --name")
            sys.exit(1)

        toolbox.generate_shell_command(args.check, args.name)


if __name__ == "__main__":
    main()
