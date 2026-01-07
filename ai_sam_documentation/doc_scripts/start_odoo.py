#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odoo 18 Server Startup Script - Python Version
==============================================

Cross-platform Odoo startup script with advanced options.

Usage:
    python start_odoo.py                    - Normal startup
    python start_odoo.py --test             - Test startup (stop after init)
    python start_odoo.py --update all       - Update all modules
    python start_odoo.py --install ai_base  - Install specific module
    python start_odoo.py --upgrade ai_trunk - Upgrade specific module
    python start_odoo.py --shell            - Open Odoo shell
    python start_odoo.py --dev xml          - Dev mode with auto-reload for XML
    python start_odoo.py --log-level debug  - Set log level
"""

import os
import sys
import subprocess
import argparse


class OdooStarter:
    def __init__(self):
        self.odoo_path = r"C:\Program Files\Odoo 18\server"
        self.odoo_bin = os.path.join(self.odoo_path, "odoo-bin")
        self.odoo_config = os.path.join(self.odoo_path, "odoo.conf")

    def validate_paths(self):
        """Validate Odoo installation paths"""
        if not os.path.exists(self.odoo_bin):
            print(f"[!] ERROR: Odoo not found at: {self.odoo_bin}")
            print("Please check your installation path.")
            return False

        if not os.path.exists(self.odoo_config):
            print(f"[!] ERROR: Config file not found: {self.odoo_config}")
            return False

        return True

    def build_command(self, args):
        """Build the Odoo command based on arguments"""
        cmd = [sys.executable, self.odoo_bin, "-c", self.odoo_config]

        # Test mode
        if args.test:
            cmd.append("--stop-after-init")

        # Shell mode
        if args.shell:
            cmd.append("shell")

        # Install module
        if args.install:
            cmd.extend(["-i", args.install])
            if not args.no_stop:
                cmd.append("--stop-after-init")

        # Update module
        if args.update:
            cmd.extend(["-u", args.update])
            if args.update != "all" and not args.no_stop:
                cmd.append("--stop-after-init")

        # Upgrade module (alias for update)
        if args.upgrade:
            cmd.extend(["-u", args.upgrade])
            if args.upgrade != "all" and not args.no_stop:
                cmd.append("--stop-after-init")

        # Dev mode
        if args.dev:
            cmd.append(f"--dev={args.dev}")

        # Log level
        if args.log_level:
            cmd.append(f"--log-level={args.log_level}")

        # Database
        if args.database:
            cmd.extend(["-d", args.database])

        return cmd

    def start(self, args):
        """Start Odoo with the given arguments"""
        print("=" * 80)
        print("  Starting Odoo 18 Server")
        print("=" * 80)
        print()

        if not self.validate_paths():
            return 1

        print(f"[*] Odoo Path: {self.odoo_path}")
        print(f"[*] Config: {self.odoo_config}")

        # Determine mode
        mode = "Normal startup"
        if args.test:
            mode = "Test startup only"
        elif args.shell:
            mode = "Odoo shell"
        elif args.install:
            mode = f"Install module: {args.install}"
        elif args.update:
            mode = f"Update module: {args.update}"
        elif args.upgrade:
            mode = f"Upgrade module: {args.upgrade}"
        elif args.dev:
            mode = f"Development mode: {args.dev}"

        print(f"[*] Mode: {mode}")

        if not args.shell and not args.test:
            print("[*] Access Odoo at: http://localhost:8069")
            print("[*] Press CTRL+C to stop the server")

        print()

        # Build and run command
        cmd = self.build_command(args)

        if args.verbose:
            print(f"[*] Command: {' '.join(cmd)}")
            print()

        try:
            # Change to Odoo directory
            os.chdir(self.odoo_path)

            # Run Odoo
            result = subprocess.run(cmd)
            return result.returncode

        except KeyboardInterrupt:
            print("\n")
            print("=" * 80)
            print("  Odoo Server Stopped (Ctrl+C)")
            print("=" * 80)
            return 0

        except Exception as e:
            print(f"\n[!] ERROR: {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Odoo 18 Server Startup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_odoo.py                        # Normal startup
  python start_odoo.py --test                 # Test startup
  python start_odoo.py --install ai_base      # Install ai_base module
  python start_odoo.py --update ai_trunk      # Update ai_trunk module
  python start_odoo.py --upgrade all          # Upgrade all modules
  python start_odoo.py --shell                # Open Odoo shell
  python start_odoo.py --dev xml              # Dev mode (auto-reload XML)
  python start_odoo.py --dev all              # Dev mode (all features)
  python start_odoo.py --log-level debug      # Debug logging
        """
    )

    # Modes
    parser.add_argument("--test", action="store_true",
                       help="Test startup only (--stop-after-init)")
    parser.add_argument("--shell", action="store_true",
                       help="Open Odoo shell")

    # Module operations
    parser.add_argument("-i", "--install", metavar="MODULE",
                       help="Install module (e.g., ai_base)")
    parser.add_argument("-u", "--update", metavar="MODULE",
                       help="Update module (e.g., ai_trunk or 'all')")
    parser.add_argument("--upgrade", metavar="MODULE",
                       help="Upgrade module (alias for --update)")
    parser.add_argument("--no-stop", action="store_true",
                       help="Don't stop after module install/update")

    # Development
    parser.add_argument("--dev", metavar="MODE",
                       help="Dev mode: all, reload, qweb, xml, werkzeug, xml+reload")
    parser.add_argument("--log-level", metavar="LEVEL",
                       help="Log level: debug, info, warning, error, critical")

    # Database
    parser.add_argument("-d", "--database", metavar="DB",
                       help="Database name (default from config)")

    # Other
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show full command being executed")

    args = parser.parse_args()

    starter = OdooStarter()
    return starter.start(args)


if __name__ == "__main__":
    sys.exit(main())
