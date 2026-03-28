from pymongo import MongoClient

url = "mongodb+srv://dayahanauca:VH86rxWHaQOIZal6@cluster0.kisqnxo.mongodb.net/TiendaRopaDB?retryWrites=true&w=majority"
db_name = "TiendaRopaDB"

client = None
db = None

def conectar_db():
    global client, db
    if not client:
        try:
            client = MongoClient(url)
            db = client[db_name]
            print("Conectado a MongoDB")
        except Exception as e:
            print("Error de conexión:", e)
    return db