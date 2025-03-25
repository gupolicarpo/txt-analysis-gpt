import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📚 GPT Academic Text Analyzer (Prototype)")

uploaded_file = st.file_uploader("Upload your .txt thesis file", type=['txt'])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
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
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista acadêmico que ajuda a analisar teses universitárias."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
        )
        analysis = response['choices'][0]['message']['content']
        
    st.success("✅ Análise concluída!")
    st.markdown(analysis)
