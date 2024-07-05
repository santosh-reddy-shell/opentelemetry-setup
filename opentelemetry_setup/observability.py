import logging
import sys
from opentelemetry import context as context_api, trace
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.trace.propagation import _SPAN_KEY
from opentelemetry_setup.init_opentelemetry import InitOpenTelemetry

class Observability(InitOpenTelemetry):
    def __init__(self, header_dict, service_name, service_version, send_telemetry_data):
        super().__init__(header_dict, service_name, service_version, send_telemetry_data)

    def get_logger(self, endpoint_url, logger_name):
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger_provider = super().get_logger_provider(endpoint_url)
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        logger.addHandler(handler)
        return logger

    def get_tracer(self, endpoint_url, tracer_name):
        trace_provider = super().get_trace_provider(endpoint_url)
        self.tracer = trace_provider.get_tracer(tracer_name)
        return self.tracer

    def get_meter(self, endpoint_url, meter_name):
        metric_provider = super().get_meter_provider(endpoint_url)
        self.meter = metric_provider.get_meter(meter_name)
        return self.meter

    def get_current_span(self):
        return trace.get_current_span()

    def init_tracing(self, span_name):
        self.span = self.tracer.start_span(span_name)
        self.token = context_api.attach(context_api.set_value(_SPAN_KEY, self.span))

    def end_tracing(self):
        context_api.detach(self.token)
        self.span.end()
