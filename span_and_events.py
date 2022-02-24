import logging

import requests
from fastapi import APIRouter
from opentelemetry import trace

from ot_configuration import configure_opentelemetry

router = APIRouter()
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

configure_opentelemetry(__name__)

logger.info("Configuration complete.")


# @router.get("/test")
def test():
    # create a span
    logger.info("Create a span.")

    with tracer.start_as_current_span("get-menuset") as span:
        # set some span attributes
        logger.info("creating attributes.")
        span.set_attribute("_nb.system", "pos-api")
        span.set_attribute("_nb.name", "get-menu")

        # # example of utilizing baggage
        # ctx = baggage.set_baggage("menu_id", "b18237d2-aff4-4342-a911-a09a5c8bfdf8")
        # token = attach(ctx)

        # call another service
        logger.info("Calling service.")
        rsp = requests.get(f"https://producer.ordermark.com/locations/kApp/LAB-Brink")
        # detach(token)

        # add an event to the span
        span.add_event(
            "log message",
            {
                "attributes_1": "value_1",
                "attributes_2": "value_2"
            }
        )

    json_stuff = rsp.json()
    logger.info(f"{json_stuff}")

    return json_stuff


if __name__ == '__main__':
    test()
