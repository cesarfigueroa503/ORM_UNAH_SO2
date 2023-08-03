from Model import Model

class Direccion(Model):
    id=0
    ciudad=""
    codigo_postal =""

    


class Usuario(Model):
    id = "SEIRAL PRIMARY KEY"
    nombre = "VARCHAR(255)"
    email = "VARCHAR(255)"
    direccion_id = "INTEGER REFERENCES direccion(id)"

    



if __name__ == "__main__":
   
    direccion = Direccion()
    usuario = Usuario()

    #Creacion de una nueva direccion
    direccion.id = None
    direccion.ciudad = "Choloma"
    direccion.codigo_postal = "1200"
    
    direccion.save()
    #direccion.update()

    #Creacion de un nuevo Usuario

    usuario.id = None
    usuario.nombre = "Maria"
    usuario.email = "maria@unah.hn"
    usuario.direccion_id = 2

    

    
    