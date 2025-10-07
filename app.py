import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="Mi Asistente IA", page_icon="🤖")
st.title("🤖 Mi Asistente Personal Inteligente")
st.write("¡Hola! Soy tu asistente con respuestas más útiles y precisas 💡")

# Configuración
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

MODELOS = [
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium", 
]

def obtener_respuesta_mejorada(mensaje, historial):
    """Sistema de respuestas mejorado con lógica más inteligente"""
    
    mensaje = mensaje.lower().strip()
    
    # RESPUESTAS ESPECÍFICAS Y ÚTILES - SIN MENSAJES GENÉRICOS
    respuestas_directas = {
        # Saludos
        'hola': "¡Hola! 👋 Soy tu asistente personal. ¿En qué puedo ayudarte hoy?",
        'hi': "¡Hello! 👋 I'm your personal assistant. How can I help you today?",
        'hello': "¡Hello! 👋 I'm your personal assistant. What can I do for you?",
        
        # Preguntas sobre código
        'código': "¡Claro! Puedo ayudarte con código Python. ¿Qué tipo de script necesitas? Por ejemplo: web scraping, automatización, análisis de datos, bots, etc.",
        'code': "¡Sure! I can help with Python code. What kind of script do you need? For example: web scraping, automation, data analysis, bots, etc.",
        'python': "¡Python es genial! 🐍 ¿Qué quieres hacer? Puedo ayudarte con: scripts, APIs, análisis de datos, automatización, web development...",
        'script': "¡Perfecto! Cuéntame qué debe hacer tu script. ¿Es para procesar archivos, conectar con APIs, analizar datos, o algo específico?",
        
        # Funcionalidades
        'qué puedes hacer': "Puedo ayudarte con: programación Python, ideas de proyectos, explicaciones técnicas, resolver dudas, y mucho más. ¿Qué necesitas?",
        'qué sabes hacer': "Sé sobre: desarrollo Python, automatización, análisis de datos, APIs, y puedo explicar conceptos técnicos. ¡Pregúntame lo que quieras!",
        
        # Agradecimientos
        'gracias': "¡De nada! 😊 Me alegra poder ayudarte. ¿Necesitas algo más?",
        'thanks': "You're welcome! 😊 Glad I could help. Need anything else?",
        
        # Despedidas - CORREGIDO ✅
        'adiós': "¡Hasta luego! 👋 Fue un gusto ayudarte.",
        'bye': "Goodbye! 👋 It was a pleasure helping you.",
        'chao': "¡Chao! 😊 Espero verte pronto.",
    }
    
    # Buscar respuesta directa primero
    for palabra, respuesta in respuestas_directas.items():
        if palabra in mensaje:
            return respuesta
    
    # Si es una pregunta específica, dar respuestas más elaboradas
    if '?' in mensaje or any(palabra in mensaje for palabra in ['cómo', 'how', 'qué es', 'what is']):
        preguntas_especificas = {
            'python': "Python es un lenguaje de programación versátil para web, datos, IA y automatización. ¿Quieres saber sobre alguna librería específica como Pandas, Requests, o BeautifulSoup?",
            'script': "Un script Python es un programa que automatiza tareas. Puedo ayudarte a crear uno según tus necesidades específicas.",
            'web scraping': "¡El web scraping es muy útil! Se usa BeautifulSoup o Scrapy para extraer datos de páginas web. ¿Qué datos necesitas obtener?",
            'automatización': "¡La automatización con Python puede ahorrarte mucho tiempo! Podemos crear scripts para procesar archivos, enviar emails, o controlar aplicaciones.",
            'api': "Las APIs permiten que diferentes aplicaciones se comuniquen. Con Python usamos la librería 'requests' para conectarnos a APIs.",
            'datos': "Para análisis de datos usamos Pandas y NumPy. ¿Tienes datos específicos que quieras analizar o procesar?",
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
                json={"inputs": prompt_con_contexto, "parameters": {"max_length": 120}},
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
    
    # RESPUESTAS ÚTILES POR DEFECTO - NUNCA GENÉRICAS
    respuestas_utiles = [
        "¡Interesante pregunta! ¿Podrías darme más detalles para poder ayudarte mejor?",
        "Me gusta tu consulta. ¿Hay algo específico que te gustaría saber o implementar?",
        "¡Claro! Para darte una mejor respuesta, ¿podrías contarme más sobre lo que necesitas?",
        "Entiendo lo que preguntas. ¿Quieres que profundice en algún aspecto en particular?",
        "¡Perfecto! Estoy aquí para ayudarte. ¿En qué aspecto específico necesitas asistencia?",
    ]
    
    return random.choice(respuestas_utiles)

# INICIALIZAR HISTORIAL
if "historial" not in st.session_state:
    st.session_state.historial = []

# BARRA LATERAL MEJORADA
with st.sidebar:
    st.header("🎯 Controles del Chat")
    st.write(f"**📊 Mensajes:** {len(st.session_state.historial)}")
    
    if st.button("🔄 Limpiar Conversación", use_container_width=True):
        st.session_state.historial = []
        st.rerun()
    
    st.markdown("---")
    st.write("**💡 Ejemplos para probar:**")
    st.code("- Hola\n- Ayuda con código Python\n- Qué puedes hacer\n- Web scraping")
    st.markdown("---")
    st.write("**⚡ Ahora con respuestas más rápidas y útiles**")

# MOSTRAR CONVERSACIÓN
st.subheader("💬 Conversación en Tiempo Real")

for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# INPUT DEL USUARIO
if pregunta := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.historial.append({"role": "user", "content": pregunta})
    
    with st.chat_message("assistant"):
        with st.spinner("Buscando la mejor respuesta..."):
            respuesta = obtener_respuesta_mejorada(pregunta, st.session_state.historial)
        
        st.markdown(respuesta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
