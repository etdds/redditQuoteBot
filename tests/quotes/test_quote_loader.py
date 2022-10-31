import unittest
from redditquotebot.quotes import QuoteDB, QuoteLoader
from io import StringIO


class TestQuoteLoadingFromCSV(unittest.TestCase):

    def test_well_formatted_csv(self):
        infile = StringIO()
        infile.write("""quote, author, category
            You know you're in love when you can't fall asleep because reality is finally better than your dreams.,Dr. Seuss,"attributed-no-source, dreams, love, reality, sleep"
            A friend is someone who knows all about you and still loves you.,Elbert Hubbard,"friend, friendship, knowledge, love"""
                     )
        infile.seek(0)

        db = QuoteLoader.from_csv(infile)
        self.assertEqual(len(db), 2)

    def test_bad_csv(self):
        infile = StringIO()
        infile.write("""this is not a csv
                     on this line""")
        infile.seek(0)
        self.assertRaises(IndexError, QuoteLoader.from_csv, infile)
