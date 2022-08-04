import json


class JsonManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> dict:
        with open(self.filename, "r", encoding="utf8") as file:
            data = json.loads(file.read())

        return data

    def save(self, data, sort_keys=False, default=str) -> bool:
        with open(self.filename, "w", encoding="utf8") as file:
            if isinstance(default, str):
                file.write(json.dumps(data, indent=2, sort_keys=sort_keys, default=str))
            else:
                file.write(json.dumps(data, indent=2, sort_keys=sort_keys))

        return True

    def get(self, key: str) -> any:
        data = self.load()
        result = data

        for key in key.split('.'):
            result = result[key]

        return result
