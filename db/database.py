from pony.orm import Database
db = Database()
db.bind(provider="sqlite", filename="pyrobots.bd", create_db=True)