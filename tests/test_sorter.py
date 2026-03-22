import unittest
import os
from pathlib import Path
from src.sorter import sort_files

class TestSorter(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory
        self.test_dir = Path("tests/temp_folder")
        self.test_dir.mkdir(exist_ok=True)
        
    def test_file_sorting(self):
        # 1. Create a fake PDF
        test_file = self.test_dir / "sample.pdf"
        test_file.touch()
        
        # 2. Run the sorter on this temp folder
        sort_files(str(self.test_dir))
        
        # 3. Assert (Check) if the file moved to 'Documents'
        expected_path = self.test_dir / "Documents" / "sample.pdf"
        self.assertTrue(expected_path.exists())

    def tearDown(self):
        # Clean up after the test
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == "__main__":
    unittest.main()