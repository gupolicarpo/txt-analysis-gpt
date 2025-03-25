import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from docx import Document
import PyPDF2
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📚 Analisador Acadêmico com Assistente GPT Personalizado")

uploaded_file = st.file_uploader(
    "Faça upload do seu arquivo de texto (.txt, .docx, .pdf)", 
    type=['txt', 'docx', 'pdf']
)

def read_txt(file):
    return file.read().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

if uploaded_file:
    file_type = uploaded_file.type
    
    if file_type == "text/plain":
        text = read_txt(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    elif file_type == "application/pdf":
        text = read_pdf(uploaded_file)
    else:
        st.error("Tipo de arquivo não suportado!")
        st.stop()
    
    # Your custom Assistant ID goes here:
    assistant_id = "asst_7nHbRFcMNeJ83Hpdys4dh4FF"

    with st.spinner("Analisando com o Assistente GPT personalizado..."):
        thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Texto acadêmico para análise detalhada:\n\n{text}"
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Wait for analysis to complete
        while run.status in ["queued", "in_progress"]:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            analysis = messages.data[0].content[0].text.value
            st.success("✅ Análise concluída com sucesso!")
            st.markdown(analysis)
        else:
            st.error("Houve um erro durante a análise. Tente novamente.")
