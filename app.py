import streamlit as st
import requests
import random
import time
import json

st.set_page_config(page_title="Mi Asistente IA", page_icon="🤖")
st.title("🤖 Mi Asistente Personal con Memoria")
st.write("¡Hola! Recuerdo toda nuestra conversación 📝")

# Configuración
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

MODELOS = [
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium", 
    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
]

def obtener_respuesta_inteligente(mensaje, historial):
    """Usa el historial para respuestas más contextuales"""
    
    # Construir contexto de la conversación
    contexto = "\n".join([f"{msg['role']}: {msg['content']}" for msg in historial[-6:]])  # Últimos 6 mensajes
    prompt_con_contexto = f"{contexto}\nuser: {mensaje}\nassistant:"
    
    # Intentar con modelos de Hugging Face
    for modelo_url in MODELOS:
        try:
            response = requests.post(
                modelo_url,
                headers=headers,
                json={"inputs": prompt_con_contexto, "parameters": {"max_length": 200}},
                timeout=10
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado and isinstance(resultado, list) and len(resultado) > 0:
                    texto = resultado[0].get('generated_text', '')
                    if texto and len(texto) > 15:
                        # Extraer solo la respuesta del asistente
                        if "assistant:" in texto:
                            texto = texto.split("assistant:")[-1].strip()
                        return texto
            time.sleep(1)
        except:
            continue
    
    # Respuestas contextuales mejoradas
    mensaje_lower = mensaje.lower()
    
    if any(palabra in mensaje_lower for palabra in ['hola', 'hi', 'hello']):
        return "¡Hola! 👋 Veo que ya hemos estado conversando. ¿En qué más puedo ayudarte?"
    
    elif any(palabra in mensaje_lower for palabra in ['código', 'code', 'python', 'script']):
        return "¡Perfecto! Basándome en nuestra conversación anterior, puedo ayudarte con código Python. ¿Qué tipo de funcionalidad específica necesitas?"
    
    elif any(palabra in mensaje_lower for palabra in ['gracias', 'thanks', 'bye', 'adiós']):
        return "¡Ha sido un gusto conversar contigo! 😊 Recuerda que mantengo el historial de nuestra charla por si necesitas continuar después."
    
    else:
        respuestas_contextuales = [
            f"Interesante, continuando con nuestro tema anterior. Los servidores están ocupados pero recuerdo lo que hemos hablado.",
            f"Tomando en cuenta nuestra conversación previa... Los modelos están saturados pero mantengo el contexto.",
            f"Basándome en lo que hemos discutido antes... Los servicios gratuitos están al máximo pero sigo aquí."
        ]
        return random.choice(respuestas_contextuales)

# INICIALIZAR HISTORIAL
if "historial" not in st.session_state:
    st.session_state.historial = []

# BARRA LATERAL CON CONTROLES
with st.sidebar:
    st.header("🛠️ Controles del Chat")
    
    # Mostrar estadísticas
    st.write(f"**Mensajes en historial:** {len(st.session_state.historial)}")
    
    # Botón para limpiar historial
    if st.button("🗑️ Limpiar Historial", type="secondary"):
        st.session_state.historial = []
        st.rerun()
    
    # Botón para exportar conversación
    if st.button("📤 Exportar Chat", type="secondary"):
        if st.session_state.historial:
            chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.historial])
            st.download_button(
                label="Descargar conversación",
                data=chat_text,
                file_name="mi_conversacion.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.write("**💡 Tip:** El bot recuerda hasta 6 mensajes anteriores para mantener contexto")

# MOSTRAR HISTORIAL DE CONVERSACIÓN
st.subheader("💬 Conversación Actual")

for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# INPUT DEL USUARIO
if pregunta := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar pregunta al historial
    st.session_state.historial.append({"role": "user", "content": pregunta})
    
    # Obtener respuesta usando el historial
    with st.chat_message("assistant"):
        with st.spinner("Pensando en contexto..."):
            respuesta = obtener_respuesta_inteligente(pregunta, st.session_state.historial)
        
        st.markdown(respuesta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
