from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
import chromadb
import uuid

def extract_audio(video_path,output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)
    video.close()
    return output_audio_path

def audio2text(output_audio_path):
    model = WhisperModel("base",device="cpu",compute_type="int8")
    segments,info = model.transcribe(output_audio_path)
    segments = list(segments)
    return segments

def create_chunks(segments,chunk_size=4):
    chunks=[]
    for i in range(0,len(segments),chunk_size):
        text = ""
        for segment in segments[i:i+chunk_size]:
            text +=segment.text
        chunks.append({
            "text" : text.strip(),
            "start" : segments[i:i+chunk_size][0].start,
            "end" : segments[i:i+chunk_size][-1].end
            
        })
    return chunks

embeder = SentenceTransformer("all-MiniLM-L6-v2")
def embed_chunks(chunks):
    chunks_text = [chunk["text"] for chunk in chunks]
    embeddings = embeder.encode(chunks_text)
    return embeddings

def store_embeddings(embeddings, chunks):
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("my_collection")
    except:
        pass

    collection = client.get_or_create_collection(
        name="my_collection"
    )
    collection.add(
        embeddings=embeddings.tolist(),
        ids=[str(uuid.uuid4()) for _ in range(len(chunks))],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "start": chunk["start"],
                "end": chunk["end"]
            }
            for chunk in chunks
        ]
    )
    return collection

def ingestion_pipeline(video_path,output_audio_path):
    audio_path = extract_audio(video_path,output_audio_path)
    segments = audio2text(audio_path)
    chunks = create_chunks(segments)
    embedding = embed_chunks(chunks)
    collection = store_embeddings(embedding,chunks)
    return collection,chunks