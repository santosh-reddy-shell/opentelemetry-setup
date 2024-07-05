import logging
from warnings import warn
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.metrics import MeterProvider, Counter, Histogram, ObservableCounter, ObservableUpDownCounter, UpDownCounter
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

class InitOpenTelemetry:
    def __init__(self, header_dict, service_name, service_version, send_telemetry_data=False):
        self.header_dict = header_dict
        self.resource = Resource.create({"service.name": service_name, "service.version": service_version})
        self.send_telemetry_data = send_telemetry_data

    def get_trace_provider(self, endpoint_url):
        tracer_provider = TracerProvider(resource=self.resource)
        if self.send_telemetry_data:
            logging.info(f"Setting up trace provider with endpoint: {endpoint_url}/v1/traces")
            span_processor = BatchSpanProcessor(
                OTLPSpanExporter(endpoint=f"{endpoint_url}/v1/traces", headers=self.header_dict)
            )
        else:
            span_processor = BatchSpanProcessor(ConsoleSpanExporter())
        tracer_provider.add_span_processor(span_processor)
        return tracer_provider

    def get_logger_provider(self, endpoint_url):
        logger_provider = LoggerProvider(resource=self.resource)
        if self.send_telemetry_data:
            logging.info(f"Setting up logger provider with endpoint: {endpoint_url}/v1/logs")
            log_processor = BatchLogRecordProcessor(
                OTLPLogExporter(endpoint=f"{endpoint_url}/v1/logs", headers=self.header_dict)
            )
        else:
            log_processor = BatchLogRecordProcessor(ConsoleLogExporter())
        logger_provider.add_log_record_processor(log_processor)
        return logger_provider

    def get_meter_provider(self, endpoint_url):
        if self.send_telemetry_data:
            logging.info(f"Setting up meter provider with endpoint: {endpoint_url}/v1/metrics")
            exporter = OTLPMetricExporter(
                endpoint=f"{endpoint_url}/v1/metrics",
                headers=self.header_dict,
                preferred_temporality={
                    Counter: AggregationTemporality.DELTA,
                    UpDownCounter: AggregationTemporality.CUMULATIVE,
                    Histogram: AggregationTemporality.DELTA,
                    ObservableCounter: AggregationTemporality.DELTA,
                    ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
                }
            )
            reader = PeriodicExportingMetricReader(exporter)
            meter_provider = MeterProvider(metric_readers=[reader], resource=self.resource)
        else:
            meter_provider = MeterProvider(resource=self.resource)
        return meter_provider
