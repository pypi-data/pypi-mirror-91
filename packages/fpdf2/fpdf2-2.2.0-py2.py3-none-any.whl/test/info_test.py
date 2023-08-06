"""put_info_test.py"""

import unittest
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join(".."))
)

import fpdf
from test.utilities import assert_pdf_equal

# python -m unittest test.info_test


def document_operations(doc):
    doc.add_page()
    doc.set_font("Arial", size=12)
    doc.cell(w=72, h=0, border=1, ln=2, txt="hello world", fill=0, link="")


class CatalogDisplayModeTest(unittest.TestCase):
    """This test tests some possible inputs to FPDF#_put_info."""

    def test_put_info_all(self):
        doc = fpdf.FPDF()
        document_operations(doc)
        doc.set_title("sample title")
        doc.set_subject("sample subject")
        doc.set_author("sample author")
        doc.set_keywords("sample keywords")
        doc.set_creator("sample creator")
        assert_pdf_equal(self, doc, "test_put_info_all.pdf")

    def test_put_info_some(self):
        doc = fpdf.FPDF()
        document_operations(doc)
        doc.set_title("sample title")
        # doc.set_subject('sample subject')
        # doc.set_author('sample author')
        doc.set_keywords("sample keywords")
        doc.set_creator("sample creator")
        assert_pdf_equal(self, doc, "test_put_info_some.pdf")


if __name__ == "__main__":
    unittest.main()
