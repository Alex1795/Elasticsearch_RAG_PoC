from llm_interface import LlmInterface


class LlmTagger(LlmInterface):
    def __init__(self):
        pass

    def tagger(self):
        LlmInterface.llm_create_connection()