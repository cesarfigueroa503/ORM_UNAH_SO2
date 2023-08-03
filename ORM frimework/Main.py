from Model import Model

class Direccion(Model):
    id = "SERIAL PRIMARY KEY"
    ciudad = "VARCHAR(255)"
    codigo_postal = "VARCHAR(10)"


class Usuario(Model):
    id = "SERIAL PRIMARY KEY"
    nombre = "VARCHAR(255)"
    email = "VARCHAR(255)"
    direccion_id = "INTEGER REFERENCES direccion(id)"
    



if __name__ == "__main__":
   

    nuevo_usuario = Usuario()
    

    print(nuevo_usuario.getById(1))
    