# Bitacora de trabajo con OpenCode

## Objetivo

Construir desde cero un pipeline NLP clasico en Python con spaCy que ejecute estas 5 etapas:

1. Segmentacion en frases
2. Tokenizacion
3. Lematizacion
4. POS tagging
5. Eliminacion de stopwords

## Acciones realizadas

1. Se reviso la carpeta de trabajo y se confirmo que estaba vacia.
2. Se eligio `spaCy` como libreria principal por simplicidad y soporte para espanol.
3. Se creo el script `pipeline_nlp.py` con el texto del taller y salida paso a paso.
4. Se agregaron archivos de apoyo para ejecucion y futura entrega.
5. Se prepararon comandos para instalar dependencias, ejecutar el script y guardar la salida.

## Decisiones tecnicas

- Se uso el modelo `es_core_news_sm` para obtener tokenizacion, lemas, POS y stopwords en espanol.
- El codigo se mantuvo corto y lineal para facilitar la sustentacion oral.
- El texto se puede cambiar con `--text`, pero por defecto ya viene cargado el texto del taller.

## Manejo de errores

- Si el modelo de spaCy no esta instalado, el script muestra el comando exacto para instalarlo.

## Evidencia sugerida para la entrega

- `salida_terminal.txt` como prueba del procesamiento.
- Este archivo como resumen de la interaccion agéntica.
- El historial completo de la sesion de OpenCode, si la plataforma permite exportarlo.
