import sys
import datetime
import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect("evidencia3.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS VENTAS (ID_VENTAS INTEGER PRIMARY KEY, FECHA TIMESTAMP NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS ARTICULOS (ID_VENTAS INTEGER, NOMBRE TEXT NOT NULL,CANTIDAD INTEGER NOT NULL,PRECIO FLOAT NOT NULL, FOREIGN KEY(ID_VENTAS) REFERENCES VENTAS(ID_VENTAS));")
        print("Tabla creada exitosamente")
except Error as e:
    print (e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    conn.close()
