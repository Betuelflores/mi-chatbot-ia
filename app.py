import streamlit as st
import google.generativeai as genai

# Configuración simple y directa
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Interfaz mínima pero funcional
st.title("🤖 Mi Chatbot IA")
user_input = st.text_input("Pregúntame lo que quieras:")

if user_input:
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        st.write("**Respuesta:**", response.text)
    except Exception as e:
        st.error(f"Error: {e}")
