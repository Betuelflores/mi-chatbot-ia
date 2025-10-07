import streamlit as st
from openai import OpenAI

# Configuración de OpenAI con la nueva API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("🤖 Mi ChatGPT Personal")
st.write("¡Hola! Soy tu asistente basado en ChatGPT. ¿En qué puedo ayudarte?")

# Input del usuario
pregunta = st.text_input("Escribe tu mensaje:")

if pregunta:
    try:
        with st.spinner("Pensando..."):
            # Llamar a la API de OpenAI con la nueva sintaxis
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta}],
                max_tokens=500
            )
        
        # Mostrar la respuesta
        respuesta = response.choices[0].message.content
        st.success("Respuesta:")
        st.write(respuesta)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
