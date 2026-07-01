# 🎙️ Meeting Assistant AI

An AI-powered Meeting Assistant built using Retrieval-Augmented Generation (RAG). The application allows users to upload meeting recordings (audio/video), automatically generates transcripts, answers questions about the meeting, and provides comprehensive meeting summaries.

---

## 🚀 Features

- 🎥 Upload audio or video meeting recordings
- 🎧 Automatic audio extraction from videos
- 📝 High-quality speech-to-text transcription using Faster-Whisper
- ✂️ Intelligent transcript chunking
- 🧠 Semantic search using Sentence Transformers
- 📚 ChromaDB vector database for efficient retrieval
- 💬 Ask natural language questions about the meeting
- 📄 Generate complete meeting summaries
- ⚡ Powered by Google Gemini

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Faster-Whisper
- Sentence Transformers
- ChromaDB
- Google Gemini API
- MoviePy
- Python Dotenv

---

# 📂 Project Structure

```
Meeting-Assistant/
│
├── app.py
│
├── lib/
│   ├── __init__.py
│   ├── backend.py
│   ├── ingestion_pipeline.py
│   ├── retrieval_pipeline.py
│   └── llm.py
│
├── notebooks/
│   └── Full_pipeline.ipynb
│
├── upload_video/
├── extracted_audio/
├── chroma_db/
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# ⚙️ Project Workflow

## Ingestion Pipeline

```
Video
   │
   ▼
Extract Audio
   │
   ▼
Speech-to-Text (Faster Whisper)
   │
   ▼
Create Transcript
   │
   ▼
Chunk Transcript
   │
   ▼
Generate Embeddings
   │
   ▼
Store in ChromaDB
```

---

## Retrieval Pipeline

```
User Query
      │
      ▼
Generate Query Embedding
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Generate Prompt
      │
      ▼
Gemini
      │
      ▼
Final Answer
```

---

## Meeting Summary Pipeline

```
Complete Transcript
        │
        ▼
Generate Summary Prompt
        │
        ▼
Gemini
        │
        ▼
Meeting Summary
```

---

# 💡 Example Questions

- Summarize this meeting.
- What were the key discussion points?
- What decisions were made?
- What was discussed about the client?
- Explain the backend architecture.
- Were any deadlines mentioned?
- What technologies were discussed?
- Give me an overview of the meeting.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Meeting-Assistant.git
```

Move into the project directory

```bash
cd Meeting-Assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

# 📈 Future Improvements

- Speaker Diarization
- Speaker-wise Summaries
- Action Item Detection
- Deadline Detection
- Meeting Analytics Dashboard
- Chat History
- Timestamp Navigation
- Multi-language Support
- Hybrid Search (Semantic + Keyword)
- Reranking for Improved Retrieval

---

# 📓 Development Notebook

The repository also includes **Full_pipeline.ipynb**, which contains the complete end-to-end development process of the Meeting Assistant, from preprocessing and transcription to Retrieval-Augmented Generation (RAG).

---

# 📜 License

This project is developed for educational, research, and portfolio purposes.

---

# 👨‍💻 Author

## Aaditya Hole

B.Tech Computer Engineering Student  
AI | Machine Learning | Data Science | Generative AI Enthusiast

If you found this project useful, consider giving it a ⭐ on GitHub.