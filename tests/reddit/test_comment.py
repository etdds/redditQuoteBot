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

    def testRetrieveAsDictionary(self):
        comment = Comment()
        comment.author = "ben"
        comment.uid = "abcd"
        comment.body = "body"
        comment.edited = False
        comment.subreddit = "test"
        comment.url = "www"
        comment.utc = 12345
        d = comment.to_dict()
        self.assertEqual(d["author"], "ben")
        self.assertEqual(d["uid"], "abcd")
        self.assertEqual(d["body"], "body")
        self.assertEqual(d["edited"], False)
        self.assertEqual(d["subreddit"], "test")
        self.assertEqual(d["url"], "www")
        self.assertEqual(d["utc"], 12345)
