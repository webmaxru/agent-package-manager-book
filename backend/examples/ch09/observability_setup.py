"""No-network OpenTelemetry setup probe for Agent Framework 1.9.0."""

from agent_framework.observability import (
    OBSERVABILITY_SETTINGS,
    configure_otel_providers,
    enable_instrumentation,
    get_meter,
    get_tracer,
)


def main() -> None:
    # configure_otel_providers is the installed setup function. With no OTLP
    # endpoint and console exporters disabled, this configures local providers
    # without sending telemetry over the network.
    configure_otel_providers(enable_console_exporters=False, enable_sensitive_data=False)
    enable_instrumentation(enable_sensitive_data=False, force=True)

    tracer = get_tracer("playbook.ch09")
    meter = get_meter("playbook.ch09")
    counter = meter.create_counter("playbook_ch09_observability_runs")
    counter.add(1, {"example": "observability_setup"})

    with tracer.start_as_current_span("playbook.ch09.no_network_probe") as span:
        span.set_attribute("example.chapter", "09")
        print(f"span recording: {span.is_recording()}")

    print(f"instrumentation enabled: {OBSERVABILITY_SETTINGS.ENABLED}")
    print(f"sensitive telemetry enabled: {OBSERVABILITY_SETTINGS.SENSITIVE_DATA_ENABLED}")


if __name__ == "__main__":
    main()
