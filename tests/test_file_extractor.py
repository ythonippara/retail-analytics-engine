import unittest
from unittest.mock import patch, mock_open, MagicMock
import zipfile
from scripts.file_extractor import download_zip, extract_zip, extract_files

import sys
import os

# Add the project root directory to sys.path so scripts/ can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestZipFunctions(unittest.TestCase):
    
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_zip(self, mock_file, mock_requests_get):
        """Test downloading a ZIP file successfully."""
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"test_data"]
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        download_zip("http://example.com/test.zip", "test.zip")
        mock_file.assert_called_with("test.zip", "wb")
        mock_requests_get.assert_called_with("http://example.com/test.zip", stream=True)
    
    @patch("zipfile.ZipFile")
    @patch("os.makedirs")
    def test_extract_zip(self, mock_makedirs, mock_zipfile):
        """Test extracting a ZIP file while skipping intermediary folders."""
        mock_zip = MagicMock()
        mock_zip.namelist.return_value = ["folder/file1.txt", "folder/file2.txt"]
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        extracted_files = extract_zip("test.zip", "data/raw")
        
        self.assertEqual(len(extracted_files), 2)
        self.assertIn("data/raw/file1.txt", extracted_files)
        self.assertIn("data/raw/file2.txt", extracted_files)
        mock_makedirs.assert_called()
    
    @patch("your_module.download_zip")
    @patch("your_module.extract_zip", return_value=["data/raw/file1.txt"])
    @patch("your_module.load_config", return_value={"zip_url": "http://example.com/test.zip", "zip_path": "test.zip", "extracted_to": "data/raw"})
    @patch("os.remove")
    def test_extract_files(self, mock_remove, mock_load_config, mock_extract_zip, mock_download_zip):
        """Test extract_files function end-to-end with mocked dependencies."""
        extracted_files = extract_files()
        
        mock_download_zip.assert_called_with("http://example.com/test.zip", "test.zip")
        mock_extract_zip.assert_called_with("test.zip", "data/raw")
        mock_remove.assert_called_with("test.zip")
        self.assertEqual(extracted_files, ["file1.txt"])

if __name__ == "__main__":
    unittest.main()