import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="Mi Chatbot Gratuito", page_icon="🤖")
st.title("🤖 Mi Asistente IA 100% Gratis")
st.write("¡Hola! Funciono con modelos de Hugging Face usando tu token personal")

# Configuración con TU token
API_URLS = [
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
]

headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

def query_huggingface(prompt, model_url):
    try:
        response = requests.post(model_url, headers=headers, json={"inputs": prompt})
        return response.json()
    except:
        return None

def get_ai_response(user_input):
    """Obtiene respuesta de múltiples modelos con tu token"""
    
    # Intentar con cada modelo
    for model_url in API_URLS:
        try:
            result = query_huggingface(user_input, model_url)
            
            if result and isinstance(result, list) and len(result) > 0:
                response_text = result[0].get('generated_text', '')
                if response_text and len(response_text) > 10:
                    return response_text
                    
        except Exception as e:
            continue
    
    # Respuestas amigables si todos los modelos fallan
    fallback_responses = [
        "¡Hola! Soy tu asistente IA. En este momento los servidores gratuitos están muy solicitados, pero estoy aquí para ayudarte. ¿En qué más puedo asistirte?",
        "¡Hola! Los sistemas de IA están procesando muchas solicitudes. ¿Puedes reformular tu pregunta o intentar en un minuto?",
        "¡Hola! Veo que quieres conversar. Los servicios gratuitos están temporariamente ocupados, pero me encanta ayudarte. ¿Qué más te gustaría saber?",
        "¡Hola! Los modelos de IA están cargando debido a alta demanda. Mientras tanto, ¿puedo ayudarte con algo específico?"
    ]
    
    import random
    return random.choice(fallback_responses)

# Interfaz de chat mejorada
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar historial de chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if user_input := st.chat_input("Escribe tu mensaje aquí..."):
    # Mostrar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Obtener y mostrar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Conectando con servicios IA..."):
            response = get_ai_response(user_input)
        
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
