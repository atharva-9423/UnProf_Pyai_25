<div align="center">

# 🎨 Day 25 — Streamlit Chatbot UI
### Clean, Minimal, and Beautiful

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)

*Bringing our CLI RAG Chatbot to life with a beautiful, modern graphical user interface.*

</div>

---

## 📖 Overview

For Day 25, we transition our AI from the terminal to the web! We wrapped our Conversational RAG pipeline in a **Streamlit** frontend. 
This UI is designed with a focus on **strong typography** (using the Inter font) and **minimalism**, giving it a premium feel similar to ChatGPT or Claude.

## ✨ Key Features

- **🎨 Premium UI:** Custom CSS applied for strong headings, a clean layout, and modern floating input boxes.
- **💬 Streamlit Chat Interface:** Uses native `st.chat_message` and `st.chat_input` for a seamless conversational experience.
- **💾 Session Memory:** Utilizes `st.session_state` to permanently display chat bubbles and remember conversation context.
- **⚡ Performance Caching:** Utilizes `@st.cache_resource` to ensure the FAISS index is only loaded once when the server boots.

## 🚀 Setup & Usage

### 1. Install Dependencies
Navigate to the `day25` folder and install dependencies:
```bash
cd day25
pip install -U -r requirements.txt
```

### 2. Set the Gemini API Key
Provide your valid Google Gemini API key as an environment variable (Must start with `AIza`):

**Windows (PowerShell)**
```powershell
$env:GEMINI_API_KEY="AIza..."
```

### 3. Run the Streamlit Application
Unlike standard Python scripts, Streamlit applications are run using the `streamlit run` command:
```bash
streamlit run app.py
```
*(This will automatically open the web app in your default browser at `http://localhost:8501`)*

### 4. Start Chatting!
The chatbot will load the built-in static documents (`day25/documents/sample_notes.txt`). Try asking it some questions and follow-ups!

---
<div align="center">
<i>Built for the 100 Days of Code challenge. Phase 4 - UI & Deployment.</i>
</div>
