import unittest
from unittest.mock import patch

from load_tester import LoadTester

class TestLoadTester(unittest.TestCase):

    @patch('load_tester.requests.request')
    def test_single_request_success(self, mock_request):
        mock_request.return_value.status_code = 200
        tester = LoadTester(url="http://example.com", qps=1, duration=1, method="GET")
        tester.make_request()

        self.assertEqual(len(tester.results), 1)
        self.assertEqual(tester.errors, 0)

    @patch('load_tester.requests.request')
    def test_single_request_failure(self, mock_request):
        mock_request.return_value.status_code = 500
        tester = LoadTester(url="http://example.com", qps=1, duration=1, method="GET")
        tester.make_request()

        self.assertEqual(len(tester.results), 1)
        self.assertEqual(tester.errors, 1)

    @patch('load_tester.requests.request')
    def test_request_exception(self, mock_request):
        mock_request.side_effect = Exception("Request failed")
        tester = LoadTester(url="http://example.com", qps=1, duration=1, method="GET")
        tester.make_request()

        self.assertEqual(len(tester.results), 0)
        self.assertEqual(tester.errors, 1)

    @patch('load_tester.requests.request')
    def test_multiple_requests(self, mock_request):
        mock_request.return_value.status_code = 200
        tester = LoadTester(url="http://example.com", qps=5, duration=1, method="GET")
        tester.start()

        self.assertEqual(len(tester.results), 5)
        self.assertEqual(tester.errors, 0)

    def test_report_stats(self):
        tester = LoadTester(url="http://example.com", qps=1, duration=1, method="GET")
        tester.results = [0.1, 0.2, 0.3, 0.4, 0.5]
        tester.errors = 2

        expected_report = (
            "Total Requests: 7\n"
            "Successful Requests: 5\n"
            "Failed Requests: 2\n"
            "Average Latency: 0.30 seconds\n"
            "Min Latency: 0.10 seconds\n"
            "Max Latency: 0.50 seconds\n"
        )

        with patch('builtins.print') as mocked_print:
            tester.report_stats()
            calls = [
                unittest.mock.call("Total Requests: 7"),
                unittest.mock.call("Successful Requests: 5"),
                unittest.mock.call("Failed Requests: 2"),
                unittest.mock.call("Average Latency: 0.30 seconds"),
                unittest.mock.call("Min Latency: 0.10 seconds"),
                unittest.mock.call("Max Latency: 0.50 seconds")
            ]
            mocked_print.assert_has_calls(calls, any_order=False)

if __name__ == '__main__':
    unittest.main()