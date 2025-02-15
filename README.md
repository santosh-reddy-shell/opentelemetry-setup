# OpenTelemetry Setup

This package provides a convenient way to set up OpenTelemetry for logging, tracing, and metrics in Python applications.

# Installation
There are two ways of installing this package, using the shell pypi or installing via git.


## Using git
Installing from main branch:
```shell
python -m pip install git+https://github.com/santosh-reddy-shell/opentelemetry-setup
```

Installing package from a specific release, in the example above using release ``v0.7.0``
```shell
python -m pip install git+https://github.com/santosh-reddy-shell/opentelemetry-setup@v1.0.0
```

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

# Create and increment a counter metric
counter = meter.create_counter(
    name="example.counter",
        description="An example counter",
        unit="1"
    )

logger.info("Telemetry setup complete.")
observability.init_tracing("example_span")
# Increment the counter with current timestamp as attribute
counter.add(45, {"attribute_key": "attribute_value", "timestamp": datetime.datetime.now().isoformat(), "source": "VSCODE"})
observability.end_tracing()
