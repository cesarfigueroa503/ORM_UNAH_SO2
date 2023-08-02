from DataBase import Database

class Field:
    def __init__(self, data_type):
        self.data_type = data_type

class PrimaryKey:
    pass

class ForeignKey:
    def __init__(self, referenced_table):
        self.referenced_table = referenced_table

class Model:
    tableName = None
    fields = []

    def __init__(self):
        self.tableName = self.get_class_name()
        self.fields = self.get_field()
        self.db = Database(dbname="pureba001", user="postgres", password="root")

    def createTable(self):
        self.tableName = self.get_class_name()
        self.fields = self.get_field()

        print(self.tableName)

        if self.tableName is None or len(self.fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()


            field_definitions = [f"{field_name} {field.data_type}" for field_name, field in self.fields.items()]
            query = f"CREATE TABLE IF NOT EXISTS {self.tableName} ({', '.join(field_definitions)})"
            cursor.execute(query)

            cursor.close()
            self.db.disconnect()
            print(f"Tabla {self.tableName} creada exitosamente.")

        except Exception as e:
            print("Error al crear la tabla:", e)

    
    def save(self):
        if self.tableName is None or len(self.fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db.connection.cursor()

            field_names = ", ".join(self.fields)
            placeholders = ", ".join("%s" for _ in self.fields)
            values = [getattr(self, field) for field in self.fields]

            query = f"INSERT INTO {self.tableName} ({field_names}) VALUES ({placeholders})"
            cursor.execute(query, values)

            cursor.close()
            self.db.disconnect()
            print("Registro insertado correctamente.")

        except Exception as e:
            print("Error al insertar el registro:", e)

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
    
    def getById(self, model_id):
        raise NotImplementedError

    def findAll(self):
        raise NotImplementedError

    def get_field(self):
        fields = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            #print(attr)
            if callable(attr) and hasattr(attr, 'is_field'):
                fields[attr_name] = attr
        return fields

    

    def get_class_name(self):
        return self.__class__.__name__

def field(data_type):
    def decorator(func):
        setattr(func, 'is_field', True)
        setattr(func, 'data_type', data_type)
        return func
    return decorator


def Entity(cls):
    return cls

def Field(data_type):
    def decorator(func):
        func.fields = getattr(func, 'fields', {})
        func.fields[func.__name__] = Field(data_type)
        return func
    return decorator

def PrimaryKey(cls):
    return cls

def ForeignKey(referenced_table):
    def decorator(func):
        func.fields = getattr(func, 'fields', {})
        func.fields[func.__name__] = ForeignKey(referenced_table)
        return func
    return decorator

@Entity
class Usuario(Model):
    tableName = "usuarios"

    @PrimaryKey
    def id(self):
        pass

    @Field("VARCHAR(255)")
    def nombre(self):
        pass

    @Field("VARCHAR(255)")
    def email(self):
        pass

if __name__ == "__main__":
    # Crear un nuevo usuario y establecer sus datos
    nuevo_usuario = Usuario()
    nuevo_usuario.nombre = "Juan"
    nuevo_usuario.email = "juan@example.com"

    try:
        nuevo_usuario.createTable()  # Crear la tabla en la base de datos
        nuevo_usuario.save()  # Insertar el nuevo usuario en la base de datos
    except Exception as e:
        print("Error:", e)