import streamlit as st
from google import genai

# Configuración con el NUEVO cliente
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mi Chatbot IA", page_icon="🤖")
st.title("🤖 Mi Asistente IA Personal")
st.write("¡Hola! Soy tu asistente personal. ¿En qué puedo ayudarte?")

# Input del usuario
pregunta = st.text_input("Escribe tu pregunta aquí:")

if pregunta:
    try:
        with st.spinner("Pensando..."):
            # USAR EL NUEVO MÉTODO DE LA DOCUMENTACIÓN
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Modelo actualizado
                contents=pregunta
            )
        
        st.success("Respuesta:")
        st.write(response.text)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Probando con modelo alternativo...")
        
        # Intentar con modelo alternativo si falla
        try:
            with st.spinner("Probando modelo alternativo..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=pregunta
                )
            st.success("Respuesta:")
            st.write(response.text)
        except Exception as e2:
            st.error(f"Error con modelo alternativo: {str(e2)}")
