import argparse
import json
import requests
from datetime import datetime, timedelta
from time import sleep
import threading
import statistics

class LoadTester:
    def __init__(self, url, method, duration, qps, headers=None, body=None):
        if headers:
            try:
                self.headers = json.loads(headers)
            except:
                raise Exception('headers not json')
        else:
            self.headers = {}
        self.url = url
        self.method = method
        self.body = body
        self.duration = duration
        self.qps = qps
        self.results = []
        self.errors = 0
        self.lock = threading.Lock()

    def make_request(self):
        start_time = datetime.now()

        try:
            r = requests.request(self.url, method=self.method, headers=self.headers, data=self.body)
            latency = datetime.now() - start_time
            with self.lock:
                self.results.append(latency) 

                if r.status_code >= 400:
                    self.errors += 1
        except:
            with self.lock:
                self.errors += 1

    def start(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=self.duration)
        interval = 1/self.qps

        threads = []

        while datetime.now() < end_time:
            thread = threading.Thread(target=self.make_request)
            thread.start()
            threads.append(thread)
            sleep(interval)

        for thread in threads:
            thread.join()

    def report_stats(self):
        if not self.results:
            print("No successful requests.")
            return

        avg_latency = statistics.mean(self.results)
        min_latency = min(self.results)
        max_latency = max(self.results)
        med_latency = statistics.median(self.results)

        print(f"Total Requests: {len(self.results) + self.errors}")
        print(f"Successful Requests: {len(self.results)}")
        print(f"Failed Requests: {self.errors}")
        print(f"Average Latency: {avg_latency:.2f} seconds")
        print(f"Min Latency: {min_latency:.2f} seconds")
        print(f"Max Latency: {max_latency:.2f} seconds")
        print(f"Median Latency: {med_latency:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description = 'HTTP load test')

    parser.add_argument('--url', type=str, required=True, help = 'url')
    parser.add_argument('--method', type=str, choices = ['GET','POST'])
    parser.add_argument('--headers', type=str, required=True, help = 'Headers')
    parser.add_argument('--body', type=str, help = 'Body')
    parser.add_argument('--duration', type=int, required=True, help = 'Time duration in seconds')
    parser.add_argument('--qps', type=int, required=True, help = 'Queries per second')

    args = parser.parse_args()

    load_tester = LoadTester(
        url = args.url,
        method = args.method,
        headers = args.headers,
        body = args.body,
        duration = args.duration,
        qps = args.duration,
        )
    
    load_tester.start()
    load_tester.report_stats()


if __name__ == "__main__":
    main()



