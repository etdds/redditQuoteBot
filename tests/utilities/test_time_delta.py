from redditquotebot.utilities import TimeDelta
from unittest.mock import patch, Mock
import unittest
import time

mock_time = Mock()


class GettinTimeDelta(unittest.TestCase):

    @patch("time.time", mock_time)
    def test_initial_time_set(self):
        mock_time.return_value = 0
        td = TimeDelta()
        self.assertEqual(td._timestamp, 0)

    @patch("time.time", mock_time)
    def test_getting_first_timestamp(self):
        mock_time.return_value = 0
        td = TimeDelta()
        mock_time.return_value = 10
        self.assertEqual(td.elapsed(), 10)

    @patch("time.time", mock_time)
    def test_getting_multiple_timestamps(self):
        mock_time.return_value = 0
        td = TimeDelta()
        mock_time.return_value = 10
        self.assertEqual(td.elapsed(), 10)
        mock_time.return_value = 15
        self.assertEqual(td.elapsed(), 5)
