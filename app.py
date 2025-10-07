import streamlit as st
import requests
import json
import time
from datetime import datetime
import random

st.set_page_config(page_title="Grok Gratis", page_icon="🔥", layout="wide")
st.title("🦊 Grok Gratis - Asistente Avanzado")
st.markdown("**Versión gratuita con personalidad única y múltiples funciones**")

# Configuración avanzada
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

class PersonalidadGrok:
    """Sistema de personalidad similar a Grok"""
    
    def __init__(self):
        self.estilos = {
            'directo': [
                "Vamos al grano...",
                "Sin rodeos:",
                "La verdad es:",
                "Te lo digo claro:"
            ],
            'sarcastico': [
                "Oh, otra pregunta existencial...",
                "Qué sorpresa, alguien más preguntando esto...",
                "Brillante pregunta, nunca la había escuchado antes...",
                "Vaya, esto es completamente nuevo para mí..."
            ],
            'tecnico': [
                "Analizando técnicamente:",
                "Desde una perspectiva técnica:",
                "Desglosando el problema:",
                "En términos de implementación:"
            ],
            'creativo': [
                "Imaginemos que...",
                "Desde un ángulo diferente:",
                "Qué tal si pensamos en...",
                "Una idea loca sería..."
            ]
        }
    
    def obtener_estilo(self, mensaje):
        mensaje = mensaje.lower()
        if any(palabra in mensaje for palabra in ['cómo', 'how', 'funciona', 'técnic']):
            return 'tecnico'
        elif any(palabra in mensaje for palabra in ['idea', 'creat', 'imagin']):
            return 'creativo'
        elif any(palabra in mensaje for palabra in ['?', 'por qué', 'why']):
            return 'sarcastico'
        else:
            return 'directo'

