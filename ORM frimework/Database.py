import psycopg2

class Database:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """
        Inicializa una nueva instancia de la clase Database.

        Parámetros:
        dbname (str): Nombre de la base de datos.
        user (str): Nombre de usuario para acceder a la base de datos.
        password (str): Contraseña del usuario para acceder a la base de datos.
        host (str, opcional): Dirección del host de la base de datos. Por defecto, se asume "localhost".
        port (int, opcional): Puerto de la base de datos. Por defecto, se utiliza el puerto 5432.

        Retorna:
        Database: Una nueva instancia de la clase Database.
        """
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._connection = None

    def connect(self):
        """
        Establece una conexión a la base de datos utilizando psycopg2.

        Retorna:
        None
        """
        try:
            self._connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
            self._connection.autocommit = True
            print("Conectado a la base de datos")
        except psycopg2.OperationalError as e:
            print("Error en la conexión de la base de datos:", str(e))

    def disconnect(self):
        """
        Cierra la conexión actual a la base de datos, si está abierta.

        Retorna:
        None
        """
        if self._connection:
            self._connection.close()
            print("Desconectado de la base de datos.")

    @property
    def dbname(self):
        return self._dbname

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    