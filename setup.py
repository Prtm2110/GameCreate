#!/usr/bin/env python3
"""
Pixel Runner Setup Script
Automated setup for the Pixel Runner game
"""

import os
import subprocess
import sys


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def verify_assets():
    """Verify that all game assets are present"""
    print("🎨 Verifying game assets...")

    required_files = [
        "assets/font/Pixeltype.ttf",
        "assets/graphics/Sky.png",
        "assets/graphics/ground.png",
        "assets/graphics/player/player_walk_1.png",
        "assets/graphics/player/player_walk_2.png",
        "assets/graphics/player/jump.png",
        "assets/graphics/player/player_stand.png",
        "assets/graphics/snail/snail1.png",
        "assets/graphics/snail/snail2.png",
        "assets/graphics/fly/Fly1.png",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("✗ Missing required asset files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✓ All required assets are present!")
        return True


def main():
    """Main setup function"""
    print("🏃‍♂️ Pixel Runner Setup")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7+ is required")
        sys.exit(1)

    print(f"✓ Python {sys.version.split()[0]} detected")

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Verify assets
    if not verify_assets():
        print("\n⚠️  Some assets are missing. The game may not work properly.")
        print(
            "Please ensure all graphics and font files are in the correct directories."
        )

    print("\n🎮 Setup complete! Run 'python src/pixel_runner.py' to start the game.")
    print("Or use 'python run_game.py' for the launcher.")


if __name__ == "__main__":
    main()
