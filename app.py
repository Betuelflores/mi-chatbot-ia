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
        
        # Despedidas
        'adiós': "¡Hasta luego
