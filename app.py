import streamlit as st
import openai

# Configuración OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🤖 Mi Chatbot IA Global")
user_input = st.text_input("Pregúntame lo que quieras:")

if user_input:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=500
        )
        st.write("**Respuesta:**", response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")
