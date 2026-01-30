from api.database import get_db_connection

def get_db():
    db = get_db_connection()
    return db
