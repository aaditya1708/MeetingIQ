from sentence_transformers import SentenceTransformer

embeder = SentenceTransformer("all-MiniLM-L6-v2")
def embed_query(query):
    query_embedding= embeder.encode(query)
    return query_embedding

def retrive_chunks(collection,query_embedding):
    result = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results = 3
    )
    return result

def retrive_full_transcript(chunks):
    full_transcript =""
    for chunk in chunks:
        full_transcript+= chunk["text"]+"\n\n"
    return full_transcript

