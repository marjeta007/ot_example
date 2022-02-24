from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_HEADERS

# Expporters
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Span processors
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

# specific instrumentation for FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# logging
import logging
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    OTLPHandler,
    set_log_emitter_provider,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,

)
from opentelemetry.sdk._logs.export import BatchLogProcessor


# ==============================================================================

def configure_opentelemetry(service_name, app=None):
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)

    resource = Resource.create(
        {
            SERVICE_NAME: service_name
        })

    configure_tracing(resource)
    configure_logging(resource)


def configure_tracing(resource):
    provider = TracerProvider(resource=resource)
    jager_export = JaegerExporter(agent_host_name="localhost", agent_port=6831)
    otlp_exporter = OTLPSpanExporter(
        endpoint="https://otlp.nr-data.net:4317",
        headers=((f"api-key={new_relic_key}")),
    )

    # provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    provider.add_span_processor(BatchSpanProcessor(jager_export))
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    trace.set_tracer_provider(provider)


def configure_logging(resource):
    provider = LogEmitterProvider(resource=resource)
    set_log_emitter_provider(provider)
    otlp_exporter = OTLPLogExporter(
        endpoint="https://otlp.nr-data.net:4317",
        headers=((f"api-key={new_relic_key}")),
    )

    provider.add_log_processor(BatchLogProcessor(otlp_exporter))
    handler = OTLPHandler(
        level=logging.NOTSET,
        log_emitter=provider.get_log_emitter(__name__, "0.1")
    )

    c_handler = logging.StreamHandler()

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
    logging.getLogger().addHandler(c_handler)

    logging.basicConfig(
        level=logging.DEBUG)
