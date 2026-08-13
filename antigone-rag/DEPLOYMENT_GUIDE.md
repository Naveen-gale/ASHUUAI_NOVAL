# AshuuAI — Deployment Guide 🚀

Since AshuuAI is built using **Streamlit**, the easiest and most cost-effective way to deploy it is via **Streamlit Community Cloud**. It is free, handles Python dependencies automatically, and integrates seamlessly with GitHub.

Here is a step-by-step guide to deploying your project.

---

## 1. Prepare your GitHub Repository

Streamlit Cloud pulls your code directly from GitHub. Before deploying, ensure your code is pushed to a GitHub repository.

1. Create a new repository on [GitHub](https://github.com/).
2. Push your local `antigone-rag` directory to this repository.
   
> **Note:** Ensure `.env` is listed in your `.gitignore` file so you don't accidentally expose your Groq API key to the public! (The vectorstore folder should also be pushed if you want to avoid running ingest.py on the server, but make sure the `.gitignore` doesn't ignore it if you intend to push it).

---

## 2. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click the **"New app"** button.
3. If prompted, authorize Streamlit to access your GitHub repositories.
4. Fill out the deployment form:
   - **Repository**: Select the repository you created for AshuuAI.
   - **Branch**: Select the main branch (e.g., `main` or `master`).
   - **Main file path**: Enter `app/main.py`

### 3. Add Environment Variables (API Keys)

Before hitting deploy, you must add your Groq API key so the cloud app can access it.

1. On the deployment configuration screen, click on **Advanced settings**.
2. In the **Secrets** section, add your environment variables in TOML format:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

3. Click **Save**.

### 4. Deploy!

Click the **Deploy!** button. 

Streamlit will provision a server, install the dependencies from your `requirements.txt`, and launch the application. This process usually takes 1-3 minutes.

---

## Alternative: Deploying to Render / Heroku

If you prefer to deploy using a traditional PaaS like Render or Heroku, you will need to add a `Procfile` or configure the start command.

### Start Command
For Render, Heroku, or any standard VM, the command to run the app is:
```bash
streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0
```

### Render Setup:
1. Create a new "Web Service" on [Render](https://render.com/).
2. Connect your GitHub repository.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0`
5. Go to the **Environment** tab and add your `GROQ_API_KEY` secret.
6. Deploy.

---

## Troubleshooting

- **No module named '...'**: Ensure that all libraries imported in your Python files are listed in `requirements.txt`.
- **FAISS Deserialization Error**: If the app fails to load the vector store on the cloud, ensure you are either pushing the `vectorstore/` folder to GitHub, or you include a build step that runs `python app/ingest.py` before starting the app.
- **Rate Limit Errors**: If users experience rate limits in production, you might need to upgrade your Groq API tier or adjust the `temperature`/`max_tokens`.
