import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.log_parser import parse_time, LogParser
import unittest

class TestLogParser(unittest.TestCase):

    def test_parse_time_days_hours_minutes_seconds_ms(self):
        time_str = "T#1d19h56m1s172ms"
        expected_ms = (1 * 24 * 60 * 60 * 1000) + (19 * 60 * 60 * 1000) + (56 * 60 * 1000) + (1 * 1000) + 172
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_time_minutes_seconds_ms(self):
        time_str = "T#4m17s47ms"
        expected_ms = (4 * 60 * 1000) + (17 * 1000) + 47
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_time_hours_minutes_seconds_ms(self):
        time_str = "T#5h10m5s300ms"
        expected_ms = (5 * 60 * 60 * 1000) + (10 * 60 * 1000) + (5 * 1000) + 300
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_time_only_ms(self):
        time_str = "T#500ms"
        expected_ms = 500
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_time_only_seconds_ms(self):
        time_str = "T#15s250ms"
        expected_ms = (15 * 1000) + 250
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_time_minutes_seconds(self):
        time_str = "T#4m18s"
        expected_ms = (4 * 60 * 1000) + (18 * 1000)
        self.assertEqual(parse_time(time_str), expected_ms)

    def test_parse_log_basic(self):
        log_content = "\n".join(
            [
                "[Recorded curves]",
                "[Record 1]",
                "0;0.0;0.1;T#0ms",
                "1;1.0;0.2;T#100ms",
                "[Record 2]",
                "0;2.0;0.3;T#0ms",
                "1;3.0;0.4;T#100ms",
                "[Variables]",
            ]
        )
        parser = LogParser(log_content)
        dfs = parser.parse_log()
        self.assertEqual(len(dfs), 2)
        self.assertListEqual(dfs[0]["Point"].tolist(), [0, 1])
        self.assertEqual(dfs[0]["Time (ms)"].iloc[-1], 100)

if __name__ == "__main__":
    unittest.main()
