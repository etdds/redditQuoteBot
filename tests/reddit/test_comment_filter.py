import unittest
from redditquotebot.reddit import Comment, CommentAuthorFilter, CommentFilter, CommentUTCFilter, CommentUIDFilter, CommentEdditedFilter, CommentLengthFilter, CommentScoreFilter


class TestCommentAuthorFilter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCommentAuthorMatches(self):
        comment1 = Comment()
        comment1.author = "ben"
        comment2 = Comment()
        comment2.author = "ben"
        matcher = CommentAuthorFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testCommentAuthorDoesntMatch(self):
        comment1 = Comment()
        comment1.author = "ben"
        comment2 = Comment()
        comment2.author = "ted"
        matcher = CommentAuthorFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)

    def testStringAuthorMatches(self):
        comment1 = Comment()
        comment1.author = "ben"
        matcher = CommentAuthorFilter(comment1)
        equal = matcher == "ben"
        not_equal = matcher != "ben"
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testStringAuthorDoesntMatch(self):
        comment1 = Comment()
        comment1.author = "ben"
        matcher = CommentAuthorFilter(comment1)
        equal = matcher == "yo"
        not_equal = matcher != "yo"
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)


class TestCommentUTCFilter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCommentUTCMatches(self):
        comment1 = Comment()
        comment1.utc = 1234
        comment2 = Comment()
        comment2.utc = 1234
        matcher = CommentUTCFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testCommentNotUTCMatches(self):
        comment1 = Comment()
        comment1.utc = 1234
        comment2 = Comment()
        comment2.utc = 4321
        matcher = CommentUTCFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)

    def testIntegerUTCMatches(self):
        comment1 = Comment()
        comment1.utc = 1234
        matcher = CommentUTCFilter(comment1)
        equal = matcher == 1234
        not_equal = matcher != 1234
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testIntegerUTCNotMatches(self):
        comment1 = Comment()
        comment1.utc = 1234
        matcher = CommentUTCFilter(comment1)
        equal = matcher == 4321
        not_equal = matcher != 4321
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)

    def testIntegerComparisons(self):
        comment = Comment()
        comment.utc = 1234
        matcher = CommentUTCFilter(comment)
        self.assertEqual(matcher < 1234, False)
        self.assertEqual(matcher <= 1234, True)
        self.assertEqual(matcher >= 1234, True)
        self.assertEqual(matcher > 1234, False)

    def testIntegerComparisonsWithComment(self):
        comment1 = Comment()
        comment1.utc = 1234
        matcher = CommentUTCFilter(comment1)
        comment2 = Comment()
        comment2.utc = 1234
        self.assertEqual(matcher < comment2, False)
        self.assertEqual(matcher <= comment2, True)
        self.assertEqual(matcher >= comment2, True)
        self.assertEqual(matcher > comment2, False)


class TestCommentLengthFilter(unittest.TestCase):
    def setUp(self):
        self.comment = Comment()
        self.comment.body = "1234567890"

    def tearDown(self):
        pass

    def testCommentLengthEqual(self):
        self.assertEqual(CommentLengthFilter(self.comment) == 10, True)

    def testCommentLengthNotEqual(self):
        self.assertEqual(CommentLengthFilter(self.comment) != 8, True)

    def testCommentLengthLessThan(self):
        self.assertEqual(CommentLengthFilter(self.comment) < 12, True)

    def testCommentLengthLessThanEqual(self):
        self.assertEqual(CommentLengthFilter(self.comment) <= 10, True)

    def testCommentLengthGreaterThanEqual(self):
        self.assertEqual(CommentLengthFilter(self.comment) >= 10, True)

    def testCommentLengthGreaterThan(self):
        self.assertEqual(CommentLengthFilter(self.comment) > 9, True)


class TestCommentUIDFilter(unittest.TestCase):

    def testCommentUIDMatches(self):
        comment1 = Comment()
        comment1.uid = "aks"
        comment2 = Comment()
        comment2.uid = "aks"
        matcher = CommentUIDFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testStringUIDMatches(self):
        comment1 = Comment()
        comment1.uid = "asdf"
        matcher = CommentUIDFilter(comment1)
        equal = matcher == "jkl;"
        not_equal = matcher != "jkl;"
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)


class TestCommentEditedFilter(unittest.TestCase):

    def testCommentEdditMatches(self):
        comment1 = Comment()
        comment1.edited = True
        comment2 = Comment()
        comment2.edited = True
        matcher = CommentEdditedFilter(comment1)
        equal = matcher == comment2
        not_equal = matcher != comment2
        self.assertEqual(equal, True)
        self.assertEqual(not_equal, False)

    def testBoolEditMatches(self):
        comment1 = Comment()
        comment1.edited = True
        matcher = CommentEdditedFilter(comment1)
        equal = matcher == False
        not_equal = matcher != False
        self.assertEqual(equal, False)
        self.assertEqual(not_equal, True)


class TestCommentScoreFilter(unittest.TestCase):

    def test_comarisons_with_builtins(self):
        comment1 = Comment()
        comment1.score = 13
        self.assertEqual(CommentScoreFilter(comment1) == 13, True)
        self.assertEqual(CommentScoreFilter(comment1) != 17, True)
        self.assertEqual(CommentScoreFilter(comment1) > 12, True)
        self.assertEqual(CommentScoreFilter(comment1) >= 13, True)
        self.assertEqual(CommentScoreFilter(comment1) < 14, True)
        self.assertEqual(CommentScoreFilter(comment1) <= 13, True)


class TestCommentFilter(unittest.TestCase):
    def setUp(self):
        names = ["mathew", "mark", "luke", "luke"]
        self.comment_list = []
        for name in names:
            comment = Comment()
            comment.author = name
            comment.edited = True
            self.comment_list.append(comment)

        self.comment_list[-1].edited = False
        self.comment_list[0].utc = 1234
        self.comment_list[1].utc = 9999

    def testFilterByAuthor(self):
        comment_filter = CommentFilter(self.comment_list)
        comment_filter.apply(lambda comment: CommentAuthorFilter(comment) == "luke")
        self.assertEqual(len(comment_filter), 2)
        self.assertEqual(comment_filter[0].author, "luke")

    def testFilterByAuthorComment(self):
        target = Comment()
        target.author = "mark"
        comment_filter = CommentFilter(self.comment_list)
        comment_filter.apply(lambda comment: CommentAuthorFilter(comment) == target)
        self.assertEqual(len(comment_filter), 1)
        self.assertEqual(comment_filter[0].author, "mark")

    def testMultipleApplidFilters(self):
        comment_filter = CommentFilter(self.comment_list)
        comment_filter.apply(lambda comment: CommentAuthorFilter(comment) == "luke")
        self.assertEqual(len(comment_filter), 2)
        comment_filter.apply(lambda comment: CommentEdditedFilter(comment) == False)
        self.assertEqual(len(comment_filter), 1)
        self.assertEqual(comment_filter[0].author, "luke")
        results = comment_filter.result()
        self.assertEqual(results[0].author, "luke")

    def testGetLatestUTC(self):
        comment_filter = CommentFilter(self.comment_list)
        self.assertEqual(comment_filter.latest(), 9999)

    def testGetLatestUTCWhenEmpty(self):
        comment_filter = CommentFilter([])
        self.assertEqual(comment_filter.latest(), 0)
