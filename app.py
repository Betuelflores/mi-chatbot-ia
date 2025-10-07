import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="Asistente Amable", page_icon="😊", layout="wide")
st.title("😊 Asistente Virtual Amable")
st.write("¡Hola! Soy tu asistente virtual. Estoy aquí para ayudarte de manera amigable y útil.")

# Configuración
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

MODELOS = [
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium", 
]

def obtener_respuesta_amable(mensaje, historial):
    """Sistema de respuestas amable y útil"""
    
    mensaje = mensaje.lower().strip()
    
    # RESPUESTAS AMABLES Y POSITIVAS
    respuestas_directas = {
        # Saludos
        'hola': "¡Hola! 😊 ¿En qué puedo ayudarte hoy?",
        'hi': "¡Hola! 😊 ¿Cómo puedo asistirte?",
        'hello': "¡Hello! 😊 How can I help you today?",
        
        # Preguntas sobre código
        'código': "¡Claro! Me encanta ayudar con código Python. ¿Qué tipo de script necesitas? Por ejemplo: automatización, análisis de datos, o una herramienta específica.",
        'code': "¡Sure! I'd be happy to help with Python code. What kind of script are you thinking about?",
        'python': "¡Python es genial! 🐍 ¿En qué proyecto estás trabajando? Puedo ayudarte con ideas, código o resolver dudas.",
        'script': "¡Perfecto! Cuéntame más sobre lo que quieres que haga el script. ¿Es para procesar datos, interactuar con una API, o algo diferente?",
        
        # Funcionalidades
        'qué puedes hacer': "Puedo ayudarte con una variedad de temas: programación en Python, explicaciones técnicas, ideas de proyectos, y más. ¡Solo pregúntame!",
        'qué sabes hacer': "Sé sobre desarrollo de software, especialmente Python, automatización, análisis de datos, y puedo explicar conceptos de programación. ¡Estoy aquí para ayudarte!",
        
        # Agradecimientos
        'gracias': "¡De nada! 😊 Me alegra poder ayudarte. ¿Hay algo más en lo que pueda asistirte?",
        'thanks': "You're welcome! 😊 Glad I could help. Let me know if you need anything else.",
        
        # Despedidas
        'adiós': "¡Hasta luego! 👋 Fue un gusto ayudarte. ¡Éxito en tu proyecto!",
        'bye': "Goodbye! 👋 Wishing you success with your project!",
        'chao': "¡Chao! 😊 Espero verte pronto. ¡Cuídate!",
    }
    
    # Buscar respuesta directa primero
    for palabra, respuesta in respuestas_directas.items():
        if palabra in mensaje:
            return respuesta
    
    # Si es una pregunta específica, dar respuestas más elaboradas
    if '?' in mensaje or any(palabra in mensaje for palabra in ['cómo', 'how', 'qué es', 'what is']):
        preguntas_especificas = {
            'python': "Python es un lenguaje de programación versátil y fácil de aprender. Es excelente para principiantes y poderoso para expertos. ¿Te interesa alguna librería en particular?",
            'script': "Un script es un programa que automatiza tareas. En Python, podemos escribir scripts para casi cualquier cosa. ¿Tienes una tarea específica que quieres automatizar?",
            'web scraping': "El web scraping es una técnica para extraer información de sitios web. En Python, usamos bibliotecas como BeautifulSoup y Scrapy. ¿Qué datos te gustaría obtener?",
            'automatización': "La automatización con Python puede hacer tu vida más fácil. Podemos automatizar tareas repetitivas como procesar archivos, enviar correos, o incluso controlar otras aplicaciones.",
            'api': "Las APIs son interfaces que permiten que diferentes aplicaciones se comuniquen. En Python, la librería 'requests' es muy popular para trabajar con APIs.",
            'datos': "El análisis de datos es una de las fortalezas de Python. Con librerías como Pandas y NumPy, podemos procesar y analizar datos eficientemente.",
        }
        
        for tema, respuesta in preguntas_especificas.items():
            if tema in mensaje:
                return respuesta
    
    # Intentar con modelos de Hugging Face solo si no tenemos respuesta directa
    contexto = "\n".join([f"{msg['role']}: {msg['content']}" for msg in historial[-4:]])
    prompt_con_contexto = f"{contexto}\nuser: {mensaje}\nassistant:"
    
    for modelo_url in MODELOS:
        try:
            response = requests.post(
                modelo_url,
                headers=headers,
                json={"inputs": prompt_con_contexto, "parameters": {"max_length": 150}},
                timeout=8
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado and isinstance(resultado, list) and len(resultado) > 0:
                    texto = resultado[0].get('generated_text', '')
                    if texto and len(texto) > 10:
                        if "assistant:" in texto:
                            texto = texto.split("assistant:")[-1].strip()
                        return texto
            time.sleep(1)
        except:
            continue
    
    # RESPUESTAS AMABLES POR DEFECTO - NUNCA GENÉRICAS O TÓXICAS
    respuestas_amables = [
        "¡Interesante pregunta! 😊 ¿Podrías darme más detalles para poder ayudarte mejor?",
        "Me gusta tu consulta. ¿Hay algo específico que te gustaría saber o implementar?",
        "¡Claro! Para darte una mejor respuesta, ¿podrías contarme más sobre lo que necesitas?",
        "Entiendo lo que preguntas. ¿Quieres que profundice en algún aspecto en particular?",
        "¡Perfecto! Estoy aquí para ayudarte. ¿En qué aspecto específico necesitas asistencia?",
    ]
    
    return random.choice(respuestas_amables)

# INICIALIZAR HISTORIAL DE CHAT
if "historial" not in st.session_state:
    st.session_state.historial = []

# BARRA LATERAL AMIGABLE
with st.sidebar:
    st.header("⚙️ Controles del Chat")
    st.write(f"**Mensajes en la conversación:** {len(st.session_state.historial)}")
    
    if st.button("🧹 Limpiar conversación", use_container_width=True, type="secondary"):
        st.session_state.historial = []
        st.rerun()
    
    st.markdown("---")
    st.write("**💡 Ejemplos para probar:**")
    st.code("""
- Hola
- Necesito ayuda con código Python
- ¿Qué puedes hacer?
- Cómo funciona una API
- Gracias
    """)
    
    st.markdown("---")
    st.write("**🌟 Características:**")
    st.write("• 🤝 Respuestas amables")
    st.write("• 💬 Historial completo")
    st.write("• 🆓 100% gratuito")
    st.write("• 🌍 Para todos los usuarios")

# ÁREA PRINCIPAL DE CHAT
st.header("💬 Conversación en Tiempo Real")

# MOSTRAR HISTORIAL COMPLETO DE CONVERSACIÓN
for mensaje in st.session_state.historial:
    if mensaje["role"] == "user":
        # Mensaje del usuario - alineado a la derecha o con estilo diferente
        with st.chat_message("user"):
            st.markdown(f"**Tú:** {mensaje['content']}")
    else:
        # Respuesta del asistente - alineado a la izquierda
        with st.chat_message("assistant"):
            st.markdown(f"**Asistente:** {mensaje['content']}")

# INPUT DEL USUARIO EN LA PARTE INFERIOR
st.markdown("---")
if pregunta := st.chat_input("Escribe tu mensaje aquí...", key="chat_input"):
    
    # MOSTRAR INMEDIATAMENTE EL MENSAJE DEL USUARIO
    with st.chat_message("user"):
        st.markdown(f"**Tú:** {pregunta}")
    
    # AGREGAR AL HISTORIAL
    st.session_state.historial.append({"role": "user", "content": pregunta})
    
    # OBTENER Y MOSTRAR RESPUESTA
    with st.chat_message("assistant"):
        with st.spinner("Pensando en una respuesta útil..."):
            respuesta = obtener_respuesta_amable(pregunta, st.session_state.historial)
        
        st.markdown(f"**Asistente:** {respuesta}")
    
    # AGREGAR RESPUESTA AL HISTORIAL
    st.session_state.historial.append({"role": "assistant", "content": respuesta})
    
    # Hacer scroll automático hacia abajo
    st.rerun()

# PIE DE PÁGINA AMIGABLE
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>🤖 Asistente Virtual Amable - Creado para ayudar a todos los usuarios</p>
        <p>💡 Siempre respetuoso y útil • 🌟 100% Gratuito</p>
    </div>
    """,
    unsafe_allow_html=True
    )
