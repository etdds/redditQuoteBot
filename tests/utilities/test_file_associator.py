import unittest
from redditquotebot.utilities import FileAssociator, FileTypes
from unittest.mock import patch, mock_open


class GettingFileAssociations(unittest.TestCase):
    def setUp(self):
        self.fa = FileAssociator({})
        pass

    def tearDown(self):
        pass

    def testJsonFiletype(self):
        file_type = self.fa.resolve_file_type("test.json")
        self.assertEqual(file_type, FileTypes.JSON)

    def testCSVFiletype(self):
        file_type = self.fa.resolve_file_type("test.csv")
        self.assertEqual(file_type, FileTypes.CSV)

    def testUnknownFiletype(self):
        self.assertRaises(LookupError, self.fa.resolve_file_type, "test.unknownextension")


class OpenFileHandler(unittest.TestCase):
    def setUp(self):
        self.open_count = 0
        pass

    def tearDown(self):
        pass

    def fileOpener(self, *args):
        self.open_count += 1

    def testFileTypeRead(self):
        self.open_count = 0
        fa = FileAssociator({
            FileTypes.JSON: self.fileOpener
        })
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=False):
            fa.read("test.json")

        open_mock.assert_called_with("test.json", "r", encoding="utf-8")
        self.assertEqual(self.open_count, 1)

    def testFileTypeWrite(self):
        self.open_count = 0
        fa = FileAssociator({
            FileTypes.JSON: self.fileOpener
        })
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=True):
            fa.write("test.json")

        open_mock.assert_called_with("test.json", "w", encoding="utf-8")
        self.assertEqual(self.open_count, 1)
