import os
import sys
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

import streamlit as st
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* Import strong, clean Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    /* Apply globally */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Clean, minimal headings */
    h1 {
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #111827;
        margin-bottom: 0rem;
    }
    
    .subtitle {
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    /* Minimal chat bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border-bottom: 1px solid #F3F4F6;
        padding-bottom: 1.5rem;
    }
    
    /* Floating modern input box */
    .stChatInputContainer {
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Document AI")
st.markdown('<p class="subtitle">An intelligent assistant built with Retrieval-Augmented Generation.</p>', unsafe_allow_html=True)

@st.cache_resource(show_spinner="Booting up AI & Loading Documents...")
def initialize_rag():
    docs_folder = "documents"
    if not os.path.exists(docs_folder):
        st.error(f"Error: '{docs_folder}' folder not found.")
        st.stop()

    loader = DirectoryLoader(docs_folder, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    if "GEMINI_API_KEY" not in os.environ:
        st.error("Please set GEMINI_API_KEY environment variable in your terminal before running this Streamlit app.")
        st.stop()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        google_api_key=os.environ["GEMINI_API_KEY"]
    )

    def get_contextualized_question(inputs):
        history = inputs.get("chat_history", [])
        if not history:
            return inputs["input"]
        
        last_human_query = ""
        for role, text in reversed(history):
            if role == "human":
                last_human_query = text
                break
        return f"{last_human_query} {inputs['input']}"

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise."
        "\n\n"
        "Context: {context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    rag_chain = (
        RunnablePassthrough.assign(
            standalone_question=get_contextualized_question
        )
        | RunnablePassthrough.assign(
            context=lambda x: "\n\n".join(doc.page_content for doc in retriever.invoke(x["standalone_question"]))
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

rag_chain = initialize_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "langchain_history" not in st.session_state:
    st.session_state.langchain_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("Ask a question about the documents..."):

    with st.chat_message("user"):
        st.markdown(query)
    

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:

            for chunk in rag_chain.stream({
                "input": query,
                "chat_history": st.session_state.langchain_history
            }):
                full_response += chunk

                response_placeholder.markdown(full_response + "▌")
  
            response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.langchain_history.append(("human", query))
            st.session_state.langchain_history.append(("ai", full_response))
            
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
