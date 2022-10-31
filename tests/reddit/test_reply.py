import unittest
from redditquotebot.reddit import Comment, Reply
from redditquotebot.quotes import Quote


class GeneratingReply(unittest.TestCase):

    def test_call_print(self):
        comment = Comment()
        quote = Quote("body", "author", ["category"])
        reply = Reply(comment, quote)
        self.assertEqual(reply.quote, quote)
        self.assertEqual(reply.comment, comment)
        print(reply)


class DictionaryOperations(unittest.TestCase):

    def test_to_dict(self):
        comment = Comment()
        quote = Quote("body", "author", ["category"])
        reply = Reply(comment, quote)
        d = reply.to_dict()
        self.assertEqual(d["comment"], comment.to_dict())
        self.assertEqual(d["quote"], quote.to_dict())
        self.assertEqual(len(d["body"]) > 0, True)

    def test_from_dict(self):
        comment = Comment()
        quote = Quote("body", "author", ["category"])
        d = {
            "comment": comment.to_dict(),
            "quote": quote.to_dict(),
            "body": "test"
        }
        reply = Reply.from_dict(d)
        self.assertEqual(reply.comment, comment)
        self.assertEqual(reply.quote, quote)
        # Note the body contents are generated when requested, and not tested here.
