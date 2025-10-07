import streamlit as st
import openai

# Configuración de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("🤖 Mi ChatGPT Personal")
st.write("¡Hola! Soy tu asistente basado en ChatGPT. ¿En qué puedo ayudarte?")

# Input del usuario
pregunta = st.text_input("Escribe tu mensaje:")

if pregunta:
    try:
        with st.spinner("Pensando..."):
            # Llamar a la API de OpenAI
            response = openai.ChatCompletion.create(
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
