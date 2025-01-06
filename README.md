# moto-price-predictor
A price predictor for suzuki motorcycles in Colombia, with an api called through google cloud run

## Resumen
Es un predictor que toma precios y modelos de motos de la página de suzuki motos colombia,para compararlos con una base de datos de motocicletas  que da información completa sobre cada moto. Del proceso se extraen todas las motos que actualmente están en Colombia, dando datos y agregando el precio de las mismas.

Tomando los datos relevantes, se utiliza un modelo de regresión lineal para hacer las predicciones para posteriormente usarlo en una api de flask y subirlo al servicio de google: cloud run

## Descripción detallada
- Primero se realiza el ```scrape.py``` que, usando la librería de beautifulSoup,toma la información de relevancia, precio y modelo, y limpia la información, removiendo nombres que solo se le aplican a Colombia y las referencias que en lugar de precio, tienen un agotado. Se relacionan los modelos existentes en Colombia con la base de datos, dejando un json que tiene las especificaciones completas de las motos en Colombia.

- Ahora ```cleaning.py``` limpia los modelos del json que tienen más de una referencia de la misma moto y deja un json filtrado.

- Con el archivo ```prediction.py``` se toma el json para convertirlo en un dataframe de pandas, con el que se filtran las variables importantes para el modelo predictivo, además de separar las variables en categoricas y numéricas. Una vez realizado el proceso de la regresión lineal, se guarda en un archivo .pkl.

- El archivo .pkl se utiliza para el endpoint en ```app.py``` donde se utiliza flask

- Teniendo la lógica del modelo, se procede a contenerizar con docker, estableciendo un dockerfile donde se exponga el puerto necesario

- Para subir a cloud run, primero se tiene que poner la imagen de docker en el Artifact Registry, para despues llamarlo en cloud run con

- Ya se puede llamar el endpoint que deja cloud run

- Para cerrar la instancia de cloud run 
 
