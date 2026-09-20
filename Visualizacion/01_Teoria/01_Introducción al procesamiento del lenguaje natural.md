# Laboratorio de Análisis de Textos y Calificaciones

**Curso:** EIN092B - Visualización **Autor:** Jorge Portilla — Depto. de Electrónica e Informática, Universidad Técnica Federico Santa María, Concepción, Chile

Este documento desarrolla los conceptos fundamentales del **procesamiento de lenguaje natural (NLP, por sus siglas en inglés)**, explicando cada técnica de preprocesamiento y representación de texto con mayor profundidad.

---

## 1. Introducción al procesamiento del lenguaje natural

Tradicionalmente, encontrar patrones dentro de un texto era una tarea compleja, ya que el lenguaje humano es ambiguo, variable y dependiente del contexto. El **procesamiento de lenguaje natural (NLP)** surge como un conjunto de técnicas especializadas que permiten que los algoritmos **interpreten o generen texto** para resolver tareas específicas, tales como:

- **Traducción automática**
- **Análisis de sentimientos**
- **Clasificación de texto**
- Entre otras aplicaciones relacionadas con el lenguaje.

### Aplicaciones comunes

El documento menciona ejemplos concretos de dónde se usa NLP en la vida cotidiana:

- **Asistentes virtuales:** Siri, Alexa.
- **Traducción automática:** Google Translate.
- **Chatbots.**
- **Análisis de sentimientos** (por ejemplo, determinar si una reseña de producto es positiva o negativa).

Todas estas aplicaciones dependen de una cadena de pasos de preprocesamiento que transforman el texto "crudo" (tal como lo escribe una persona) en una representación que un algoritmo pueda procesar matemáticamente. El resto del documento recorre esa cadena paso a paso.

---

## 2. Tokenización (Tokenizer)

La **tokenización** es el proceso de dividir un texto en unidades más pequeñas llamadas **tokens**. Es habitualmente el **primer paso** en casi cualquier pipeline de NLP, ya que permite convertir un bloque de texto continuo en piezas manejables para el análisis.

### ¿Qué puede ser un token?

- Una **palabra individual**.
- Una **frase**.
- Una **oración**.

### Ejemplo del documento

```
Texto:   "¿Para qué hacer esto?"
Tokens:  ['¿', 'Para', 'qué', 'hacer', 'esto', '?']
```

Nótese que la tokenización no solo separa las palabras, sino también los **signos de puntuación** (los símbolos '¿' y '?' se consideran tokens independientes). Esto es importante porque, dependiendo de la tarea, la puntuación puede aportar información relevante (por ejemplo, distinguir una pregunta de una afirmación).

---

## 3. Palabras vacías (Stopwords)

Las **stop words** son palabras muy comunes en un idioma que, por su alta frecuencia y bajo contenido semántico propio, **no aportan mucho significado** al análisis de un texto. Al eliminarlas, el análisis puede concentrarse en las **palabras clave** que realmente son relevantes para la tarea.

### Ejemplos de stopwords en español

el, la, de, en, y, por, que, etc.

Estas son palabras gramaticales (artículos, preposiciones, conjunciones) que aparecen constantemente en cualquier texto, independientemente del tema que trate, por lo que suelen filtrarse antes de un análisis estadístico o de clasificación.

### Ejemplo del documento

```
Texto:               "¿Para qué hacer esto?"
Tokens:               ['¿', 'Para', 'qué', 'hacer', 'esto', '?']
Stop Words eliminadas: ['hacer', 'esto']
```

Aquí se observa cómo, tras eliminar las stopwords (que en este caso incluyen los signos de puntuación y palabras como "¿", "Para", "qué", "?"), solo quedan las palabras consideradas más informativas: **"hacer"** y **"esto"**.

---

## 4. Lematización (Lemmatizer)

El **lematizador (lemmatizer)** de la librería **NLTK (Natural Language Toolkit)** es una herramienta que reduce las palabras a su **forma base o "lema"**.

### ¿Qué es un lema?

Un lema es la forma canónica o "de diccionario" de una palabra, por ejemplo:

- Un **verbo en infinitivo** (en vez de una forma conjugada).
- Un **sustantivo en singular** (en vez de plural).

