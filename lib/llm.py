from dotenv import load_dotenv
import os
import google.generativeai as genai
from lib.retrieval_pipeline import retrive_full_transcript
from lib.retrieval_pipeline import embed_query
from lib.retrieval_pipeline import retrive_chunks

def generate_chunk_prompt(retrived_chunks,query):
    context = "\n\n".join(
        retrived_chunks["documents"][0]
    )
    prompt = f"""
    You are an AI Meeting Assistant.
    Your task is to answer the user's question using ONLY the provided meeting transcript context.
    Guidelines:
        - Answer only from the provided context.
        - Do not make up information.
        - If the answer is partially available, answer using only the available information.
        - If the answer is not found in the context, reply:
          "This information was not discussed in the meeting."
        - Keep the answer clear, concise, and professional.
        - If appropriate, mention the approximate timestamps available in the context.

    Meeting Transcript Context:
    {context}

    User Question:
    {query}

    Answer:
    """
    return prompt

def generate_transcript_prompt(full_transcript):
    prompt = f"""
    You are an AI Meeting Assistant.
    Your task is to analyze the complete meeting transcript and generate a structured summary.
    Include the following sections:

    1. Overall Summary
   - Briefly describe the purpose of the meeting.
    2. Key Discussion Points
   - List the major topics discussed.
    3. Decisions Made
   - Mention all important decisions taken during the meeting.
   - If none, write "No explicit decisions were made."
    4. Action Items
   - List any tasks assigned or follow-up work.
   - If none, write "No action items were identified."
    5. Deadlines
   - Mention any deadlines or important dates discussed.
   - If none, write "No deadlines were discussed."

    Keep the summary concise, well-structured, and easy to read.
    Do not invent information that is not present in the transcript.

    Meeting Transcript:

    {full_transcript}

    Summary:
    """

    return prompt

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def full_transcript_pipeline(chunks):
    full_transcript = retrive_full_transcript(chunks)
    prompt = generate_transcript_prompt(full_transcript)
    response = model.generate_content(prompt)
    return response.text

def normal_chunk_pipeline(query,collection):
    embedding = embed_query(query)
    retrived_chunks = retrive_chunks(collection,embedding)
    prompt = generate_chunk_prompt(retrived_chunks,query)
    response = model.generate_content(prompt)
    return response.text