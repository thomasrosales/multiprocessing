import os

from schema import Schema, And, Regex

config_schema = Schema({
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
            "klass": And(str, Regex(r'^[A-Z][a-zA-Z0-9_]*$'))
        }
    ]
})
