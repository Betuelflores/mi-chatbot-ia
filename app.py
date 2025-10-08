import streamlit as st
import requests
import re
import tempfile
import subprocess
import shutil
import os

st.set_page_config(page_title="Bot Código sin Token", page_icon="🤖", layout="wide")
st.title("🤖 Bot Asistente de Código sin Token")
st.markdown("Preguntame lo que sea o pedime código, ¡te ayudo con respuestas gratuitas!")

def llamar_space(mensaje: str) -> str:
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M"  # Modelo más conversacional
    payload = {"inputs": mensaje, "parameters": {"max_length": 100}}  # Más texto
    try:
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            return resp.json()
        else:
            return f"Error: {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"Excepción: {e}"

def extraer_codigo(texto: str) -> str:
    bloques = re.findall(r"```(?:python)?\n(.*?)```", texto, re.DOTALL)
    return "\n\n".join(bloques).strip() if bloques else ""

def ejecutar_python_simple(codigo: str, timeout: int = 5):
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "script.py")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(codigo)
        proc = subprocess.run(
            ["python3", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        return proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")
    except subprocess.TimeoutExpired:
        return "", "Tiempo excedido."
    except Exception as e:
        return "", f"Error: {e}"
    finally:
        shutil.rmtree(tmp)

mensaje = st.text_input("Escribe tu pregunta o pedí código (ej: 'suma 2+2' o 'escribe un código para sumar'):")
if mensaje:
    respuesta = llamar_space(mensaje)
    st.write("Respuesta completa:")
    st.write(respuesta)

    texto = ""
    if isinstance(respuesta, list) and "generated_text" in respuesta[0]:
        texto = respuesta[0]["generated_text"]
    else:
        texto = str(respuesta)

    st.markdown(texto)

    codigo = extraer_codigo(texto)
    if codigo:
        st.subheader("Código extraído:")
        st.code(codigo, language="python")
        if st.button("Ejecutar código"):
            salida, error = ejecutar_python_simple(codigo)
            if salida:
                st.subheader("Salida:")
                st.code(salida)
            if error:
                st.subheader("Errores:")
                st.error(error)
    else:
        st.info("No detecté código Python, ¡seguí preguntando!")
