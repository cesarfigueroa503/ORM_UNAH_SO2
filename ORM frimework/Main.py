from Model import Model

class Direccion(Model):
    id = None
    ciudad = "VARCHAR(255)"
    codigo_postal = "VARCHAR(10)"

    


class Usuario(Model):
    id = None
    nombre = "VARCHAR(255)"
    email = "VARCHAR(255)"
    direccion_id = "INTEGER REFERENCES direccion(id)"

    



if __name__ == "__main__":
   
    

    nuevo_usuario = Usuario()
    nuevo_usuario.id = 5
    nuevo_usuario.nombre = "Kattherine"
    nuevo_usuario.email = "kate@unah.hn"
    nuevo_usuario.direccion_id=2

    print(nuevo_usuario.getById(3))
    

    
    