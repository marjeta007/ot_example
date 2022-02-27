"""Configuration..."""
import logging
from pathlib import Path

import yaml
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
# Exporters
# from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# specific instrumentation for FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# logging
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    OTLPHandler,
    set_log_emitter_provider,
)
from opentelemetry.sdk._logs.export import BatchLogProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
# Span processors
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

with Path(__file__).parent.joinpath("env.yml").open() as fp:
    yaml_data = yaml.safe_load(fp)

NEW_RELIC_KEY = yaml_data["NEW_RELIC_KEY"]
OT_COLLECTOR_ENDPOINT = yaml_data["OT_COLLECTOR_ENDPOINT"]


# ==============================================================================


def configure_opentelemetry(service_name, app=None):
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)

    print(f"Service name : {service_name}")
    resource = Resource.create(
        {
            SERVICE_NAME: service_name
        })

    configure_tracing(resource)
    configure_logging(resource)


def configure_tracing(resource):
    provider = TracerProvider(resource=resource)
    # jaeger_export = JaegerExporter(agent_host_name="localhost", agent_port=6831)
    otlp_exporter = OTLPSpanExporter(
        endpoint=OT_COLLECTOR_ENDPOINT,
        headers=((f"api-key={NEW_RELIC_KEY}")),
    )

    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    # provider.add_span_processor(BatchSpanProcessor(jaeger_export))
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    trace.set_tracer_provider(provider)


def configure_logging(resource):
    orig_headers = ((f"api-key={NEW_RELIC_KEY}"))
    modified_headers = (f"api-key={NEW_RELIC_KEY}",)

    provider = LogEmitterProvider(resource=resource)
    set_log_emitter_provider(provider)
    otlp_exporter = OTLPLogExporter(
        endpoint=OT_COLLECTOR_ENDPOINT,
        headers=((f"api-key={NEW_RELIC_KEY}")),
    )

    provider.add_log_processor(BatchLogProcessor(otlp_exporter))
    otlp_handler = OTLPHandler(
        level=logging.NOTSET,
        log_emitter=provider.get_log_emitter(__name__, "0.1")
    )

    stream_handler = logging.StreamHandler()

    # Attach OTLP otlp_handler to root logger
    logging.getLogger().addHandler(otlp_handler)
    logging.getLogger().addHandler(stream_handler)

    logging.basicConfig(
        level=logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    root_logger.info("Logging setup")
