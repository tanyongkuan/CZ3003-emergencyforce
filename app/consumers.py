from channels.generic.websockets import WebsocketDemultiplexer

from .models import ReportBinding


class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        # "intval": IntegerValueBinding.consumer,
        "intval": ReportBinding.consumer,

    }

    groups = ["binding.values"]
