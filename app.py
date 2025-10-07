import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="Mi Asistente IA", page_icon="🤖")
st.title("🤖 Mi Asistente Personal")
st.write("¡Hola! Estoy aquí para ayudarte con lo que necesites")

# Configuración mejorada
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

MODELOS = [
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
    "https://api-inquiry.huggingface.co/models/microsoft/DialoGPT-medium",
    "https://api-inquiry.huggingface.co/models/facebook/blenderbot-400M-distill"
]

def obtener_respuesta_inteligente(mensaje):
    """Versión mejorada con respuestas más contextuales"""
    
    # Primero intentar con Hugging Face
    for modelo_url in MODELOS:
        try:
            response = requests.post(
                modelo_url,
                headers=headers,
                json={"inputs": mensaje, "parameters": {"max_length": 150}},
                timeout=10
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado and isinstance(resultado, list) and len(resultado) > 0:
                    texto = resultado[0].get('generated_text', '')
                    if texto and len(texto) > 15:
                        return texto
            time.sleep(1)
        except:
            continue
    
    # RESPUESTAS MEJORADAS Y CONTEXTUALES
    mensaje_lower = mensaje.lower()
    
    # Detectar tipo de pregunta
    if any(palabra in mensaje_lower for palabra in ['hola', 'hi', 'hello', 'buenas']):
        return "¡Hola! 👋 Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?"
    
    elif any(palabra in mensaje_lower for palabra in ['código', 'code', 'program', 'python', 'script']):
        return "¡Claro! Puedo ayudarte con código Python. ¿Qué tipo de script necesitas? Por ejemplo: 'quiero un script para descargar videos' o 'necesito un bot de Telegram'"
    
    elif any(palabra in mensaje_lower for palabra in ['cómo', 'how', 'funciona', 'ayuda']):
        return "Puedo ayudarte con: programación, ideas de proyectos, explicaciones técnicas, y mucho más. ¿Qué necesitas específicamente?"
    
    elif '?' in mensaje:
        return "Buena pregunta. Los servicios de IA están ocupados en este momento, pero puedo intentar ayudarte si reformulas tu pregunta o me das más detalles."
    
    else:
        respuestas_contextuales = [
            f"Entiendo que quieres hablar sobre '{mensaje}'. Los servidores de IA están temporariamente ocupados, pero estoy aquí para ayudarte. ¿Puedes darme más detalles?",
            f"Interesante pregunta sobre {mensaje}. Los modelos están procesando muchas solicitudes. ¿Te importaría reformularla o intentar en unos minutos?",
            f"¡Me gusta tu mensaje! Los servicios gratuitos están saturados ahora mismo. Mientras se liberan, ¿hay algo específico en lo que pueda asistirte?",
            f"Recibí tu mensaje. Los sistemas de IA están al máximo de capacidad. ¿Puedes intentar de nuevo en un momento o ser más específico en tu consulta?"
        ]
        return random.choice(respuestas_contextuales)

# Interfaz de chat mejorada
if "historial" not in st.session_state:
    st.session_state.historial = []

# Mostrar historial
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Input del usuario
if pregunta := st.chat_input("Escribe tu pregunta aquí..."):
    # Agregar pregunta del usuario
    st.session_state.historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # Obtener respuesta mejorada
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu pregunta..."):
            respuesta = obtener_respuesta_inteligente(pregunta)
        
        st.markdown(respuesta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
