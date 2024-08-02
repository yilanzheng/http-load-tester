# HTTP Load Testing and Benchmarking Tool

This project provides a general-purpose HTTP load-testing and benchmarking library implemented in Python. The tool allows you to specify an HTTP address, generate requests at a given fixed Queries Per Second (QPS), and reports latency statistics and error rates. It is also Dockerized for easy deployment and execution.

## Features

- Specify an HTTP address as input.
- Support for a `--qps` flag to generate requests at a given fixed QPS.
- Reports latency statistics (average, minimum, and maximum latencies) and error rates.
- Extensible design to add more features.
- Unit tests to verify the functionality.
- Dockerized for easy deployment.

## Installation

### Prerequisites

- Docker
- Python 3.9 (if running locally without Docker)

### Build Docker Image

To build the Docker image, navigate to the project directory and run:

```sh
docker build -t load-tester .
```

## Usage

### Run the Docker Container

**Command-Line Arguments**

​	•	--url: The URL to be tested (required).

​	•	--qps: Queries per second (required).

​	•	--duration: Duration of the test in seconds (required).

​	•	--method: HTTP method to use (default is GET).

​	•	--headers: Optional headers as a JSON string.

​	•	--body: Optional request body.

### Example

```sh
docker run --rm load-tester --url http://example.com --qps 10 --duration 60 --method GET
```

### Development

#### Local Development

If you want to develop and test the tool locally without Docker, you need to have Python 3.9 installed.

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the tool locally:

   ```sh
   python load_tester.py --url http://example.com --qps 10 --duration 60 --method GET
   ```

3. Run the tests locally:

   ```sh
   python -m unittest discover -s .
   ```

