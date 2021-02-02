import unittest

from .form_filler import InputFileError, OutputPathError, is_file, is_path_defined, output_exists


class TestOutputFolder(unittest.TestCase):
    def setUp(self):
        self.user_dict_right = {
            "name": "Meier",
            "first_name": "Hans",
            "rate": 12,
            "date": "12.12.2020",
            "cert_number": "12341",
            "input": "./input_docs/201103_dummy_cert.docx",
            "output": "./pdf_docs/cert_23432.pdf",
        }

        self.user_dict_wrong = {
            "name": "Meier",
            "first_name": "Hans",
            "rate": 12,
            "date": "12.12.2020",
            "cert_numer": "12341",
            "input": "./input_docs/",
            "output": "cert_23432.pdf",
        }

    def test_1_is_file(self):
        self.assertRaises(InputFileError, is_file, self.user_dict_wrong)

    def test_2_is_file(self):
        assert is_file(self.user_dict_right) is None

    def test_1_output_exists(self):
        loc_dict = self.user_dict_wrong.copy()
        del loc_dict["output"]
        self.assertRaises(KeyError, output_exists, loc_dict)

    def test_2_output_exists(self):
        assert output_exists(self.user_dict_right) is None

    def test_1_is_path_defined(self):
        self.assertRaises(OutputPathError, is_path_defined, self.user_dict_wrong)

    def test_2_is_path_defined(self):
        assert is_path_defined(self.user_dict_right) is None
