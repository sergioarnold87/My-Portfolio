
![Logo](https://stonkstutors.com/wp-content/uploads/2022/07/Soy-Henry-Entiende-como-funciona-la-plataforma-y-si-vale-la-pena.jpg)


## Autor

- [@SergioArnold87](https://github.com/sergioarnold87)


# Proyecto Individual 1- Data 04- Soy Henry

### Acerca del proyecto

En este primer proyecto realizamos un proceso ETL a partir de un conjunto de datos que vienen de diversas fuentes.

### Tabla de Contenido
- [PI01nery.db y CSVs limpios](https://drive.google.com/drive/folders/1ubkZiZ8km2HHCHyt8AKTNG99R0pDz2DN?usp=share_link)
- Archivo .txt con el link del drive donde están los datasets limpios y la base de datos PI01henry.db
- Notebook de python DataEngineering.ipynb
- Notebook de python D_E_data_wrangling.ipynb
- Diagrama de flujo de trabajo.jpg
- Base de datos SQLite PI01henry.db

### Tecnologías utilizadas

- SQLite3
- Python (.ipynb)
- Pandas

### Tablas de la base de datos
- Sucursal 
- Producto
- Precio

#### Por que SQLITE?
- Proporciona una base de datos local para almacenar datos.
- Configuración cero.
- Organice, limpie y transforme datos para análisis.
- Cree un almacén de datos local de manera sencilla.
- El código y los datos se pueden compartir con cualquier persona.

#### Por que Pandas?
- Mejor opciones para trabajar con datos tabulares en Python.
- Provee estructuras de datos.
- Facil de usar.

## Plan de Ataque

1 Transformar y limpiar todos los datasets, para luego unificar la extensión.

2 Crear una conexión a SQLite3, que viene integrada a python.

3 Crear el cursor para ejecutar Sentencias SQL en nuestro Notebook.

4 Crear las Tablas.

5 Ingestar los Dataframes a las tablas existentes en SQLite a traves del modulo pd.read_sql_query de Pandas.







