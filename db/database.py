from pony.orm import Database

<<<<<<< HEAD
=======

>>>>>>> origin/PB-24-verificacion-de-correo
db = Database()
db.bind(provider="sqlite", filename="pyrobots.bd", create_db=True)


def gen_map():
<<<<<<< HEAD
    """
    Asigna las entidades definidas a las tablas de la base de datos
    """
=======
    '''
    Asigna las entidades definidas a las tablas de la base de datos
    '''
>>>>>>> origin/PB-24-verificacion-de-correo
    db.generate_mapping(create_tables=True)
