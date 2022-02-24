from opentelemetry import baggage, trace
from opentelemetry.context import attach, detach


@router.get("/test")
def test():
    # create a span
    with t.start_as_current_span("get-menuset") as span:
        # set some span attributes
        span.set_attribute("_nb.system", "pos-api")
        span.set_attribute("_nb.name", "get-menu")

        # example of utilizing baggage
        ctx = baggage.set_baggage("menu_id", "b18237d2-aff4-4342-a911-a09a5c8bfdf8")
        token = attach(ctx)
        # call another service
        rsp = requests.get(f"https://producer.ordermark.com/locations/kApp/LAB-Brink")
        detach(token)

        # add an event to the span
        span.add_event(
            "log message",
            {
                "attributes_1": "value_1",
                "attributes_2": "value_2"
            }
        )

    return rsp.json()