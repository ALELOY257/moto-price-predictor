# moto-price-predictor
A price predictor for suzuki motorcycles in Colombia, with an api called through google cloud run
## Changes that need to be applied
When I made this, I wasnt aware of some methods to have a better performing model, this is the checklist of the implementation of those changes
- [ ] Recreate the model with Jupyter notebooks for simplicity when making summaries of the model
- [ ] Take out the features with an elevated p-value
- [ ] Check the variations of R2 value
- [ ] Try a Lasso regression to compare to the base model


## Resumen
Es un predictor que toma precios y modelos de motos de la página de suzuki motos colombia,para compararlos con una base de datos de motocicletas  que da información completa sobre cada moto. Del proceso se extraen todas las motos que actualmente están en Colombia, dando datos y agregando el precio de las mismas.

Tomando los datos relevantes, se utiliza un modelo de regresión lineal para hacer las predicciones para posteriormente usarlo en una api de flask y subirlo al servicio de google: cloud run

## Descripción detallada
- Primero se realiza el ```scrape.py``` que, usando la librería de beautifulSoup,toma la información de relevancia, precio y modelo, y limpia la información, removiendo nombres que solo se le aplican a Colombia y las referencias que en lugar de precio, tienen un agotado. Se relacionan los modelos existentes en Colombia con la base de datos, dejando un json que tiene las especificaciones completas de las motos en Colombia.

- Ahora ```cleaning.py``` limpia los modelos del json que tienen más de una referencia de la misma moto y deja un json filtrado.

- Con el archivo ```prediction.py``` se toma el json para convertirlo en un dataframe de pandas, con el que se filtran las variables importantes para el modelo predictivo, además de separar las variables en categoricas y numéricas. Una vez realizado el proceso de la regresión lineal, se guarda en un archivo .pkl.

- El archivo .pkl se utiliza para el endpoint en ```app.py``` donde se utiliza flask

- Teniendo la lógica del modelo, se procede a contenerizar con docker, estableciendo un dockerfile donde se exponga el puerto necesario

- Para subir a cloud run, primero se tiene que poner la imagen de docker en el Artifact Registry ```docker tag suzuki-motos-api northamerica-south1-docker.pkg.dev/fiery-catwalk-447000-h7/motoapi-repo/suzuki-motos-api ```
  ```docker push northamerica-south1-docker.pkg.dev/fiery-catwalk-447000-h7/motoapi-repo/suzuki-motos-api```, para despues llamarlo en cloud run con
  ```gcloud run deploy suzuki-motos-api 
>> --image=northamerica-south1-docker.pkg.dev/fiery-catwalk-447000-h7/motoapi-repo/suzuki-motos-api \
>> --platform=managed \
>> --region=us-east1 \
>> --allow-unauthenticated```
- Ya se puede llamar el endpoint que deja cloud run

- Para cerrar la instancia de cloud run
  ``` gcloud run services delete suzuki-motos-api \
>> --platform=managed \
>> --region=us-east1 \
>> --quiet ```

- Para hacer el proceso automatizado, se debe crear una función en python para la lógica de deploy y stop para la instancia de cloud run con
  ```gcloud functions deploy my-function \
>>     --runtime python39 \
>>     --trigger-http \
>>     --allow-unauthenticated \
>>     --source . \
>>     --entry-point deploy_stop ```
Para esto se debe crear una carpeta con el archivo main.py y requirements.txt, con esto, se reserva el url de la funcion
- Se establece un scheduler de gcloud para automatizar el deploy de la api
  ```gcloud scheduler jobs create http 20-minutes-job `
>> --schedule="*/20 * * * *" `
>> --uri="https://us-central1-fiery-catwalk-447000-h7.cloudfunctions.net/my-function" `
>> --http-method=GET `
>> --location us-central1```
