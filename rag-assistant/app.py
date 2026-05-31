import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="LLM Powered RAG Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🤖 LLM Powered RAG Assistant")

st.markdown(
    "Upload PDFs → Ask Questions → Get AI Answers"
)

# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        with st.spinner("Uploading PDFs..."):

            files = []

            for file in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            file.name,
                            file,
                            "application/pdf"
                        )
                    )
                )

            response = requests.post(
                "http://127.0.0.1:8000/upload-pdf/",
                files=files
            )

        result = response.json()

        st.success("PDFs Uploaded Successfully")

        st.write(result)

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()

# ---------------- QUESTION INPUT ----------------

question = st.text_input(
    "Ask Question From PDFs"
)

# ---------------- RESUME ANALYZER ----------------

if st.button("📄 Analyze Resume"):

    with st.spinner("Analyzing Resume..."):

        response = requests.post(
            "http://127.0.0.1:8000/ask/",
            params={
                "question": """
Analyze this resume and provide:

1. ATS Score
2. Technical Skills
3. Missing Skills
4. Best Job Roles
5. Resume Improvements
6. Interview Questions
"""
            }
        )

        data = response.json()

        if "answer" in data:

            st.subheader("📊 Resume Analysis")

            st.write(data["answer"])

        else:

            st.error(data["error"])

# ---------------- PDF SUMMARY ----------------

if st.button("📝 Summarize PDF"):

    with st.spinner("Generating Summary..."):

        response = requests.post(
            "http://127.0.0.1:8000/ask/",
            params={
                "question": "Give a detailed summary of the uploaded PDFs."
            }
        )

        data = response.json()

        if "answer" in data:

            st.subheader("📚 PDF Summary")

            st.write(data["answer"])

        else:

            st.error(data["error"])

# ---------------- ASK BUTTON ----------------

if st.button("Ask AI"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask/",
                params={
                    "question": question
                }
            )

            data = response.json()

            if "answer" in data:

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": data["answer"]
                    }
                )

            else:

                st.error(data["error"])

# ---------------- CHAT HISTORY ----------------

st.divider()

st.subheader("💬 Chat History")

for chat in reversed(st.session_state.chat_history):

    with st.chat_message("user"):

        st.write(chat["question"])

    with st.chat_message("assistant"):

        st.write(chat["answer"])

    st.divider()