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

    def test_to_dict(self):
        comment = Comment()
        quote = Quote("body", "author", ["category"])
        reply = Reply(comment, quote)
        d = reply.to_dict()
        self.assertEqual(d["comment"], comment.to_dict())
        self.assertEqual(d["quote"], quote.to_dict())
        self.assertEqual(len(d["body"]) > 0, True)
