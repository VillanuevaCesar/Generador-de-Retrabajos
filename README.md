# Generador-de-Retrabajos
# Automatización de Retrabajos en Línea de Ensamble Electrónico (SMT)

##  Descripción del Problema (Caso de Estudio)
En las plantas de manufactura de tarjetas electrónicas (PCBA) en la industria maquiladora, los defectos de calidad como "Soldadura Insuficiente" o "Componente Desalineado" son detectados en estaciones automáticas de inspección (AOI). Asignar manualmente a dónde debe viajar cada tarjeta defectuosa para ser reparada genera retrasos críticos en las líneas de producción y tiempos muertos.

**El Requerimiento del Cliente:**
El cliente solicitó una herramienta capaz de tomar este ruteo y generar de forma automática una cadena de texto estructurada bajo una sintaxis estricta de tres componentes por cada retrabajo para el sistema de control de piso (MES):
1. `GoToFlowPath[Estación de Destino]`
2. `ReturnStep[Estación de Retorno]`
3. `Reason[Defecto Detectado]`

Si una estación del proceso cuenta con múltiples razones de retrabajo, el sistema debe ser capaz de concatenar las instrucciones de forma secuencial en una única celda de salida, separadas por un espacio y punto y coma `;`.

---

## 🔬 Diario de Investigación y Proceso de Solución

### Fase 1: Análisis del Requerimiento y Descubrimiento de Ambigüedades
Al revisar el material de la maquila, se identificó un escenario crítico: **Una sola estación de inspección puede disparar múltiples caminos de retrabajo independientes.** * *Ejemplo:* En la estación **"Inspección AOI"**, si la tarjeta tiene soldadura insuficiente va a la estación de cautines, pero si tiene un chip desalineado debe ir a una máquina de aire caliente.
* *Decisión de diseño:* Se optó por construir una solución dinámica basada en un **mapeo relacional** (usando dos tablas en Excel), de modo que el software no dependa de reglas fijas en el código (*hardcoded*), sino de lo que el usuario declare en las matrices de entrada.

### Fase 2: Selección de Herramientas e Ingeniería de Solución
Se seleccionó **Python junto con la librería Pandas** debido a la velocidad de procesamiento de dataframes, facilidad de lectura de archivos XLSX mediante `openpyxl` y robustez al agrupar cadenas de texto complejas. Para acelerar el diseño de la lógica de agregación string, se utilizó un modelo de Inteligencia Artificial (Gemini) como copiloto de desarrollo.

### Fase 3: Bitácora de Errores y Lecciones Aprendidas

####  Error 1: Worksheet named 'Pasos_Principales' not found (ValueError)
* **Problema:** Al ejecutar el script por primera vez, Pandas arrojó un error indicando que no encontraba la pestaña especificada.
* **Solución:** Se descubrió que la pestaña en el archivo físico de Excel tenía un espacio invisible al final (`"Pasos_Principales "`). Se corrigió el nombre de la hoja en el archivo de Excel para que coincidiera exactamente con el string buscado por el script.

#### Error 2: Pérdida de formato y sobreescritura de retrabajos
* **Problema:** Al intentar usar un bucle tradicional para iterar por filas, los pasos que tenían más de un retrabajo reescribían la celda previa, dejando únicamente el último retrabajo registrado.
* **Solución:** Se implementó una función lambda combinada con un `.groupby(['FLOW', 'STEP'])` y una agregación `.apply(lambda x: ' '.join(x))`. Esto permitió que todas las reglas de un mismo paso se unieran limpiamente.

---

##  Instrucciones de Uso

### Prerrequisitos
Tener instalado Python 3.8+ y las librerías necesarias:
```bash
pip install pandas openpyxl