### Características clave

- El lematizador **tiene en cuenta el contexto gramatical** de la palabra y devuelve siempre una **palabra válida** en el idioma (a diferencia de otras técnicas más simples).
- Utiliza la base de datos **WordNet** para encontrar la forma base de cada palabra, **mapeando las formas flexionadas** (conjugadas, pluralizadas, etc.) a sus respectivos lemas según su **rol gramatical** (verbo, sustantivo, adjetivo, etc.).

### Ejemplo del documento

```
Texto: "Los estudiantes están haciendo el laboratorio antes de ir a clase."

Lematizer:
['El', 'estudiante', 'estar', 'hacer', 'el',
 'laboratorio', 'antes', 'de', 'ir', 'a', 'clase']
```

Se puede observar cómo:

- "estudiantes" (plural) → "estudiante" (singular)
- "están" (conjugado) → "estar" (infinitivo)
- "haciendo" (gerundio) → "hacer" (infinitivo)

El resto de las palabras (preposiciones, artículos) permanecen prácticamente sin cambios porque ya están en su forma base.

---

## 5. Stemming (derivación de raíces)

El **stemming** es una técnica relacionada con la lematización, pero más simple: consiste en **cortar los sufijos** de las palabras para obtener una **raíz (stem)**, sin necesariamente verificar que el resultado sea una palabra válida del idioma.

### Diferencia con la lematización

El documento contrasta ambos métodos:

- **Lemmatizer (WordNet):** consulta un **corpus** (como WordNet) para encontrar la **forma canónica (lema)** de una palabra, considerando el contexto gramatical (tiempo verbal, número, género). El resultado siempre es una palabra real del idioma.
- **Stemming:** simplemente **recorta sufijos** de forma más mecánica, sin garantizar que el resultado sea una palabra gramaticalmente válida.

### Ejemplo del documento

```
Texto: "Los estudiantes están haciendo el laboratorio antes de ir a clase."

Tokens:
['Los', 'estudiantes', 'están', 'haciendo', 'el',
 'laboratorio', 'antes', 'de', 'ir', 'a', 'clase']

Stemming:
['Los', 'estudiant', 'estan', 'hac', 'el',
 'laborator', 'ant', 'de', 'ir', 'a', 'clas']
```

Aquí se ve claramente la diferencia con la lematización: "estudiantes" se convierte en **"estudiant"** (una raíz truncada, no una palabra completa), "haciendo" se convierte en **"hac"**, y "laboratorio" se convierte en **"laborator"**. Estas no son palabras válidas por sí mismas, sino raíces comunes que agrupan distintas variantes de una misma palabra (por ejemplo, "estudiant" agruparía "estudiante", "estudiantes", "estudiantil", etc.).

**En resumen:** el stemming es más rápido y simple pero menos preciso; la lematización es más costosa computacionalmente pero produce resultados lingüísticamente correctos.

---

## 6. Embeddings y representaciones vectoriales

Una vez tokenizado y normalizado el texto, el siguiente gran desafío es **representar las palabras de forma numérica**, ya que los algoritmos de aprendizaje automático solo trabajan con números.

### Concepto de embedding

- Las palabras se representan como **vectores en un espacio de características de dimensión m**.
- Cada palabra deja de ser un símbolo único (como una cadena de texto) y pasa a ser un **conjunto de valores numéricos**.
- Los **embeddings** son representaciones **densas y de baja dimensión** de palabras (u otros elementos), en contraste con representaciones dispersas de alta dimensión como el one-hot encoding.

### Propiedad semántica clave

Los embeddings **capturan información semántica**: palabras con **significados similares** quedan representadas por vectores que están **más cerca entre sí** en el espacio vectorial. Esto permite, por ejemplo, que operaciones vectoriales entre embeddings reflejen relaciones semánticas entre palabras.

### ¿Cómo se obtienen?

Los embeddings se **aprenden automáticamente** durante el entrenamiento de modelos de aprendizaje profundo. Dos técnicas clásicas mencionadas en el documento son:

- **Word2Vec** (Mikolov, Chen, Corrado y Dean, 2013)
- **GloVe** (Pennington, Socher y Manning, 2014)

### Comparación visual: one-hot vs. embeddings

