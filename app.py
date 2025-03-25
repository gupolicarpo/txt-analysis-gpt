import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from docx import Document
import PyPDF2

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📚 GPT Academic Text Analyzer (Prototype)")

uploaded_file = st.file_uploader(
    "Upload your thesis file (.txt, .docx, .pdf)", 
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
        st.error("Unsupported file type!")
        st.stop()
    
    prompt = f"""
    Analise detalhadamente o texto acadêmico abaixo quanto à:
    1. Coerência geral.
    2. Qualidade lógica e argumentativa.
    3. Adequação às normas ABNT.
    Forneça sugestões específicas para melhoria, se necessário.

    Texto acadêmico:
    {text}
    """

    with st.spinner("GPT está analisando seu texto..."):
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista acadêmico que ajuda a analisar teses universitárias."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )

    analysis = response.choices[0].message.content
        
    st.success("✅ Análise concluída!")
    st.markdown(analysis)
