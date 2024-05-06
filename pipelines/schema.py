import os

from schema import Schema, And, Regex, Optional, SchemaError

ALLOWED_NAMES = ("WikiWorker", "YahooFinancePriceWorker", "PostgresWorker")


class PipelineSchema(Schema):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data, _is_event_schema=True):
        data = super().validate(data, _is_event_schema=False)

        if _is_event_schema:
            queues = [q["name"] for q in data["queues"]]

            workers_input_queue = {w["name"]: w["input_queue"] for w in data["workers"] if w.get("input_queue")}
            for w, input_queue in workers_input_queue.items():
                if input_queue not in queues:
                    raise SchemaError(f"input_queue ({input_queue}) of worker ({w}) is not defined in queues")

            workers_output_queues = {w["name"]: w["output_queues"][0] for w in data["workers"] if w.get("output_queues")}
            for w, output_queue in workers_output_queues.items():
                if output_queue not in queues:
                    raise SchemaError(f"output_queue ({output_queue}) of worker ({w}) is not defined in queues")
        return data


schema = {
    "queues": [
        {
            "name": str,
            "description": And(str, lambda s: len(s) < 120)
        }
    ],
    "workers": [
        {
            "name": str,
            "description": And(str, lambda s: len(s) < 120),
            "location": And(os.path.exists, lambda s: os.access(s, os.R_OK), error="path invalid"),
            "klass": And(str, Regex(r'^[A-Z][a-zA-Z0-9_]*$')),
            "num_of_threads": And(int, lambda s: 0 < s < 5),
            Optional("input_queue"): And(str, Regex(r'^[A-Z][a-zA-Z0-9_]*$')),
            Optional("output_queues"): And([And(str, Regex(r'^[A-Z][a-zA-Z0-9_]*$'))]),
        }
    ]
}

config_schema = PipelineSchema(schema)
