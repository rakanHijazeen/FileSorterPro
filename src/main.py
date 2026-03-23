import sys
import os

# This ensures the script can find the other files in the src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import SortFlowGUI

def main():
    """The official entry point for SortFlow Pro."""
    print("Initializing SortFlow Pro...")
    app = SortFlowGUI()
    app.mainloop()

if __name__ == "__main__":
    main()