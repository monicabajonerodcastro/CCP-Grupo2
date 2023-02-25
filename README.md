# CCP-Grupo2

## Instalación y ejecución

### Requerimientos 
- Docker
- Docker compose

### Iniciar docker
Ejecutar el la raiz del proyecto
```sh
docker-compose up -d --build
```

## API Gateway - Endpoints

http://localhost:8080/plan-ruta?fecha=&cliente=

http://localhost:8080/ordenes

## Ejecuciónes

# ASR-13

1. Se debe detener el servicio de ordenes con su respectivo consumidor de mensajes con el siguiente comando:
```sh
docker-compose stop orden & docker-compose stop consumidor-orden wait
```
2. Se deben enviar las peticiones a la URL http://localhost:8080/plan-ruta?fecha=&cliente= (la fecha y el cliente no son obligatorios pero los tag si).
3. Si se ingresa a la terminal del servicio de monitoreo en Doker, se debe visualizar el mensaje "Connection NOT established".
4. Si se ingresa a la UI de RabbitMQ (http://localhost:15672/#/queues con usuario y contraseña guest) se debe ver en la gráfica de la cola que las peticiones se encuentran encoladas.

# ASR-14
1. Se deben tener todos los servicios corriendo.
2. Se deben enviar las peticiones a la URL http://localhost:8080/plan-ruta?fecha=&cliente= (la fecha y el cliente no son obligatorios pero los tag si).
3. Al ingresar al componente de votación en Docker, se deben ver los mensajes con las respuestas de los 3 servicios de plan de ruta.
4. Si los 3 servicios coninciden en la validación (es decir, que los 3 servicios están de acuerdo que la validación fue exitosa o que la validación no cumple con la calidad e la petición), el servicio de votación respondera:
```sh
{
    "message": "La respuesta de los servicios son iguales",
    "status": true
}
```
5. Si la respuesta no pasa los controles de calidad en al menos un servicio, el servicio de votación respondera:
```sh
{
    "message": "Al menos una respuesta es diferente",
    "status": false
}
```

## License

MIT
