import anthropic
import os
from elasticsearch import Elasticsearch


class LlmInterface():
    def __init__(self, key, model = "claude-3-opus-20240229"):
        self.llm_key = key
        self.model = model
        self.random_doc = {}
        self.trial_title = ""
        self.trial_description = ""
        self.llm_client = {}
        self.conversation = []
        self.context_message = ""

    def es_create_connection(self, cloud_id, username, password):
        self.es_client = Elasticsearch(cloud_id=cloud_id, basic_auth=(username, password))
        try:
            self.es_client.info()
        except:
            print("Unable to connect to Elasticsearch")

    def get_random_doc(self, index):
        get_random_doc_body = {
            "size": 1,
            "query": {
                "function_score": {
                    "query": {"match_all": {}},
                    "random_score": {}
                }
            }
        }
        self.random_doc = self.es_client.search(index=index, body=get_random_doc_body)["hits"]["hits"][0]
        print(self.random_doc["_id"])
        return self.random_doc

    def llm_create_connection(self):
        self.llm_client = anthropic.Anthropic(
            api_key=self.llm_key
        )

    def llm_give_context(self):

        self.trial_title = self.random_doc["_source"]["protocolSection"]["identificationModule"]["officialTitle"]
        self.trial_description = self.random_doc["_source"]["protocolSection"]["descriptionModule"]["briefSummary"]
        self.context_message = {"role": "user", "content": """
                You are a clinical trials expert
                Answer the next questions based on this clinical trial information
                Title: {0}
                Description: {1}
                """.format(self.trial_title, self.trial_description),
                 }
        self.conversation.append(self.context_message)
        message = self.llm_client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[self.context_message]
        )

        self.conversation.append({"role":message.role, "content": message.content[0].text})
        print(message.content[0].text)

    def llm_ask_question(self, question):
        current_message = {"role": "user", "content": question}
        self.conversation.append(current_message)
        response = self.llm_client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages= self.conversation
        )
        self.conversation.append({"role": response.role, "content": response.content[0].text})
        print(response.content[0].text)

    def llm_tag_trial(self):

        question = "what disease is this treating? give me the direct answer in as little words as possible"
        trials_interface.llm_ask_question(question=question)

        self.es_client.update(index=index, id=self.random_doc["_id"],
                              body={"doc": {"disease_tag": self.conversation[-1]["content"]}})


cloud_id = os.getenv("ES_CLOUD_ID")
user = os.getenv("ES_USER")
password = os.getenv("ES_PASSWORD")
index_name = os.getenv("ES_INDEX")
claude_id = os.getenv("CLAUDE_ID")
trials_interface = LlmInterface(key=claude_id)
trials_interface.es_create_connection(cloud_id, user, password)
trials_interface.get_random_doc(index=index_name)
trials_interface.llm_create_connection()
trials_interface.llm_give_context()
trials_interface.llm_tag_trial()


while True:
    question = input("What is your clinical trial question?\n")
    trials_interface.llm_ask_question(question=question)
