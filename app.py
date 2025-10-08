import streamlit as st
import requests
import json
import time
import random

st.set_page_config(page_title="Asistente Universal de Código", page_icon="🚀", layout="wide")
st.title("🚀 Asistente Universal de Programación")
st.markdown("**Como ChatGPT + Gemini + Grok - Pero 100% Gratis y para Todos**")

headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

class AsistenteUniversal:
    def __init__(self):
        self.especialidades = {
            'python': "🐍 Python - Web, Datos, IA, Bots, Automatización",
            'javascript': "📱 JavaScript - Frontend, Backend, Apps Móviles",
            'web': "🌐 Desarrollo Web - HTML, CSS, React, APIs",
            'datos': "📊 Análisis de Datos - Pandas, SQL, Visualización",
            'ia': "🤖 IA y Machine Learning - Modelos, Procesamiento",
            'movil': "📱 Apps Móviles - Android, iOS, React Native",
            'devops': "⚙️ DevOps - Docker, Cloud, Deployment",
            'bd': "🗄️ Bases de Datos - SQL, NoSQL, Optimización",
            'seguridad': "🔒 Seguridad - Ethical Hacking, Pentesting",
            'automatizacion': "⚡ Automatización - Bots, Scripts, Tareas"
        }
    
    def detectar_tema(self, mensaje):
        mensaje = mensaje.lower()
        temas = {
            'python': ['python', 'py', 'pandas', 'django', 'flask', 'script'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular'],
            'web': ['html', 'css', 'web', 'página', 'website', 'frontend'],
            'datos': ['datos', 'data', 'excel', 'csv', 'análisis', 'pandas'],
            'ia': ['ia', 'ai', 'machine learning', 'modelo', 'neuronal'],
            'movil': ['móvil', 'mobile', 'android', 'ios', 'app'],
            'devops': ['docker', 'cloud', 'deploy', 'servidor', 'nginx'],
            'bd': ['base de datos', 'mysql', 'sql', 'mongodb', 'postgresql'],
            'seguridad': ['hacking', 'seguridad', 'pentest', 'vulnerabilidad'],
            'automatizacion': ['automatizar', 'bot', 'script', 'tarea automática']
        }
        
        for tema, palabras in temas.items():
            if any(palabra in mensaje for palabra in palabras):
                return tema
        return 'general'

def obtener_respuesta_universal(mensaje, historial, tema_detectado):
    asistente = AsistenteUniversal()
    tema_nombre = asistente.especialidades.get(tema_detectado, "Programación General")
    
    modelos_tecnicos = [
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
        "https://api-inference.huggingface.co/models/codeparrot/codeparrot",
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    ]
    
    prompts_especializados = {
        'python': f"""Eres un experto en Python. Responde sobre: {mensaje}
        
Ejemplos de ayuda que puedes dar:
- Escribir código Python completo
- Explicar conceptos de programación
- Debuggear errores
- Optimizar código
- Enseñar mejores prácticas
- Sugerir librerías adecuadas

Respuesta útil:""",

        'javascript': f"""Eres un experto en JavaScript. Responde sobre: {mensaje}

Puedes ayudar con:
- Código JavaScript/Node.js
- Frameworks (React, Vue, Angular)
- APIs y servicios web
- Desarrollo frontend/backend
- Solución de problemas

Respuesta técnica:""",

        'web': f"""Eres un experto en desarrollo web. Responde sobre: {mensaje}

Áreas de ayuda:
- HTML/CSS/JavaScript
- Frameworks web
- Diseño responsive
- Performance optimization
- SEO y accesibilidad

Respuesta web:""",

        'datos': f"""Eres un experto en análisis de datos. Responde sobre: {mensaje}

Puedes asistir con:
- Análisis con Pandas/NumPy
- Visualización de datos
- Limpieza y procesamiento
- SQL y consultas
- Machine Learning básico

Respuesta datos:""",

        'general': f"""Eres un asistente universal de programación. Responde sobre: {mensaje}

Puedes ayudar con:
- Cualquier lenguaje de programación
- Arquitectura de software
- Resolución de problemas
- Mejores prácticas
- Recursos de aprendizaje

Respuesta general:"""
    }
    
    prompt = prompts_especializados.get(tema_detectado, prompts_especializados['general'])
    
    for modelo_url in modelos_tecnicos:
        try:
            response = requests.post(
                modelo_url,
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 300,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                },
                timeout=15
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado and isinstance(resultado, list) and len(resultado) > 0:
                    texto = resultado[0].get('generated_text', '')
                    if texto and len(texto) > 25:
                        if "Respuesta" in texto:
                            texto = texto.split("Respuesta")[-1].replace(":", "").strip()
                        return f"**🧠 {tema_nombre}:**\n\n{texto}"
            time.sleep(1)
        except:
            continue
    
    respuestas_tecnicas = {
        'python': [
            f"**🧠 {tema_nombre}:**\n\nPara tu consulta sobre Python, te recomiendo:\n\n1. **Para scripts simples:** Usa las librerías estándar de Python\n2. **Para datos:** Pandas y NumPy son excelentes\n3. **Para web:** Flask (simple) o Django (completo)\n4. **Para automatización:** Puedes usar Selenium o BeautifulSoup\n\n¿Podrías darme más detalles específicos sobre lo que necesitas?",
            
            f"**🧠 {tema_nombre}:**\n\nEn Python, puedes abordar esto de varias maneras. Algunas opciones:\n\n- **Librerías útiles:** requests, pandas, selenium, openpyxl\n- **Patrones comunes:** funciones, clases, manejo de excepciones\n- **Buenas prácticas:** PEP8, documentación, testing\n\n¿Qué aspecto específico te interesa más?"
        ],
        
        'javascript': [
            f"**🧠 {tema_nombre}:**\n\nPara desarrollo JavaScript considera:\n\n**Frontend:** React, Vue, Angular\n**Backend:** Node.js, Express\n**Móvil:** React Native, Ionic\n**Bases de datos:** MongoDB, Firebase\n\n¿En qué parte del stack necesitas ayuda?",
        ],
        
        'web': [
            f"**🧠 {tema_nombre}:**\n\nDesarrollo web moderno incluye:\n\n- **Frontend:** HTML5, CSS3, JavaScript ES6+\n- **Frameworks:** React, Vue, Angular\n- **Backend:** Node.js, Python, PHP\n- **Bases de datos:** SQL y NoSQL\n- **DevOps:** Docker, CI/CD\n\n¿Qué tecnología específica te interesa?"
        ],
        
        'general': [
            f"**🧠 {tema_nombre}:**\n\n¡Excelente pregunta técnica! Para darte la mejor ayuda:\n\n1. ¿Qué lenguaje de programación prefieres?\n2. ¿Tienes algún código existente?\n3. ¿Qué resultado esperas obtener?\n4. ¿Hay requisitos específicos?\n\nCon más detalles, puedo darte una solución más precisa. 😊",
            
            f"**🧠 {tema_nombre}:**\n\nInteresante desafío técnico. Podemos abordarlo de varias formas:\n\n- **Análisis del problema** y posibles soluciones\n- **Código de ejemplo** en el lenguaje que prefieras\n- **Optimizaciones** y mejores prácticas\n- **Recursos** para aprender más\n\n¿Por dónde quieres que empecemos?"
        ]
    }
    
    return random.choice(respuestas_tecnicas.get(tema_detectado, respuestas_tecnicas['general']))

def generar_ejemplo_rapido(tema):
    ejemplos = {
        'python': """
```python
# Ejemplo práctico de Python
def procesar_archivos(ruta):
    import os
    import pandas as pd
    
    for archivo in os.listdir(ruta):
        if archivo.endswith('.csv'):
            datos = pd.read_csv(os.path.join(ruta, archivo))
            print(f"Procesado: {archivo}")
    
    return "Procesamiento completado"
