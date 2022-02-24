"""
## ummary

Motivation

Leverage open source observability stack to standardize system wide Tracing, Metrics reporting, and Logging. Reduce or eliminate efforts to implement custom code for these purposes.

Goals:

- setup and define reusable configurations and standardize packages based on OpenTelemetry to add Tracing
- discover what auto-instrumentation provides out of the box
- discover how best to standardize tracing/logging
- explore ways and means to distribute the data to various source agnostically

* if the distribution target changes, underlying code already instrumented should not have to change

Further Reading

[What is OpenTelemetry and why is it the future of instrumentation?](https://newrelic.com/blog/best-practices/what-is-opentelemetry)

[What is OpenTelemetry?](https://opentelemetry.io/docs/concepts/what-is-opentelemetry/)

Reference Links:

[https://pypi.org/project/opentelemetry-instrumentation/](https://pypi.org/project/opentelemetry-instrumentation/)

## **Lambda: auto-instrumentation using Layer (no code changes)**

1. Include this layer:

    arn:aws:lambda:us-east-2:901920570463:layer:aws-otel-python38-ver-1-7-1:1

2. Add lambda env variables:

    **AWS_LAMBDA_EXEC_WRAPPER**: /opt/otel-instrument
    **OPENTELEMETRY_COLLECTOR_CONFIG_FILE**: /var/task/otel.yml

3. Add otel.yml at root of project:
"""
