from Database import Database
import json

class Model:
    def __init__(self, table_name=None):
        """
        Inicializa una nueva instancia de la clase Model.

        Parámetros:
        table_name (str, opcional): Nombre de la tabla asociada al modelo. Por defecto, es None.

        Retorna:
        Model: Una nueva instancia de la clase Model.
        """
        self.db = Database(dbname="pureba001", user="postgres", password="root")
        

    def createTable(self):
        """
        Crea una tabla en la base de datos utilizando los atributos de la clase hija como definiciones de campo.

        Retorna:
        None
        """
        tableName = self.get_class_name()
        fields = self.get_fields()
        if tableName is None and fields:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            field_definitions = []
            
           
            for field_name in fields:
                field_value = getattr(self, field_name)

                if isinstance(field_value, str):
                    # Verifica si el valor del atributo es una cadena (representando metadatos)
                    field_definitions.append(f"{field_name} {field_value}")
                    if ("REFERENCES" or "refernces") in field_value or ("PRIMARY" or "primary") in field_name :
                        setattr(self, field_name, None)
                        
                elif field_name != "db":
                    # Si el atributo no es la conexión a la base de datos, se asume que es un campo regular
                    field_definitions.append(f"{field_name} VARCHAR(255)")
                        

            query = f"CREATE TABLE IF NOT EXISTS {tableName} ({', '.join(field_definitions)})"
            cursor.execute(query)

            cursor.close()
            self.db.disconnect()
            print(f"Tabla {tableName} creada exitosamente.")

        except Exception as e:
            print("Error al crear la tabla:", e)


    def save(self):
        """
        Inserta un nuevo registro en la tabla asociada al modelo utilizando los valores de los atributos de la instancia.

        Retorna:
        None
        """
        tableName = self.get_class_name()
        fields = self.get_fields()

        if tableName is None or len(fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            field_names = []
            placeholders = []
            for field_name in fields:
                field_value = getattr(self, field_name, None)
                if field_value != None:
                    field_names.append(field_name)
                    placeholders.append(field_value)

            field_names = ", ".join(field_names)
            placeholders = ", ".join("%s" for _ in fields)  # Usar placeholders %s para los valores

            query = f"INSERT INTO {tableName} ({field_names}) VALUES ({placeholders})"
            values = [getattr(self, field) for field in fields]
            cursor.execute(query, values)
            
            cursor.close()
            self.db.disconnect()
            print("Registro insertado correctamente.")

        except Exception as e:
            print("Error al insertar el registro:", e)

    def update(self):
        """
        Actualiza un registro existente en la tabla asociada al modelo utilizando los valores de los atributos de la instancia.

        Retorna:
        None
        """
        tableName = self.get_class_name()
        fields = self.get_fields()
        print(fields)
        if tableName is None or len(fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            # Obtener el valor de la clave primaria
            primary_key_value = getattr(self, "id", None)
            if primary_key_value is None:
                raise ValueError("La clave primaria 'id' no ha sido definida.")

            # Construir la cláusula SET para los campos a actualizar
            set_clause = ", ".join([f"{field} = %s" for field in fields if field != "id"])

            # Construir el query de actualización
            query = f"UPDATE {tableName} SET {set_clause} WHERE id = %s"
            values = [getattr(self, field) for field in fields if field != "id"]
            values.append(primary_key_value)

            cursor.execute(query, values)
            cursor.close()
            self.db.disconnect()
            print("Registro actualizado correctamente.")

        except Exception as e:
            print("Error al actualizar el registro:", e)

    def delete(self):
        """
        Elimina un registro existente en la tabla asociada al modelo utilizando la clave primaria "id".

        Retorna:
        None
        """
        tableName = self.get_class_name()
        fields = self.get_fields()

        if tableName is None or len(fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            # Obtener el valor de la clave primaria
            primary_key_value = getattr(self, "id", None)
            if primary_key_value is None:
                raise ValueError("La clave primaria 'id' no ha sido definida.")

            # Construir el query de eliminación
            query = f"DELETE FROM {tableName} WHERE id = %s"
            values = [primary_key_value]

            cursor.execute(query, values)
            cursor.close()
            self.db.disconnect()
            print("Registro eliminado correctamente.")

        except Exception as e:
            print("Error al eliminar el registro:", e)
    
    def getById(self, model_id):
        """
        Obtiene un registro de la tabla asociada al modelo basado en su clave primaria "id".

        Parámetros:
        model_id (int): El valor de la clave primaria "id" del registro que se desea obtener.

        Retorna:
        dict: Un diccionario que contiene los campos relevantes del registro obtenido o None si no se encontró el registro.
        """
        tableName = self.get_class_name()
        fields = self.get_fields()

        if tableName is None or len(fields) == 0:
            raise ValueError("Nombre de tabla o campos no definidos en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            # Construir el query de consulta
            query = f"SELECT * FROM {tableName} WHERE id = %s"
            cursor.execute(query, (model_id,))

            # Obtener el registro y sus campos
            row = cursor.fetchone()
            if row is not None:
                record = {}
                for i, field_name in enumerate(fields):
                    record[field_name] = row[i]
                return record
            else:
                return None

        except Exception as e:
            print("Error al obtener el registro:", e)
            return None

        finally:
            cursor.close()
            self.db.disconnect()


    def findAll(self):
        """
        Obtiene todos los registros de la tabla asociada al modelo.

        Retorna:
        None
        """
        tableName = self.get_class_name()
        fields = self.get_fields()

        if tableName is None:
            raise ValueError("Nombre de tabla no definido en la clase hija.")

        try:
            self.db.connect()
            cursor = self.db._connection.cursor()

            # Construir el query de consulta
            query = f"SELECT * FROM {tableName}"
            cursor.execute(query)

            # Obtener todos los registros y sus campos
            rows = cursor.fetchall()
            result = []

            for row in rows:
                record = {}
                i=0
                for field_name in fields:
                     
                    record[field_name] = row[i]
                    i+=1
                result.append(record)

            cursor.close()
            self.db.disconnect()

            result = '\n'.join([str(item) for item in result])

            print(result)
            return result

        except Exception as e:
            print("Error al obtener los registros:", e)
            return []

    def get_fields(self):
        """
        Obtiene los campos relevantes del modelo en forma de diccionario.

        Retorna:
        dict: Un diccionario que contiene los campos relevantes del modelo y sus valores actuales.
        """
        fields_data = {}
        fields = self.get_class_attributes()
        for field_name in fields:
            field_value = getattr(self, field_name)
            

            if isinstance(field_value, str) or isinstance(field_value, list) or isinstance(field_value, int):
                fields_data[field_name] = field_value
        return fields_data

    def get_class_name(self):
        """
        Obtiene el nombre de la clase actual.

        Retorna:
        str: El nombre de la clase.
        """
        return self.__class__.__name__
    
    def get_class_attributes(self):
        """
        Obtiene una lista con los nombres de los atributos de la clase actual.

        Retorna:
        list: Una lista con los nombres de los atributos.
        """
        return [attr for attr in dir(self) if not attr.startswith("_")]
