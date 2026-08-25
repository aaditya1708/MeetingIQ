import os
import time
import chromadb
import streamlit as st

from lib.ingestion_pipeline import (
    extract_audio,
    audio2text,
    create_chunks,
    embed_chunks,
    store_embeddings,
)
from lib.backend import backend_pipeline

st.set_page_config(
    page_title="MeetingIQ",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

UPLOAD_DIR = "upload_video"
AUDIO_DIR = "extracted_audio"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "my_collection"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

st.markdown(
    """
    <style>
        #MainMenu, footer {visibility: hidden;}

        .app-header {
            padding: 1.25rem 1.5rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
            margin-bottom: 1.5rem;
        }
        .app-header h1 {
            margin: 0;
            font-size: 1.6rem;
            font-weight: 700;
        }
        .app-header p {
            margin: 0.35rem 0 0 0;
            opacity: 0.85;
            font-size: 0.92rem;
        }

        .status-pill {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .pill-ready { background: #DCFCE7; color: #166534; }
        .pill-empty { background: #FEF3C7; color: #92400E; }

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(49, 51, 63, 0.1);
        }

        .stChatMessage { border-radius: 12px; }

        div[data-testid="stChatInput"] {
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

defaults = {
    "collection": None,
    "chunks": None,
    "messages": [],
    "meeting_name": None,
    "processed": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_meeting_state():
    st.session_state.collection = None
    st.session_state.chunks = None
    st.session_state.messages = []
    st.session_state.meeting_name = None
    st.session_state.processed = False


def clear_existing_collection():
    """Wipe any previously stored meeting so old + new chunks never mix."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass  


def process_video(uploaded_file):
    """Run the ingestion pipeline step by step with live UI feedback."""
    video_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    audio_filename = os.path.splitext(uploaded_file.name)[0] + ".wav"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    with st.status("Processing your meeting…", expanded=True) as status:
        st.write("🎧 Extracting audio from video…")
        audio_path = extract_audio(video_path, audio_path)

        st.write("📝 Transcribing audio (this can take a few minutes)…")
        segments = audio2text(audio_path)

        st.write("✂️ Splitting transcript into chunks…")
        chunks = create_chunks(segments)

        st.write("🧠 Generating embeddings…")
        embeddings = embed_chunks(chunks)

        st.write("📚 Clearing previous meeting data & storing new embeddings…")
        clear_existing_collection()
        collection = store_embeddings(embeddings, chunks)

        status.update(label="Meeting processed successfully!", state="complete")

    st.session_state.collection = collection
    st.session_state.chunks = chunks
    st.session_state.meeting_name = uploaded_file.name
    st.session_state.processed = True
    st.session_state.messages = []

st.markdown(
    """
    <div class="app-header">
        <h1>🎙️ MeetingIQ</h1>
        <p>Upload a meeting recording, get an instant transcript-backed Q&A assistant and summary.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
with st.sidebar:
    st.subheader("📁 Meeting Upload")

    if not os.getenv("GEMINI_API_KEY"):
        st.warning("`GEMINI_API_KEY` not found. Add it in the Render Environment Variables.", icon="⚠️")
    uploaded_file = st.file_uploader(
        "Upload a video file",
        type=["mp4", "mov", "mkv", "avi", "webm"],
        help="The audio will be extracted and transcribed automatically.",
    )

    process_clicked = st.button(
        "🚀 Process Meeting",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None,
    )

    if process_clicked and uploaded_file is not None:
        process_video(uploaded_file)
        st.rerun()

    st.divider()

    if st.session_state.processed:
        st.markdown('<span class="status-pill pill-ready">● Meeting Ready</span>', unsafe_allow_html=True)
        st.caption(f"**File:** {st.session_state.meeting_name}")
        st.caption(f"**Chunks indexed:** {len(st.session_state.chunks)}")
    else:
        st.markdown('<span class="status-pill pill-empty">○ No Meeting Loaded</span>', unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True, disabled=not st.session_state.processed):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 New Meeting", use_container_width=True, disabled=not st.session_state.processed):
            reset_meeting_state()
            st.rerun()

    st.divider()
    with st.expander("💡 Example questions"):
        st.markdown(
            "- Summarize this meeting\n"
            "- What decisions were made?\n"
            "- What are the action items?\n"
            "- Were any deadlines mentioned?\n"
            "- What was discussed about the client?"
        )

if not st.session_state.processed:
    st.info(
        "👋 Upload a meeting recording from the sidebar and click **Process Meeting** to get started.",
        icon="🎬",
    )
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Ask something about the meeting, or type 'summarize this meeting'…")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    answer = backend_pipeline(
                        user_query,
                        st.session_state.collection,
                        st.session_state.chunks,
                    )
                except Exception as e:
                    answer = f"⚠️ Something went wrong while generating a response: `{e}`"
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})