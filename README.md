# Pipeline NLP con spaCy

Implementación de un pipeline de Procesamiento de Lenguaje Natural (NLP) clásico utilizando spaCy (`es_core_news_lg`) para español, con interfaz web Flask y etiquetado EAGLES/FreeLing.

## Pipeline

1. **Segmentación en frases**
2. **Tokenización**
3. **Lematización** (con normalización de adjetivos: femenino → masculino singular)
4. **POS Tagging** con etiquetas EAGLES/FreeLing (NCMS000, VMIS3P0, DI0MS0, etc.)
5. **Eliminación de stopwords**

## Correcciones aplicadas

| Problema | Solución |
|---|---|
| Verbos en pasado etiquetados como Imperfecto (I) | Mapeo `Tense=Past` → `S` (VMIS3P0) |
| Adjetivos femeninos lematizados como femeninos | `_lemma_normalizado()` → masculino singular |
| Artículos indefinidos (`un`/`una`) como definidos | `Definite=Ind` → `DI0...`, `Definite=Def` → `DA0...` |
| `calamar` analizado como verbo | Reclasificado a NCMS000 si va tras determinante |
| `siquiera` analizado como sustantivo | Forzado a ADV (RG) + stopword |
| `Sin embargo` como preposición + sustantivo | Detectado como locución CC + stopword |

## Archivos

| Archivo | Descripción |
|---|---|
| `nlp_pipeline.py` | Clase `NLPipeline` con las 5 etapas, mapeo EAGLES, correcciones |
| `pipeline_nlp.py` | Script de línea de comandos (`--text`, `--json`) |
| `app.py` | Servidor Flask con interfaz web y API REST `/api/procesar` |
| `templates/index.html` | Plantilla HTML con selectores de etapa |
| `static/style.css` | Estilos modernos responsive |
| `Procfile` | `web: gunicorn app:app` (para Render, Fly.io, etc.) |
| `runtime.txt` | Versión de Python para el cloud |
| `salida_terminal.txt` | Output completo del pipeline |
| `session-ses_1c36.md` | Bitácora completa de la sesión con OpenCode |

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download es_core_news_lg
python app.py
```

Abrir `http://localhost:5000` en el navegador.

### CLI

```powershell
python pipeline_nlp.py
python pipeline_nlp.py --text "Tu texto aquí"
python pipeline_nlp.py --json
```

## Deploy en Render

1. Crear cuenta en https://render.com
2. Conectar repositorio de GitHub
3. Crear **Web Service**
   - Runtime: **Python**
   - Build Command: `pip install -r requirements.txt && python -m spacy download es_core_news_lg`
   - Start Command: `gunicorn app:app`
4. Desplegar

El servicio quedará disponible en `https://<nombre>.onrender.com`

## Créditos

Construido de forma agéntica con [OpenCode](https://opencode.ai) y spaCy.