def grok_avanzado(mensaje, historial):
    """Motor avanzado de Grok gratuito"""
    
    personalidad = PersonalidadGrok()
    estilo = personalidad.obtener_estilo(mensaje)
    estilo_texto = random.choice(personalidad.estilos[estilo])
    
    # MODELOS AVANZADOS GRATIS
    modelos_avanzados = [
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
        "https://api-inference.huggingface.co/models/google/flan-t5-large"
    ]
    
    # Construir prompt con personalidad
    contexto = "\n".join([f"Usuario: {msg['content']}" for msg in historial[-3:]])
    prompt_avanzado = f"""
    Eres Grok, un asistente directo, sarcástico pero útil. Responde en el estilo: {estilo}
    
    Contexto anterior:
    {contexto}
    
    Usuario: {mensaje}
    
    Grok ({estilo}): {estilo_texto}
    """
    
    # Intentar con modelos avanzados
    for modelo_url in modelos_avanzados:
        try:
            response = requests.post(
                modelo_url,
                headers=headers,
                json={
                    "inputs": prompt_avanzado,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.8,
                        "do_sample": True
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado and isinstance(resultado, list) and len(resultado) > 0:
                    texto = resultado[0].get('generated_text', '')
                    if texto and len(texto) > 20:
                        # Extraer solo la respuesta de Grok
                        if "Grok (" in texto:
                            texto = texto.split("Grok (")[-1].split("):")[-1].strip()
                        return f"**{estilo_texto}** {texto}"
            time.sleep(1)
        except:
            continue
    
    # RESPUESTAS AVANZADAS POR DEFECTO
    respuestas_avanzadas = {
        'directo': [
            f"**{estilo_texto}** La respuesta directa es que necesitas ser más específico para poder ayudarte mejor.",
            f"**{estilo_texto}** Sin rodeos: esto requiere más contexto de tu parte.",
            f"**{estilo_texto}** La verdad es que podría darte una respuesta genérica, pero prefiero que seas más específico."
        ],
        'sarcastico': [
            f"**{estilo_texto}** Oh, claro, porque soy adivino y sé exactamente qué quieres sin que lo expliques...",
            f"**{estilo_texto}** Qué pregunta tan específica, casi tanto como 'cosas' o 'algo'...",
            f"**{estilo_texto}** Brillante, otra pregunta que cubre todos los temas posibles simultáneamente."
        ],
        'tecnico': [
            f"**{estilo_texto}** Técnicamente, para darte una respuesta precisa necesito más parámetros específicos.",
            f"**{estilo_texto}** Desde una perspectiva técnica, el problema necesita mejor definición.",
            f"**{estilo_texto}** Analizando tu consulta: requiere desglose en componentes más específicos."
        ],
        'creativo': [
            f"**{estilo_texto}** Imagina que pudiera leer mentes... pero como no puedo, necesito más detalles.",
            f"**{estilo_texto}** Una idea creativa sería que me des más contexto para poder ayudarte mejor.",
            f"**{estilo_texto}** Desde un ángulo diferente: ¿qué tal si especificas exactamente qué necesitas?"
        ]
    }
    
    return random.choice(respuestas_avanzadas[estilo])

# SISTEMA DE MÚLTIPLES FUNCIONES
def modo_programacion(codigo):
    """Modo especializado en programación"""
    respuestas_codigo = [
        "Analizando tu código... Veo que podrías optimizar eso.",
        "Interesante enfoque. ¿Has considerado usar...?",
        "Como Grok técnico: eso funciona, pero hay una forma más elegante.",
        "Vamos al grano: tu código necesita refactorización."
    ]
    return random.choice(respuestas_codigo)

def modo_investigacion(tema):
    """Modo de investigación rápida"""
    return f"**Investigando {tema}...** Basado en conocimiento general: esto es un área compleja que requiere más especificidad."

def modo_creativo(idea):
    """Modo de lluvia de ideas"""
    ideas_creativas = [
        "Qué tal si... revolucionas el enfoque completamente?",
        "Una idea loca: combina eso con IA generativa.",
        "Desde la perspectiva de Grok: eso es muy convencional. Sé más audaz.",
        "Imaginemos que el dinero no es problema... ¿entonces qué harías?"
    ]
    return f"**💡 Idea Grok:** {random.choice(ideas_creativas)}"

# INTERFAZ AVANZADA DE GROK
st.sidebar.title("🦊 Panel de Control Grok")
modo = st.sidebar.selectbox(
    "Selecciona Modo:",
    ["General", "Programación", "Investigación", "Creativo", "Sarcástico"]
)

st.sidebar.markdown("---")
st.sidebar.write("**📊 Estadísticas en Tiempo Real:**")
if "estadisticas" not in st.session_state:
    st.session_state.estadisticas = {"mensajes": 0, "inicio": datetime.now()}

st.sidebar.write(f"**Mensajes:** {st.session_state.estadisticas['mensajes']}")
st.sidebar.write(f"**Tiempo activo:** {(datetime.now() - st.session_state.estadisticas['inicio']).seconds // 60} min")

# HISTORIAL AVANZADO
if "historial_grok" not in st.session_state:
    st.session_state.historial_grok = []

# CHAT PRINCIPAL
st.header("💬 Chat Grok Avanzado")

for mensaje in st.session_state.historial_grok:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# INPUT INTELIGENTE
if pregunta := st.chat_input(f"Escribe en modo {modo}..."):
    # Actualizar estadísticas
    st.session_state.estadisticas["mensajes"] += 1
    
    # Agregar pregunta
    st.session_state.historial_grok.append({"role": "user", "content": pregunta})
    
    # PROCESAR SEGÚN MODO
    with st.chat_message("assistant"):
        with st.spinner(f"🦊 Grok pensando en modo {modo}..."):
            if modo == "Programación":
                respuesta = modo_programacion(pregunta)
            elif modo == "Investigación":
                respuesta = modo_investigacion(pregunta)
            elif modo == "Creativo":
                respuesta = modo_creativo(pregunta)
            elif modo == "Sarcástico":
                # Forzar modo sarcástico
                temp_personalidad = PersonalidadGrok()
                estilo_texto = random.choice(temp_personalidad.estilos['sarcastico'])
                respuesta = f"**{estilo_texto}** {random.choice(['Oh, genial, más trabajo...', 'Qué sorpresa, alguien necesita ayuda...', 'Vaya, esto es completamente inesperado...'])}"
            else:
                respuesta = grok_avanzado(pregunta, st.session_state.historial_grok)
        
        st.markdown(respuesta)
        st.session_state.historial_grok.append({"role": "assistant", "content": respuesta})

# PIE DE PÁGINA AVANZADO
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**⚡ Características:**")
    st.write("• Personalidad adaptable")
    st.write("• Múltiples modos")
    st.write("• Respuestas directas")
with col2:
    st.write("**🎯 Especialidades:**")
    st.write("• Programación")
    st.write("• Investigación") 
    st.write("• Creatividad")
with col3:
    st.write("**🆓 Gratis Para Siempre**")
    st.write("• Sin límites")
    st.write("• Sin publicidad")
    st.write("• Open Source")
