#  ACCIDENTES DE AUTOMÓVIL EN NYC


Proyecto para la visualización de la por medio de mapas de la distribución de los accidentes
ocurridos en la ciudad de NYC por medio de Streamlit.

La información del Dataset puede ser encontrada en [NYC Open Data]( https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95), siendo información de uso publico.

![Alt Text](https://media.giphy.com/media/f5MUYjxSet5jwkid95/giphy.gif)

##  Nota

Las dependencias, librerías necesarias para poder utilizar el proyecto se encuentran en `requirements.txt`, para poder instalarlas utilizar el siguiente comando:
```

pip install -r requirements.txt

```
Para correr el servidor utilizar el siguiente comando:

```

streamlit run app.py

```
Debido al tamaño del Dataset este puede ser descargado [aquí]( https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD). Este deberá agregarse a la siguiente carpeta:

```

./Data/Motor_Vehicle_Collisions_-_Crashes.csv

```