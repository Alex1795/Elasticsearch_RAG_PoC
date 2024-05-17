import requests
import json


class DataSerializer:
    def __init__(self):
        self.serialized_documents = []
        self.raw_json = ""

    def get_serialized_data(self, url: str) -> None:
        raw_text = self.get_raw_data(url)
        self.transform_json(raw_text)

        for raw_document in self.raw_json:
            serialized_document = self.generate_serialized_document(raw_document, "", {})
            self.serialized_documents.append(serialized_document)

    def get_raw_data(self, url: str):
        return requests.get(url).content

    def transform_json(self, raw_data):
        json_data = json.loads(raw_data)['studies']
        self.raw_json = json_data
        return

    @staticmethod
    def print_single_json(self, single_json):
        pretty_json = json.dumps(single_json, indent=4)
        print(pretty_json)
        return

    def generate_serialized_document(self, document, key="", serialized_document={}):

        if isinstance(document, dict):
            for k in document.keys():
                serialized_document = self.generate_serialized_document(document[k], key + "." + str(k),
                                                                        serialized_document)
        elif isinstance(document, list):
            for i, k in enumerate(document):
                serialized_document = self.generate_serialized_document(k, key + "." + str(i), serialized_document)
        else:
            serialized_document[key[1:]] = str(document)

        return serialized_document


if __name__ == "__main__":

    trials_data_url = "https://clinicaltrials.gov/api/v2/studies"
    trials_data = DataSerializer()
    trials_data.get_serialized_data(trials_data_url)
    print(trials_data.serialized_documents)