El documento incluye una figura que compara dos formas de representar una secuencia de 20 palabras (correspondientes a un documento):

- **Panel superior (One-hot):** cada palabra se codifica usando un diccionario de **16 palabras**. En la codificación one-hot, cada palabra se representa como un vector binario donde solo una posición tiene el valor 1 (marcada en negro) y el resto son 0 (marcadas en gris) — es decir, un vector disperso (sparse) y de alta dimensión, del tamaño del vocabulario completo.
- **Panel inferior (Embed):** las mismas palabras se representan en un **espacio m-dimensional con m = 5**, es decir, cada palabra pasa a estar representada por solo 5 valores numéricos (mostrados como celdas de colores), en vez de 16 valores binarios.

Un punto importante que aclara el texto: a diferencia de la codificación one-hot (que es binaria, solo 0 y 1), **los vectores de embeddings no son binarios**, sino que tienen **valores continuos**, y se obtienen generalmente mediante técnicas de aprendizaje como Word2Vec o GloVe, entrenadas sobre grandes cantidades de texto.

Esta comparación ilustra la principal ventaja de los embeddings frente al one-hot encoding: **reducción drástica de la dimensionalidad** (de 16 a 5 en este ejemplo, pero en la práctica de decenas de miles de palabras del vocabulario a unos pocos cientos de dimensiones) junto con la **captura de relaciones semánticas** entre palabras, algo que el one-hot encoding no puede representar (en one-hot, todas las palabras están igual de "lejos" unas de otras).

---

## 7. N-gramas

Un **n-grama** es una **secuencia de n elementos consecutivos** extraídos de un texto o discurso. Estos elementos pueden ser:

- Palabras
- Caracteres
- Cualquier otro tipo de unidad textual

### Uso principal

Los n-gramas se utilizan para **modelar la probabilidad de ocurrencia de una palabra** basándose en las palabras que la preceden. Esto es la base de los llamados **modelos de lenguaje de n-gramas**, que estiman qué tan probable es que una palabra aparezca dado un contexto de n-1 palabras anteriores.

### Ejemplo del documento: bigramas (n = 2)

```
Texto: "Los estudiantes están realizando experimentos en el laboratorio."

Bigramas (n=2):
['Los estudiantes', 'estudiantes están', 'están realizando',
 'realizando experimentos', 'experimentos en', 'en el',
 'el laboratorio']
```

Cada bigrama se forma tomando **pares consecutivos** de palabras del texto, deslizando una "ventana" de tamaño 2 a lo largo de toda la oración. De forma similar, se podrían generar **trigramas (n=3)**, tomando grupos de tres palabras consecutivas, y así sucesivamente para cualquier valor de n.

Los n-gramas son útiles tanto para tareas estadísticas simples (por ejemplo, contar frecuencias de combinaciones de palabras) como para alimentar modelos de lenguaje más complejos que predicen la siguiente palabra en una secuencia.

---

## Resumen general del documento

Esta presentación describe, paso a paso, el **pipeline típico de preprocesamiento de texto en NLP**, desde el texto crudo hasta una representación numérica utilizable por algoritmos de aprendizaje automático:

1. **Tokenización:** dividir el texto en unidades mínimas (tokens).
2. **Eliminación de stopwords:** filtrar palabras muy frecuentes y poco informativas.
3. **Lematización:** reducir las palabras a su forma base válida (lema), considerando el contexto gramatical mediante WordNet.
4. **Stemming:** alternativa más simple y rápida que la lematización, que recorta sufijos para obtener raíces (no necesariamente palabras válidas).
5. **Embeddings:** representar las palabras como vectores numéricos densos y de baja dimensión, capaces de capturar relaciones semánticas entre palabras, en contraste con la codificación dispersa one-hot.
6. **N-gramas:** capturar el contexto secuencial del texto mediante combinaciones consecutivas de n elementos (por ejemplo, bigramas), útiles para modelar la probabilidad de aparición de palabras.

En conjunto, estos pasos constituyen los fundamentos clásicos del preprocesamiento de texto que preceden a tareas más avanzadas de NLP, como la clasificación de texto, el análisis de sentimientos o la traducción automática, mencionadas al inicio del documento.