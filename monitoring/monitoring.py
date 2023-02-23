import threading
import requests
import logging
from datetime import datetime

disponible = True
cambioRegistro = True
tiempoInicial = None
logging.basicConfig(filename='health_check.log', encoding='utf-8', level=logging.INFO)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def func():
    global cambioRegistro
    global tiempoInicial
    try:
        health_check = requests.get(url = "http://orden:5005/health-check")
        mensaje = health_check.status_code
        if mensaje == 200: disponible=True
        else: disponible=False
    except:
        mensaje = "'Servicio no disponible'"
        disponible=False
    
    if disponible == False:
        if cambioRegistro == True:
            cambioRegistro = False
            now = datetime.now()
            logging.info('{}. El servicio comenzó a no estar disponible'.format(now)) 
            tiempoInicial = now
        else:
            logging.info('{}. El servicio sigue sin estar disponible'.format(datetime.now())) 
    else:
        if cambioRegistro == False:
            cambioRegistro = True
            now = datetime.now()
            diferencia = now - tiempoInicial
            logging.info('{}. El servicio se restableció despues de {} segundos'.format(now, diferencia.seconds))

    print("{}. Respuesta {}".format(datetime.now(), mensaje), flush=True)
    


    
set_interval(func, 2)