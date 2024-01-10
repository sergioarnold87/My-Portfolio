# Datathon - Predicción de Entregas

## Descripción del Proyecto

Este proyecto forma parte del Datathon de Henry y tiene como objetivo principal predecir si un envío llegará a tiempo o no, utilizando información relevante proporcionada en el conjunto de datos.

## Archivos

- `E-Commerce_train.xlsx`: Conjunto de entrenamiento con 8998 observaciones y 12 dimensiones, incluyendo información sobre si el envío llegó a tiempo o no.
- `E-Commerce_test.xlsx`: Conjunto de prueba con 2000 observaciones y 11 dimensiones, sin información sobre la puntualidad del envío.

## Dimensiones del Conjunto de Datos

1. **ID:** Identificador del registro de orden (valor entero).
2. **Warehouse_block:** Almacén de distribución de donde salió la orden (A a F).
3. **Mode_of_Shipment:** Medio de transporte (Flight, Road, Ship).
4. **Customer_care_calls:** Número de llamadas a atención al cliente por esa orden (valores enteros del 2 al 7).
5. **Customer_rating:** Puntaje del cliente (valores enteros 1 al 5).
6. **Cost_of_the_Product:** Costo del producto (valor numérico entero de 96 a 310).
7. **Prior_purchases:** Número de compras previas realizadas por el cliente (valor numérico entero de 2 a 10).
8. **Product_importance:** Nivel de importancia del producto (low, medium, high).
9. **Gender:** Género del comprador (F, M).
10. **Discount_offered:** Porcentaje de descuento ofrecido por esa compra (valor numérico entero de 1 a 65).
11. **Weight_in_gms:** Peso del paquete de la orden, en gramos (valor numérico entero de 1001 a 7846).
12. **Reached.on.Time_Y.N:** Información sobre la llegada del paquete a destino (1 si llegó a tiempo, 0 si no llegó a tiempo).

## Objetivo

Implementar un modelo que pueda predecir si un envío llegará a tiempo o no, utilizando la métrica de Exhaustividad (Recall) de la matriz de confusión.

## Métrica

La métrica de evaluación del desempeño del modelo es la Exhaustividad (Recall), calculada mediante la fórmula:

$$ Recall=\frac{TP}{TP+FN}$$

siendo $TP$ los verdaderos positivos y $FN$ los falsos negativos.

## Entrega

El código fuente debe estar en un archivo `.py` o un Jupyter Notebook `.ipynb`. Además, se debe generar un archivo `.csv` con las predicciones, utilizando una columna llamada 'pred'.

## Instrucciones

1. Explorar el conjunto de datos.
2. Realizar un análisis EDA (Exploratory Data Analysis).
3. Aplicar feature engineering según sea necesario.
4. Implementar un modelo que se ajuste al problema.
5. Generar un archivo .csv con las predicciones.

## Modelos de Aprendizaje Automático Utilizados

En el desarrollo de este proyecto, se exploraron varios modelos de aprendizaje automático para abordar el problema de predicción de entregas. A continuación, se enumeran los modelos utilizados:

1. **Árbol de Decisión (Decision Tree):** Se implementó un árbol de decisión utilizando la biblioteca scikit-learn. Se exploraron diferentes configuraciones de hiperparámetros para optimizar el rendimiento del modelo.

2. **Regresión Logística (Logistic Regression):** Se aplicó la regresión logística para comprender la relación entre las variables de entrada y la variable de salida binaria.

3. **Red Neuronal (Neural Network):** Se construyó una red neuronal utilizando la biblioteca Keras. La red consta de capas de entrada, capas ocultas y una capa de salida con activación sigmoide.

Cada modelo fue evaluado utilizando la métrica de Exhaustividad (Recall) de la matriz de confusión, como se especifica en las instrucciones del Datathon.


## Conclusiones

Aprovechar esta instancia de aprendizaje para experimentar y divertirse.

