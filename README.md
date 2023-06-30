# Tweet-RSS
Script elaborado para la Oficina de Relaciones Internacionales (ORI) de la UDC. Obtiene las noticias publicadas en el RSS de la ORI y las publica en twitter de forma automática. Esta diseñado para estar continuamente en ejecución y comprobar la existencia de nuevas noticias cada 5 minutos.
## Dependencias
- feedpasrser
- pendulum
- request_oauthlib
Las dependencias estan contenidas en el fichero ```dependencies.txt```. Puedes instalarlas con ```pip``` ejecutando:
```shell
python3 -m pip install -r dependencies.txt
```
Se requiere también una [cuenta de desarrollador de twitter](https://developer.twitter.com/) para obtener las ```consumer_key``` y ```consumer_secret``` necesarias para las peticiones a la API. una vez obtenidas, se crea en el directorio raíz del prouyecto un fichero ```secret.json``` con el siguiente contenido:
```json
{
{
    "consumer_key": "Your key",
    "consumer_secret": "Your secret"
}
```
Por último, basta con ejecutar:
```shell
python3 rss_ori.py
```
