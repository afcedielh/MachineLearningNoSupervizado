import streamlit as st
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional

# Scikit-learn Base Classes (Necesarias para deserializar)
from sklearn.base import BaseEstimator, TransformerMixin


# 1. Definición del Transformador (Debe ser idéntico al del Notebook)
class TextPreprocessor(BaseEstimator, TransformerMixin):
    """Limpieza de texto compatible con serialización."""

    def __init__(self, language: str = 'spanish'):
        self.language = language

    def fit(self, X: pd.Series, y: Optional[pd.Series] = None) -> 'TextPreprocessor':
        return self

    def transform(self, X: pd.Series) -> List[str]:
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import SnowballStemmer
        import re

        # Descarga silenciosa en tiempo de ejecución para Streamlit
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)

        stop_words = set(stopwords.words(self.language))
        stemmer = SnowballStemmer(self.language)

        cleaned_texts = []
        for text in X:
            text = str(text).lower()
            text = re.sub(r'[^a-záéíóúñü]', ' ', text)
            words = [stemmer.stem(w) for w in text.split() if w not in stop_words and len(w) > 2]
            cleaned_texts.append(' '.join(words))

        return cleaned_texts


# 2. Carga del Modelo en Caché
@st.cache_resource
def load_model():
    """Carga el pipeline serializado en caché para evitar recargas en cada interacción."""
    try:
        return joblib.load('./models/pipeline_ods.pkl')
    except FileNotFoundError:
        st.error("Error: No se encontró el archivo './models/pipeline_ods.pkl'. Ejecuta el notebook primero.")
        return None


# 3. Interfaz de Usuario (UI)
st.set_page_config(page_title="Clasificador ODS - UNFPA", page_icon="🌍", layout="centered")

st.title("Clasificador de Textos: ODS")

st.divider()

# Input del usuario
texto_usuario = st.text_area("Ingresa el texto a clasificar:", height=150,
                             placeholder="Ejemplo: El gobierno debe invertir en educación pública...")

# Botón de inferencia
if st.button("Clasificar Texto", type="primary"):
    if len(texto_usuario.strip()) < 10:
        st.warning("Por favor, ingresa un texto más descriptivo (mínimo 10 caracteres).")
    else:
        modelo = load_model()

        if modelo is not None:
            with st.spinner('Procesando lenguaje natural e infiriendo...'):
                # Inferencia
                probabilidades = modelo.predict_proba([texto_usuario])[0]
                indice_max = np.argmax(probabilidades)
                prob_max = probabilidades[indice_max]
                ods_predicho = str(modelo.classes_[indice_max]).upper()

                # Evaluación de confianza (Umbral de 40%)
                st.subheader("Resultado de la Evaluación")
                if prob_max < 0.40:
                    st.error("❌ **Fuera de Dominio / Alta Incertidumbre**")
                    st.write(f"El texto no parece relacionarse claramente con un ODS específico.")
                    st.caption(f"Aproximación más cercana: ODS {ods_predicho} ({prob_max:.1%} de confianza).")
                else:
                    st.success(f"**Clasificación Asignada: ODS {ods_predicho}**")
                    st.progress(float(prob_max), text=f"Nivel de Confianza: {prob_max:.1%}")

                    # Mostrar el top 3 de predicciones
                    st.markdown("### Otras probabilidades cercanas:")
                    top_3_idx = np.argsort(probabilidades)[-3:][::-1]
                    for idx in top_3_idx:
                        if idx != indice_max:
                            st.write(f"- **ODS {str(modelo.classes_[idx]).upper()}**: {probabilidades[idx]:.1%}")