from fastapi import FastAPI, UploadFile, File, Query
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from dotenv import load_dotenv
import chromadb
import os

# ---------------- LOAD ENV ----------------

load_dotenv()

# ---------------- FASTAPI APP ----------------

app = FastAPI()

# ---------------- GROQ CLIENT ----------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- UPLOAD FOLDER ----------------

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- EMBEDDING MODEL ----------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------------- CHROMADB ----------------

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="pdf_data"
)

# ---------------- HOME API ----------------

@app.get("/")
def home():

    return {
        "message": "LLM Powered RAG Assistant Running"
    }

# ---------------- PDF UPLOAD ----------------

@app.post("/upload-pdf/")
async def upload_pdf(
    files: list[UploadFile] = File(...)
):

    all_chunks = []

    for file in files:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        if text.strip() == "":
            continue

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = text_splitter.split_text(text)

        all_chunks.extend(chunks)

    if len(all_chunks) == 0:

        return {
            "error": "No text found in uploaded PDFs"
        }

    embeddings = embedding_model.encode(
        all_chunks
    ).tolist()

    try:

        existing = collection.get()

        if existing["ids"]:
            collection.delete(ids=existing["ids"])

    except:
        pass

    for i, chunk in enumerate(all_chunks):

        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )

    return {
        "message": "PDFs uploaded successfully",
        "total_chunks": len(all_chunks)
    }

# ---------------- ASK QUESTION ----------------

@app.post("/ask/")
async def ask_question(

    question: str = Query(...)

):

    try:

        question_embedding = embedding_model.encode(
            question
        ).tolist()

        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )

        context = ""

        if results and results["documents"]:
            context = "\n".join(
                results["documents"][0]
            )

        if context.strip() == "":
            return {
                "question": question,
                "answer": "No relevant data found in PDFs."
            }

        messages = [

            {
                "role": "system",
                "content": "Answer only from the provided context."
            },

            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ]

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=messages

        )

        answer = response.choices[0].message.content

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }ssssssss