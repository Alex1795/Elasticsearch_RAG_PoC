# PoC for RAG with Elasticsearch

This PoC takes some clinical trials from "https://clinicaltrials.gov/api/v2/studies". 

data_upload.py uploads trials to an index in Elasticsearch

llm_interface.py takes a random trial as a context, tags the dissease it's treating and then let's you ask questions about it. 

As a PoC this only provides the title and summary of the trial as context for now.

The LLM used here is Claude, more especifically the claude-3-opus-20240229 model.

You need to define the following environments variables for it to work:

```
ES_CLOUD_ID
ELASTICSEARCH_HOST
ES_USER
ES_PASSWORD
ES_INDEX
CLAUDE_ID
```

So you need an Elastic cloud deployment and a Claude token. 
