# -*- coding: utf-8 -*-
"""TalentPitch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dcwB0kmBpNR70FyNe6oW4g2_K9eRCOQE

## **Prueba de Talent Pitch Data Analyst - Jorge Gomez**

# Carga y Limpieza de datos

Lo primero respecto a la prueba es hacer la carga de datos para poder hacer posteriormente el análisis. Lo primero es instalar los paquetes de la librería Missingno que no se encuentren instalados, esta librería es para hacer una visualización de los datos faltantes. Para ello se usa el siguiente código:
"""

!pip install missingno

"""Posteriormente se importan los datos almacenados en el repositorio, que en este caso son las CSV suministradas. Para ellos primero se clona el repositorio y se accede a la carpeta donde están los archivos."""

# Commented out IPython magic to ensure Python compatibility.
# Clone the entire repo.
!git clone -l -s https://github.com/JoRgEXx1899/TalentPitchDataAnalysis.git cloned-repo
# %cd cloned-repo
!ls

"""Se hace la importación de las librerías que se van a usar, como missingno, pandas, numpym scipy y seaborn."""

import missingno as ms
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import seaborn as sb

"""Se importan los archivos .csv y se verifica cib la librería missingno cual es el estado de los datos y si hay algún dato vacío o nulo."""

# Lectura de datos en Python
usuarios=pd.read_csv('users.csv')
usuarios_raw=pd.read_csv('users_raw.csv')
ms.matrix(usuarios_raw)
usuarios_raw.info()
ms.matrix(usuarios)
usuarios.info()
#usuarios.info()
#ms.bar(usuarios)

"""Se observa mediante las anteriores gráficasque el conunto de datos necesita hacer una limpieza y completar datos que faltan, en las columnas que son cualitativas como ultimo nivel de estudio se rellena con un texto que sea acorde a las opciones, se escogió "Other" como relleno para los datos faltantes, y  para los campos que son de tipo númerico se observa que son estadísticas de uso por lo que se rellenaron los vaciós con "0"."""

usuarios['level_last_study'] = usuarios['level_last_study'].fillna('other')
usuarios['received_messages'] = usuarios['received_messages'].fillna(0)
usuarios['sent_messages'] = usuarios['sent_messages'].fillna(0)
usuarios['num_resumes_created'] = usuarios['num_resumes_created'].fillna(0)
usuarios['events_scheduled'] = usuarios['events_scheduled'].fillna(0)
usuarios['views_to_resume_received'] = usuarios['views_to_resume_received'].fillna(0)
usuarios['views_to_profile_received'] = usuarios['views_to_profile_received'].fillna(0)
usuarios['saved_from_playlist'] = usuarios['saved_from_playlist'].fillna(0)
usuarios['reactions_received'] = usuarios['reactions_received'].fillna(0)
usuarios['average_feedback'] = usuarios['average_feedback'].fillna(0)
usuarios['selector_appearances'] = usuarios['selector_appearances'].fillna(0)
usuarios['reactiones_made'] = usuarios['reactiones_made'].fillna(0)
usuarios['match_with_playlists'] = usuarios['match_with_playlists'].fillna(0)
usuarios['contents_viewed'] = usuarios['contents_viewed'].fillna(0)
usuarios['connections_sent'] = usuarios['connections_sent'].fillna(0)

"""Se observa la matriz nuevamente para verificar el estado de los datos y se puede ver que ya no hay datos faltantes en el archivo de "users"."""

ms.matrix(usuarios)
usuarios.info()

"""Se hace el mismo proceso de completado de datos faltantes con la tabla de usuarios_raw, pero en este se hace el llenado de forma distinta. Las fechas de cumpleaños faltantes se tomó "01/01/2000" para rellenarlas y la fecha de creación faltante se tomó el "01/01/2023". Para los campos de género ciudad y estado se rellenaron con NE, siglas de "No especificado"."""

usuarios_raw['birthdate'] = usuarios_raw['birthdate'].fillna('01/01/2000')
usuarios_raw['created_at'] = usuarios_raw['created_at'].fillna('01/01/2023')
usuarios_raw['gender'] = usuarios_raw['gender'].fillna('NE')
usuarios_raw['city'] = usuarios_raw['city'].fillna('NE')
usuarios_raw['state'] = usuarios_raw['state'].fillna('NE')

"""Se observa dentro de los datos que hay inconsistencias en la tabla usuarios_raw, en las columnas ciudad y género debido a que en ciudad se encuentran algunas fechas, y en género algunos con un "0". Se busca reemplazar estos datos de tipo fecha en los formatos "dd/mm/yyyy" y "yyyy-mm-dd" por "NE", y en el género también se decide proceder igual con cualquier dato numérico cambiandolo por "NE"."""

