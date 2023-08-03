import json


def cargar_configuracion():
    with open("ConfigurationFolder/config.json") as archivo:
        configuracion = json.load(archivo)
    return configuracion

class config_database:
    configuracion = cargar_configuracion()

    USER = configuracion["username"]
    PASSWORD = configuracion["password"]
    DATA_BASE_NAME = configuracion["database"]
    HOST = configuracion["host"]
    PORT = configuracion["port"]



