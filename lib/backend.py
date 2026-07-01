from lib.llm import full_transcript_pipeline
from lib.llm import normal_chunk_pipeline

def backend_pipeline(query,collection,chunks):
    keywords = [
        "summary",
        "summarize",
        "summarise",
        "overview",
        "brief",
        "explain the meeting",
        "what happened in this meeting"
    ]
    query = query.lower()
    if any(keyword in query for keyword in keywords):
        return full_transcript_pipeline(chunks)
    else :
        return normal_chunk_pipeline(query,collection)