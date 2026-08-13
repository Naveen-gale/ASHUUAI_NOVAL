# AshuuAI — Antigone Scholar 🎭

AshuuAI is an AI-powered scholar and interactive Retrieval-Augmented Generation (RAG) application trained exclusively on Sophocles' *Antigone*. It answers questions, provides scene summaries, analyzes characters, and generates exam-style questions strictly using the context from the provided text.

## Features ✨

- **Interactive Chat Interface**: A responsive, premium dark-themed UI built with Streamlit.
- **Context-Aware Responses**: Powered by LangChain, FAISS, and HuggingFace embeddings.
- **Strict Guardrails**: Refuses to answer out-of-scope questions that are not related to the play.
- **Fast Generation**: Uses Groq API (Llama 3.3 70B) for rapid and intelligent responses.
- **Rate-limit Handling**: Gracefully handles API rate limits with visual countdowns.

## Project Structure 📁

- `app/main.py`: The Streamlit web application.
- `app/rag.py`: Core RAG logic, Groq LLM setup, and FAISS vector retrieval.
- `app/ingest.py`: Script to process the PDF and build the FAISS vector database.
- `vectorstore/`: Directory containing the pre-built FAISS index.
- `data/`: Directory where the original PDF (`antigone_2.pdf`) is placed.
- `requirements.txt`: Python dependencies.

## Local Setup & Installation 🛠️

### 1. Clone the repository
Ensure you have the project files on your local machine.

### 2. Create a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory (you can copy from `.env.example` if it exists) and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. (Optional) Rebuild the Vector Database
If you need to update the text or rebuild the FAISS index, run:
```bash
python app/ingest.py
```

### 6. Run the Application
Launch the Streamlit app locally:
```bash
streamlit run app/main.py
```
The app will be available at `http://localhost:8501`.

## Deployment 🚀

For detailed deployment instructions, please see the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
