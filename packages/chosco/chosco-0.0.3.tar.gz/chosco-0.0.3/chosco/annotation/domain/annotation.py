import json


class Annotation:
    def __init__(self, id: str, metadata: dict):
        self.id = id
        self.metadata = metadata

    def __repr__(self):
        kdict = {"id": self.id, "metadata": self.metadata}
        return json.dumps(kdict, indent=4)
