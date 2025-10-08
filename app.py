import streamlit as st
import requests
import json
import time
import random
import tempfile
import subprocess
import os
import shutil
import re

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

    return f"**🧠 {tema_nombre}:**\n\nLo siento, no pude generar una respuesta útil en este momento."

def extraer_codigo(respuesta):
    bloques = re.findall(r"```(?:python)?\n(.*?)```", respuesta, re.DOTALL)
    return "\n\n".join(bloques).strip() if bloques else ""

def ejecutar_codigo_seguro(codigo):
    tmpdir = tempfile.mkdtemp()
    script_path = os.path.join(tmpdir, "script.py")
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(codigo)

        result = subprocess.run(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=6
        )
        salida = result.stdout.decode("utf-8")
        errores = result.stderr.decode("utf-8")
        return salida, errores
    except subprocess.TimeoutExpired:
        return "", "Error: tiempo de ejecución excedido."
    except Exception as e:
        return "", f"Error al ejecutar: {str(e)}"
    finally:
        shutil.rmtree(tmpdir)

# ===== Interfaz principal Streamlit =====

mensaje_usuario = st.text_input("💬 Ingresa tu pregunta o tarea de programación:")

if mensaje_usuario:
    tema = AsistenteUniversal().detectar_tema(mensaje_usuario)
    respuesta = obtener_respuesta_universal(mensaje_usuario, historial=[], tema_detectado=tema)

    st.markdown(respuesta)

    if tema == "python":
        if st.toggle("⚙️ Ejecutar el código generado (Python solo)"):
            codigo = extraer_codigo(respuesta)
            if not codigo:
                st.warning("No se detectó código en la respuesta.")
            else:
                st.text_area("🔍 Código detectado:", codigo, height=200)
                if st.button("▶️ Ejecutar código"):
                    salida, errores = ejecutar_codigo_seguro(codigo)
                    if salida:
                        st.success("✅ Salida del código:")
                        st.code(salida)
                    if errores:
                        st.error("❌ Errores al ejecutar:")
                        st.code(errores)
