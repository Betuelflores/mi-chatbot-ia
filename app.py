import streamlit as st
import google.generativeai as genai

# Configuración con secrets de Streamlit Cloud
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mi Chatbot IA", page_icon="🤖")
st.title("🤖 Mi Asistente IA Personal")
st.write("¡Hola! Soy tu asistente personal. ¿En qué puedo ayudarte?")

# Input del usuario
pregunta = st.text_input("Escribe tu pregunta aquí:")

if pregunta:
    try:
        # Intentar con el modelo básico que siempre funciona
        model = genai.GenerativeModel('models/gemini-pro')
        
        with st.spinner("Pensando..."):
            respuesta = model.generate_content(pregunta)
        
        st.success("Respuesta:")
        st.write(respuesta.text)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("""
        🔧 Solución:
        1. Ve a Google Cloud Console
        2. Busca 'Gemini API' 
        3. Habilita la API
        4. Espera 5 minutos
        """)
