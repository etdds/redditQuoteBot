import unittest
from redditquotebot.reddit import Comment


class UsingPrintAccessor(unittest.TestCase):
    def test_can_call_print(self):
        comment = Comment()
        print(comment)


class UsingDictionaries(unittest.TestCase):

    def test_comment_to_dictionary(self):
        comment = Comment()
        comment.author = "ben"
        comment.uid = "abcd"
        comment.body = "body"
        comment.edited = False
        comment.subreddit = "test"
        comment.url = "www"
        comment.utc = 12345
        comment.score = 12
        d = comment.to_dict()
        self.assertEqual(d["author"], "ben")
        self.assertEqual(d["uid"], "abcd")
        self.assertEqual(d["body"], "body")
        self.assertEqual(d["edited"], False)
        self.assertEqual(d["subreddit"], "test")
        self.assertEqual(d["url"], "www")
        self.assertEqual(d["utc"], 12345)
        self.assertEqual(d["score"], 12)

    def test_comment_from_dictionary(self):
        d = {
            "author": "ben",
            "uid": "asdf",
            "body": "body",
            "edited": False,
            "utc": 1234,
            "url": "www",
            "subreddit": "test",
            "score": 20
        }
        comment = Comment().from_dict(d)
        self.assertEqual(comment.author, "ben")
        self.assertEqual(comment.uid, "asdf")
        self.assertEqual(comment.body, "body")
        self.assertEqual(comment.edited, False)
        self.assertEqual(comment.subreddit, "test")
        self.assertEqual(comment.url, "www")
        self.assertEqual(comment.utc, 1234)
        self.assertEqual(comment.score, 20)


class CommentEquality(unittest.TestCase):

    def test_equal(self):
        comment1 = Comment()
        comment2 = Comment()
        comment1.uid = "1234"
        comment2.uid = "1234"
        self.assertEqual(comment1, comment2)

    def test_not_equal(self):
        comment1 = Comment()
        comment2 = Comment()
        comment1.uid = "1234"
        comment2.uid = "12345"
        self.assertNotEqual(comment1, comment2)
