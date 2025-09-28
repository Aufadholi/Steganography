#!/usr/bin/env python3
"""
Launcher untuk GUI Hybrid LSB Steganography-Blockchain System
Quick start script untuk menjalankan aplikasi GUI

Usage: python launch_gui.py
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the GUI application"""
    print("🚀 Launching Hybrid LSB Steganography-Blockchain GUI...")
    print("📍 System: Windows PowerShell")
    print("🔧 Python:", sys.version)
    
    # Check if we're in the right directory
    project_root = Path(__file__).parent
    gui_script = project_root / "gui_steganography.py"
    
    if not gui_script.exists():
        print(f"❌ Error: GUI script not found at {gui_script}")
        print("💡 Make sure you're running from the stego-chain directory")
        return 1
        
    # Set PYTHONPATH to include project root
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        
    try:
        # Import and run GUI
        print("📦 Loading GUI modules...")
        
        # Import the GUI module
        import gui_steganography
        
        print("✅ GUI modules loaded successfully!")
        print("🖥️ Starting GUI interface...")
        print("\n" + "="*60)
        print("🔐 HYBRID LSB STEGANOGRAPHY-BLOCKCHAIN SYSTEM")
        print("📚 Research Tool for Sinta 3+ Journal Publication")
        print("="*60)
        
        # Run the GUI
        gui_steganography.main()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("2. Check if all modules exist in stego_chain/")
        print("3. Verify Python environment is activated")
        return 1
        
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        print("\n💡 If you see 'tkinter' errors:")
        print("- On Windows: tkinter should be included with Python")
        print("- On Linux: sudo apt-get install python3-tk")
        print("- On macOS: brew install python-tk")
        return 1
    
    print("\n👋 GUI application closed. Thank you!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    
    # Keep window open on Windows if run from file explorer
    if os.name == 'nt' and exit_code != 0:
        input("\nPress Enter to close...")
        
    sys.exit(exit_code)