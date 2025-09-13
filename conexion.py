import sqlite3

class Conexion:
    def __init__(self):
        try:
            self.con = sqlite3.connect('base_de_datos.db')
            self.creartabla()
        except Exception as ex:
            print(ex)
            
    def creartabla(self):
        sql_create_table_1 = """CREATE TABLE IF NOT EXISTS usuarios (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nombre TEXT NOT NULL,
                                    usuario TEXT NOT NULL,
                                    pin TEXT NOT NULL
                                );"""
        cur = self.con.cursor()
        cur.execute(sql_create_table_1)
        
con = Conexion()            
   