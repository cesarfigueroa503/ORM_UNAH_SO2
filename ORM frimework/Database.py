import psycopg2

class Database:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._connection = None

    def connect(self):
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

    