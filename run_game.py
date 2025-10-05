#!/usr/bin/env python3
"""
Pixel Runner Game Launcher
Simple launcher script for the Pixel Runner game
"""

import os
import subprocess
import sys


def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import pygame

        print(f"✓ Pygame {pygame.version.ver} is installed")
        return True
    except ImportError:
        print("✗ Pygame is not installed")
        print("Please install it with: pip install pygame")
        return False


def main():
    """Main launcher function"""
    print("🏃‍♂️ Pixel Runner Game Launcher")
    print("=" * 40)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check if game file exists
    if not os.path.exists("src/pixel_runner.py"):
        print("✗ Game file 'src/pixel_runner.py' not found!")
        print("Make sure you're running this from the game directory.")
        sys.exit(1)

    print("✓ All dependencies are ready")
    print("Starting Pixel Runner...")
    print("=" * 40)

    # Launch the game
    try:
        subprocess.run([sys.executable, "src/pixel_runner.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\nGame closed by user")
    except Exception as e:
        print(f"Error launching game: {e}")


if __name__ == "__main__":
    main()
