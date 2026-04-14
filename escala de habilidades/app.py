import streamlit as st
import pandas as pd

# Configuración visual
st.set_page_config(page_title="Sistema de Evaluación Goldstein", layout="centered")

# --- BASE DE DATOS INTERNA (Extraída de tus archivos) ---
GRUPOS = {
    "Grupo I: Primeras Habilidades": list(range(1, 9)),
    "Grupo II: Habilidades Avanzadas": list(range(9, 15)),
    "Grupo III: Habilidades Relacionadas con los Sentimientos": list(range(15, 22)),
    "Grupo IV: Habilidades Alternativas a la Agresión": list(range(22, 31)),
    "Grupo V: Habilidades para hacer frente al Estrés": list(range(31, 43)),
    "Grupo VI: Habilidades de Planificación": list(range(43, 51))
}

# Baremos de Eneatipos (Según el Manual para Estudiantes de Psicología)
BAREMOS = {
    "I": {9:38, 8:35, 7:33, 6:30, 5:28, 4:26, 3:23, 2:21, 1:0},
    "II": {9:28, 8:26, 7:24, 6:22, 5:21, 4:19, 3:17, 2:15, 1:0},
    "III": {9:33, 8:31, 7:29, 6:26, 5:24, 4:22, 3:20, 2:17, 1:0},
    "IV": {9:43, 8:41, 7:38, 6:36, 5:33, 4:31, 3:29, 2:26, 1:0},
    "V": {9:56, 8:53, 7:49, 6:46, 5:42, 4:39, 3:35, 2:32, 1:0},
    "VI": {9:40, 8:38, 7:35, 6:33, 5:31, 4:28, 3:26, 2:23, 1:0},
    "TOTAL": {9:228, 8:216, 7:204, 6:192, 5:181, 4:169, 3:157, 2:145, 1:0}
}

# Preguntas exactas del PDF
PREGUNTAS = [
    "Prestar atención a la persona que habla", "Hablar de temas poco importantes",
    "Hablar sobre cosas que interesan a ambos", "Clarificar información necesaria",
    "Agradecer favores", "Darse a conocer por iniciativa propia",
    "Ayudar a que otros se conozcan", "Hacer cumplidos",
    "Pedir ayuda", "Integrarse en un grupo", "Explicar cómo hacer una tarea",
    "Seguir instrucciones", "Pedir disculpas", "Persuadir a los demás",
    "Reconocer emociones propias", "Expresar sentimientos", "Comprender sentimientos de otros",
    "Comprender el enfado ajeno", "Expresar afecto", "Controlar el miedo",
    "Autorrecompensarse", "Pedir permiso", "Compartir algo", "Ayudar a los demás",
    "Negociar", "Controlar el carácter", "Defender los propios derechos",
    "Responder a las bromas", "Evitar problemas a los demás", "No entrar en peleas",
    "Quejarse", "Responder a una queja", "Demostrar deportividad",
    "Manejar la vergüenza", "Manejar el aislamiento", "Defender a un amigo",
    "Responder a la persuasión", "Responder al fracaso", "Manejar mensajes contradictorios",
    "Responder a una acusación", "Prepararse para una conversación difícil",
    "Hacer frente a la presión de grupo", "Tomar decisiones", "Discernir la causa de un problema",
    "Establecer un objetivo", "Determinar las propias habilidades", "Recoger información",
    "Resolver problemas según su importancia", "Tomar una decisión", "Concentrarse en una tarea"
]

def calcular_enea(punto, clave):
    for e, limite in sorted(BAREMOS[clave].items(), reverse=True):
        if punto >= limite: return e
    return 1

def interpretar(e):
    if e >= 7: return "Nivel Superior / Competencia Alta"
    if e >= 4: return "Nivel Promedio / Normal"
    return "Nivel Bajo / Deficiente"

# --- INTERFAZ ---
st.header("Escala de Habilidades Sociales de Goldstein")
nombre = st.text_input("Nombre del Evaluado")

respuestas = {}
for i, p in enumerate(PREGUNTAS, 1):
    respuestas[i] = st.select_slider(f"{i}. {p}", options=[1, 2, 3, 4, 5], 
                                     help="1: Nunca, 5: Siempre")

if st.button("Generar Informe"):
    st.subheader(f"Resultados de: {nombre}")
    
    res_finales = []
    total_pd = 0
    
    for g_nombre, items in GRUPOS.items():
        pd_grupo = sum(respuestas[idx] for idx in items)
        total_pd += pd_grupo
        clave = g_nombre.split(" ")[1].replace(":", "")
        enea = calcular_enea(pd_grupo, clave)
        
        res_finales.append({
            "Área": g_nombre,
            "Puntaje": pd_grupo,
            "Eneatipo": enea,
            "Diagnóstico": interpretar(enea)
        })
    
    st.table(pd.DataFrame(res_finales))
    
    # Puntaje Total
    enea_t = calcular_enea(total_pd, "TOTAL")
    st.metric("Eneatipo Total", enea_t, help="Basado en baremos universitarios")
    st.info(f"**Interpretación General:** {interpretar(enea_t)}")
    
    # Sección de Recomendaciones
    st.subheader("Asesoría y Recomendaciones")
    for r in res_finales:
        if r["Eneatipo"] <= 3:
            st.error(f"⚠️ **Reforzar {r['Área']}:** Se sugiere entrenamiento en técnicas de modelado y rol-playing.")
        elif r["Eneatipo"] >= 7:
            st.success(f"✅ **Fortaleza en {r['Área']}:** El evaluado muestra liderazgo en este campo.")