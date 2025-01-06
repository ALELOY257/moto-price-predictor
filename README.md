# moto-price-predictor
A price predictor for suzuki motorcycles in Colombia, with an api called through google cloud run

## Resumen
Es un predictor que toma precios y modelos de motos de la página de suzuki motos colombia,para compararlos con una base de datos de motocicletas  que da información completa sobre cada moto. Del proceso se extraen todas las motos que actualmente están en Colombia, dando datos y agregando el precio de las mismas.

Tomando los datos relevantes, se utiliza un modelo de regresión lineal para hacer las predicciones para posteriormente usarlo en una api de flask y subirlo al servicio de google: cloud run

## Descripción detallada
Primero se realiza el ```scrape.py``` que, usando la librería de beautifulSoup,toma la información de relevancia, precio y modelo, y limpia la información, removiendo nombres que solo se le aplican a Colombia y las referencias que en lugar de precio, tienen un agotado
 
