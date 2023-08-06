import json
from dataclasses import dataclass


@dataclass
class InsightData:
    tags: list
    significance: float
    data: dict


class InsightDataEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, InsightData):
            return (json.dumps({"Payload": obj.data,
                                "Significance": obj.significance,
                                "Tags": obj.tags}))
        return json.JSONEncoder.default(self, obj)
