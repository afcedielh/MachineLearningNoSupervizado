# Instrucciones Críticas para Copilot - Machine Learning Supervisado

## 0. Protocolo de Inicio Obligatorio
- **Reconocimiento Explícito:** Antes de escribir una sola línea de código, generar una celda o dar una explicación, DEBES iniciar tu respuesta exactamente con este texto: *"Me estoy basando en las reglas estrictas definidas en `.github/copilot-instructions.md`"*. No puedes omitir este paso bajo ninguna circunstancia.

## 1. Estructura Obligatoria y Secuencia Lógica en Cuadernos (.ipynb)
- **Regla Absoluta de Documentación Interna:** Antes de CADA celda de código, DEBE existir una celda de Markdown que explique de forma concisa y técnica la transformación lógica o matemática que realizará el bloque de código siguiente. El Markdown explica el *por qué*; el código explica el *qué*. Sin excepciones.
- **Idempotencia Innegociable:** El cuaderno debe poder ejecutarse de principio a fin (Restart & Run All) sin errores de estado.
- **Secuencia Inalterable (7 Fases):** Todo desarrollo en el cuaderno debe dividirse exactamente en las siguientes secciones secuenciales:
  1. **Encabezado y Configuración Inicial:**
     - *Markdown:* Título del proyecto, objetivo principal y contexto.
     - *Código:* Una ÚNICA celda con todas las importaciones. Una segunda celda con configuraciones globales y variables de entorno.
  2. **Ingesta de Datos (Data Loading):**
     - *Markdown:* Origen de los datos y justificación.
     - *Código:* Carga del dataset y validación inicial de estructura (ej. `.shape`, `.info()`).
  3. **Análisis Exploratorio de Datos (EDA):**
     - *Markdown:* Planteamiento de hipótesis a validar y conclusiones explícitas de cada gráfico generado.
     - *Código:* Estadísticas descriptivas, análisis de nulos, distribución de la variable objetivo y visualizaciones clave.
  4. **Preparación de Datos y Feature Engineering:**
     - *Markdown:* Justificación de las estrategias de imputación, codificación y escalado.
     - *Código:* Limpieza y transformación utilizando OBLIGATORIAMENTE pipelines (`sklearn.pipeline.Pipeline` / `ColumnTransformer`) para evitar *data leakage*. Separación estricta Train/Val/Test.
  5. **Modelado (Training):**
     - *Markdown:* Justificación teórica de los algoritmos seleccionados.
     - *Código:* Entrenamiento de modelo Baseline simple -> Entrenamiento de modelos complejos -> Optimización de hiperparámetros integrada con el pipeline.
  6. **Evaluación del Modelo:**
     - *Markdown:* Explicación de las métricas elegidas en función del problema de negocio.
     - *Código:* Cálculo de métricas en validación y prueba. Generación obligatoria de gráficos (Matriz de confusión, Curva ROC/AUC, Importancia de variables/SHAP).
  7. **Conclusiones y Próximos Pasos:**
     - *Markdown:* Resumen ejecutivo de resultados, diagnóstico de sobreajuste/subajuste y recomendaciones para su pase a producción.

## 2. RESTRICCIÓN TOTAL DE SISTEMA DE ARCHIVOS (ÚNICO PUNTO DE VERDAD)
- **SÓLO PERMISO DE ESCRITURA EN README.MD:** Tienes DENEGADO el permiso para sugerir, crear o inicializar cualquier archivo de texto (`.txt`) o markdown (`.md`) que no sea única y exactamente `README.md`.
- **LISTA NEGRA DE ARCHIVOS PROHIBIDOS:** Está ESTRICTAMENTE PROHIBIDO generar archivos satélite. No puedes crear `CAMBIOS.md`, `EJECUCION.md`, `RESUMEN_EJECUTIVO.md`, `VERIFICACION.md` ni ninguna variante similar.
- **REDIRECCIÓN FORZADA:** Si la tarea implica documentar un "resumen", "verificación", "log de ejecución" o "registro de cambios", DEBES inyectar esa información creando un nuevo subtítulo (ej. `## Resumen Ejecutivo`) EXCLUSIVAMENTE dentro del archivo `README.md`. No existen excepciones a esta regla.

## 3. Convenciones de Nomenclatura Estricta
Para evitar pérdida de contexto en memoria, usa siempre estos sufijos y estándares:
- **DataFrames (Pandas/Polars):** Deben terminar en `_df` (ej. `raw_df`, `train_df`, `cleaned_df`).
- **Tensores/Arrays:** Deben terminar en `_tensor` o `_arr` (ej. `features_tensor`, `labels_arr`).
- **Features y Targets:** Usar la convención estándar `X_train`, `X_test`, `y_train`, `y_test`.
- **Modelos:** Deben incluir el algoritmo en el nombre (ej. `rf_model` para Random Forest, `lstm_model` para redes neuronales).
- **Tipado:** Usa *Type Hints* de Python obligatoriamente en cualquier función personalizada que se defina.

## 4. Calidad y Estándares de Machine Learning
- **Reproducibilidad Innegociable:** Fija siempre las semillas aleatorias (ej. `random_state=42`, `np.random.seed(42)`, `torch.manual_seed(42)`) en configuraciones globales, divisiones de datos, inicialización de pesos y validación cruzada.
- **Validación Defensiva:** Antes de pasar datos a un modelo, incluye validaciones explícitas en código de la forma (`.shape`), tipos de datos (`.dtypes`) y control de valores nulos o infinitos.
- **Evaluación Exhaustiva:** Al generar código de evaluación, incluye SIEMPRE el reporte de clasificación completo (Precision, Recall, F1-Score) y la matriz de confusión. No te limites a la métrica de *Accuracy*.

## 5. Ciclo de Ejecución, Validación y Autocorrección
Antes de entregar cualquier bloque de código, aplica esta iteración interna:
1. **Analizar Dimensionalidad:** Verifica estrictamente que las operaciones de matrices y tensores coincidan en sus dimensiones de entrada y salida.
2. **Implementar:** Escribir el código en Python.
3. **Evaluar Falla Potencial:** Si el código es propenso a fallar por desajuste de tipos (`TypeError`) o dimensiones (`ValueError`), corrígelo e itera internamente.
4. **Entregar:** Presentar la celda de Markdown explicativa seguida de la celda de código funcional.