import re
usuarios_raw['city'] = usuarios_raw['city'].apply(lambda x: re.sub(r'\d{1,2}/\d{1,2}/\d{4}', 'NE', str(x)))
usuarios_raw['city'] = usuarios_raw['city'].apply(lambda x: re.sub(r'\d{4}-\d{1,2}-\d{1,2}', 'NE', str(x)))
usuarios_raw['gender'] = usuarios_raw['gender'].apply(lambda x: re.sub('\d+', 'NE', str(x)))
print(usuarios_raw['city'])

"""Se visualiza de nuevo la tabla de usuarios_raw con el Missingno para verificar si queda información faltante o nula y se observa que ya se encuentra completa la información en cada una de las columnas."""

ms.matrix(usuarios_raw)
usuarios_raw.info()

"""Se procede a hacer el JOIN de ambas tablas, usuarios y usuarios_raw, para tener datos para el modelo más completos y procedentes de ambas tablas. Para ellos se usa la columna "user_id" de la tabla usuarios y la columna "id" de la tabla usuarios_raw y se juntan por medio de el merge de pandas. Y se guardan ambas tablas en un nuevo archivo CSV haciendo un commit a GitHub."""

tabla_unida = pd.merge(usuarios, usuarios_raw, left_on='user_id',right_on='id')
tabla_unida.to_csv('datosLimpios.csv', index=False)
!ls

!git config user.email "daniel990918@gmail.com"
!git config user.name "JoRgEXx1899"
!git add datoslimpios.csv
!git commit -m "Cambios y limpieza de datos. Listos para Analizar"
!git remote add origin https://"JoRgEXx1899":"jdgv1899"@github.com/JoRgEXx1899/TalentPitchDataAnalysis.git
!git push -u origin main

tabla_unida['created_at'] = pd.to_datetime(tabla_unida['created_at'] )

"""# Visualización y Análisis

Se crea la tabla de Finalización de perfil a lo largo del tiempo usando como índice la fecha de creación y listándolo resumido el promedio por mes y año.
"""

tabla_Finalización_Perfil_en_el_Tiempo = tabla_unida.groupby([tabla_unida['created_at'].dt.year, tabla_unida['created_at'].dt.month])['profile_completed'].mean()
#tabla_Finalización_Perfil_en_el_Tiempo = tabla_Finalización_Perfil_en_el_Tiempo.reset_index()
tabla_Finalización_Perfil_en_el_Tiempo.columns = ['year', 'month', 'valor']
print(tabla_Finalización_Perfil_en_el_Tiempo)

"""Y se observa que en el trascurso de 2023 el primedio de completado de perfil es de menos del 65%.

Se crea la tabla de Visualizaciones al resumen por ciudad usando como índice la ciudad y listándolo resumido el promedio de visualización por ciudad.
"""

tabla_Vistas_por_ciudad = tabla_unida.groupby('city')['views_to_resume_received'].mean()
tabla_Vistas_por_ciudad.columns = ['Ciudad', 'Vistas_promedio_resumen']
print(tabla_Vistas_por_ciudad)

"""Se crea la tabla de Visualizaciones al perfil por estado laboral actual usando como índice "desired_state" y listándolo resumido el promedio de finalización del perfil por cada uno de los estados laborales."""

tabla_Finalización_Perfil_por_estado_de_perfil = tabla_unida.groupby('desired_state')['profile_completed'].mean()
tabla_Finalización_Perfil_por_estado_de_perfil.columns = ['Situacion laboral', 'Tasa de Completado del perfil']
print(tabla_Finalización_Perfil_por_estado_de_perfil)

"""Se crea la tabla de creaciones de resumenes por estado laboral actual usando como índice "desired_state" y listándolo resumido la suma de creaciones de resúmenes por cada uno de los estados laborales."""

tabla_estado_laboral_vs_creaciones = tabla_unida.groupby('desired_state')['num_resumes_created'].sum()
tabla_estado_laboral_vs_creaciones.columns = ['Situacion laboral', 'Resumenes creados']
print(tabla_estado_laboral_vs_creaciones)

"""Creamos la visualización de Gráfico de línea de perfil_completadoa lo largo del tiempo (por mes y año) usando plot de matplotlib.pyplot.

"""

datos_nuevos = pd.DataFrame({'fecha':tabla_Finalización_Perfil_en_el_Tiempo['year'], 'valor': tabla_Finalización_Perfil_en_el_Tiempo['valor']})

plt.plot(datos_nuevos['fecha'], datos_nuevos['valor'])
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.title('Finalización del perfil a lo largo del tiempo')
plt.show()