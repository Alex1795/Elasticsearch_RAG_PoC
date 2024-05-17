from elasticsearch import Elasticsearch
import os
from data_download import DataSerializer

host = os.getenv("ELASTICSEARCH_HOST", "localhost")
user = os.getenv("ES_USER")
password = os.getenv("ES_PASSWORD")
index_name = os.getenv("ES_INDEX")

es_client = Elasticsearch(host,basic_auth=(user, password))
trials_data_url = "https://clinicaltrials.gov/api/v2/studies"
url_query = "?pageSize=1000"#"?query.cond=%22lung%20cancer%22&pageSize=1000"
index = index_name
trials_data_url += url_query

trials_data = DataSerializer()
trials_data.get_serialized_data(trials_data_url)

print(es_client.info())
print(len(trials_data.serialized_documents))
for document in trials_data.raw_json:
    es_client.index(index=index, document=document, id=document["protocolSection"]["identificationModule"]["nctId"])

