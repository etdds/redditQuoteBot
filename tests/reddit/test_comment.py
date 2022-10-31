import unittest
from redditquotebot.reddit import Comment


class UsingPrintAccessor(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCanCallPrint(self):
        comment = Comment()
        print(comment)
