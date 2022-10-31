import unittest
from redditquotebot.reddit import Comment, Reply
from redditquotebot.quotes import Quote


class GeneratingReply(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCanCallPrint(self):
        comment = Comment()
        quote = Quote("body", "author", ["category"])
        reply = Reply(comment, quote)
        self.assertEqual(reply.quote, quote)
        self.assertEqual(reply.comment, comment)
        print(reply)
