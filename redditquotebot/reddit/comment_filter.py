from redditquotebot.reddit import Comment
from typing import List, Callable


class CommentAuthorFilter():
    """Filter a comment by author
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Comment):
            return self._comment.author == other.author
        else:
            return self._comment.author == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class CommentUIDFilter():
    """Filter a comment by UID
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Comment):
            return self._comment.uid == other.uid
        else:
            return self._comment.uid == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class CommentEdditedFilter():
    """Filter a comment by eddited flag
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Comment):
            return self._comment.edited == other.edited
        else:
            return self._comment.edited == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class CommentLengthFilter():
    """Filter a comment by the length of its body
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __gt__(self, other) -> bool:
        return len(self._comment.body) > other

    def __ge__(self, other) -> bool:
        return len(self._comment.body) >= other

    def __lt__(self, other) -> bool:
        return len(self._comment.body) < other

    def __le__(self, other) -> bool:
        return len(self._comment.body) <= other

    def __eq__(self, other) -> bool:
        return len(self._comment.body) == other

    def __ne__(self, other) -> bool:
        return len(self._comment.body) != other


class CommentUTCFilter():
    """Filter a comment by UTC time
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Comment):
            return self._comment.utc == other.utc
        else:
            return self._comment.utc == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, Comment):
            return self._comment.utc > other.utc
        else:
            return self._comment.utc > other

    def __ge__(self, other) -> bool:
        if isinstance(other, Comment):
            return self._comment.utc >= other.utc
        else:
            return self._comment.utc >= other

    def __lt__(self, other) -> bool:
        if isinstance(other, Comment):
            return self._comment.utc < other.utc
        else:
            return self._comment.utc < other

    def __le__(self, other) -> bool:
        if isinstance(other, Comment):
            return self._comment.utc <= other.utc
        else:
            return self._comment.utc <= other


class CommentScoreFilter():
    """Filter a comment by its score
    """

    def __init__(self, comment: Comment):
        self._comment = comment

    def __eq__(self, other: object) -> bool:
        return self._comment.score == other

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other) -> bool:
        return self._comment.score > other

    def __ge__(self, other) -> bool:
        return self._comment.score >= other

    def __lt__(self, other) -> bool:
        return self._comment.score < other

    def __le__(self, other) -> bool:
        return self._comment.score <= other


class CommentFilter():
    """Filter a set of comments by a number of filters
    """

    def __init__(self, comments: List[Comment]):
        """
        Args:
            comments (List[Comment]): A list of initial comments to filter.
        """
        self._comments = comments

    def apply(self, operator: Callable):
        """Apply a filter to the comment

        Expected usage:
            comment_filter.apply(lambda comment: CommentEdditedFilter(comment) == False)

        Args:
            operator (Callable): labda function description for the filter to apply
        """
        self._comments = list(filter(operator, self._comments))

    def result(self) -> List[Comment]:
        """Get the remaining comments after the filter has been applied.

        Returns:
            List[Comment]: _description_
        """
        return self._comments

    def latest(self) -> int:
        """Get the latest (greatest) UTC value from the list of comments stored.

        Returns:
            Comment: Latest comment
        """
        if len(self._comments):
            return max([c.utc for c in self._comments])
        return 0

    def __len__(self):
        return len(self._comments)

    def __getitem__(self, index):
        return self._comments[index]
