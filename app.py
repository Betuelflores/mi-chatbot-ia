import streamlit as st
import google.generativeai as genai

# Configuración de la API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Configuración de la página
st.set_page_config(
    page_title="Mi Chatbot IA",
    page_icon="🤖"
)

# Interfaz de la aplicación
st.title("🤖 Mi Asistente IA Personal")
st.write("¡Hola! Soy tu asistente personal. ¿En qué puedo ayudarte?")

# Input del usuario
pregunta = st.text_input("Escribe tu pregunta aquí:")

# Procesar la pregunta
if pregunta:
    try:
        # Crear el modelo
        model = genai.GenerativeModel('gemini-pro')
        
        # Mostrar spinner mientras se genera la respuesta
        with st.spinner("Pensando..."):
            respuesta = model.generate_content(pregunta)
        
        # Mostrar la respuesta
        st.success("Respuesta:")
        st.write(respuesta.text)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
