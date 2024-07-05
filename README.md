# OpenTelemetry Setup

This package provides a convenient way to set up OpenTelemetry for logging, tracing, and metrics in Python applications.

## Installation

There are two ways of installing this package, using the shell pypi or installing via git.

Using git
Installing from main branch:

python -m pip install git+https://github.com/sede-x/see-pda-core
Installing package from a specific release, in the example above using release v0.7.0

python -m pip install git+https://github.com/sede-x/see-pda-core@v0.7.0


## Usage

```python
from opentelemetry_setup.observability import Observability

header_dict = {"Authorization": "Api-Token your-dynatrace-api-token"}
service_name = "YourService"
service_version = "1.0.0"
endpoint_url = "https://your-dynatrace-url/api/v2/otlp"
send_telemetry_data = True

observability = Observability(header_dict, service_name, service_version, send_telemetry_data)
logger = observability.get_logger(endpoint_url, "my_logger")
tracer = observability.get_tracer(endpoint_url, "my_tracer")
meter = observability.get_meter(endpoint_url, "my_meter")

# Example usage
logger.info("This is an info message")
