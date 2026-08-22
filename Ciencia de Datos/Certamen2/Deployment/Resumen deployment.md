## 1. ¿Qué es el Deployment y dónde encaja?

El deployment (despliegue) es el proceso de tomar un modelo entrenado y ponerlo a funcionar en el mundo real para que reciba datos nuevos y entregue predicciones útiles, rápidas y confiables. Un modelo que solo vive en un notebook de Jupyter no genera valor real.

- **No es el final, es un ciclo:** Metodologías como CRISP-DM demuestran que el despliegue es una fuente de retroalimentación. Una vez en producción, el modelo genera nueva información que sirve para evaluar si el negocio cambió o si el modelo quedó desactualizado, reiniciando el ciclo.
    
- **La analogía larval de Hinton:** Geoffrey Hinton explica que **el modelo que se entrena no tiene por qué ser el mismo que se despliega**.
    
    - _Fase de entrenamiento ("larval"):_ El objetivo es extraer conocimiento; se usan arquitecturas enormes y lentas sin importar el consumo energético.
        
    - _Fase de producción ("adulta"):_ El objetivo es que sea rápido, liviano, eficiente y que quepa en el hardware disponible. Para resolver esta tensión se usan técnicas como la **destilación de conocimiento** (un modelo pequeño imita a uno grande), **cuantización** (reducir la precisión numérica de los pesos) y **poda** (eliminar conexiones redundantes).
        

## 2. Paradigmas de Despliegue: Edge vs. Cloud

La decisión de dónde vivirá el modelo define la arquitectura del proyecto:

|**Criterio**|**Despliegue en el Dispositivo (Edge / Embedded)**|**Despliegue en la Nube (Cloud)**|
|---|---|---|
|**Ubicación**|Hardware local (Raspberry Pi, Arduino, Nvidia Jetson).|Servidores remotos (AWS, GCP, Azure).|
|**Ventajas**|Tiempo real, bajo consumo de energía y **no necesita conectividad** a internet.|Alta escalabilidad (millones de usuarios) y alto poder computacional (modelos grandes sin comprimir).|
|**Desventajas**|Recursos muy limitados (poca memoria y poder de cómputo).|**Requiere conexión estable a internet**, costos de infraestructura y latencia de red.|

## 3. Hardware para Inferencia y la importancia de CUDA

La inferencia es la fase en la que el modelo genera predicciones en producción. El hardware se elige según el rendimiento, las limitaciones del entorno y el costo:

- **CPU vs. GPU:** La CPU está optimizada para latencia baja en tareas secuenciales complejas (pocos núcleos pero potentes). La GPU está optimizada para **alto throughput** (rendimiento masivo) mediante el modelo **SIMT** (_Single Instruction, Multiple Threads_), ideal para el cómputo paralelo que exige la multiplicación de matrices en redes neuronales.
    
- **El rol de CUDA:** Es la plataforma de NVIDIA que permite usar la GPU como un coprocesador de propósito general y no solo para gráficos. **No se limita al Deep Learning:** CUDA también acelera algoritmos de ML clásico (como KNN, K-Means y Random Forest) al paralelizar operaciones vectoriales como el cálculo de distancias o la creación de histogramas.
    
- **GPU Discreta vs. Integrada:** Las discretas tienen memoria dedicada exclusiva (GDDR6) y se conectan por PCIe. Las integradas —comunes en los **System-on-Chip (SoC)** como la familia Nvidia Jetson— **comparten la memoria RAM con la CPU**, lo que evita tener que copiar datos entre bancos de memoria, ahorrando espacio físico y energía.
    

## 4. Cadenas de Herramientas (Toolchains)

Para llevar un modelo desde frameworks como PyTorch o TensorFlow hasta el hardware final, se requiere un flujo de transformación:

1. **Formato Intermedio (ONNX):** Actúa como un "idioma universal" para evitar tener que escribir un conversor para cada combinación de framework y hardware.
    
2. **Optimizadores de Inferencia:** Herramientas específicas de hardware que reducen la complejidad, cuantizan y compilan el modelo (ej. _TensorRT_ para NVIDIA o _Vitis AI_ para Xilinx).
    

## 5. El Extremo del Edge: TinyML y Microcontroladores

Cuando se despliega en el escenario con mayores restricciones de recursos, se pasa de los microprocesadores a los **microcontroladores** (sistemas integrados completos en un solo chip, como el ATmega328p de Arduino).

- **Diferencia de Órdenes de Magnitud:** Un microcontrolador opera en megahertz (1-400 MHz) en lugar de gigahertz, su memoria se mide en **kilobytes** (2-512 KB) y su consumo de potencia es hasta un millón de veces menor (microwatts a milliwatts), haciéndolos ideales para dispositivos a batería.
    
- **TinyML:** Paradigma centrado en implementar modelos de deep learning o ML en estos entornos tan limitados. El pipeline exige obligatoriamente entrenamiento en PC, destilación/cuantización, conversión a formatos como _TensorFlow Lite_ e inferencia local.
    
- **Árboles de Decisión en TinyML:** Son ideales para microcontroladores porque no requieren operaciones matriciales complejas; son solo **secuencias de comparaciones condicionales (`if-else`)**. Herramientas como `micromlgen` permiten traducir automáticamente modelos de scikit-learn (incluyendo Random Forests completos) directamente a código C++ ejecutable en Arduino.