import sys
import sqlite3
import datetime
from sqlite3 import Error
def registrar1(articulos,opcion):
    
    fecha_registro=input("Dime una fecha (dd/mm/aaaa): ")
    fecha_converter = datetime.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
    fecha_actual = datetime.datetime.combine(fecha_converter, datetime.datetime.min.time())
    try:
        with sqlite3.connect("evidencia3.db") as conn:
            monto_total=0
            print("Registrar") 
            contador= max(articulos,default=0)+1
            while opcion!='0':
                print("Conexión establecida")
                mi_cursor = conn.cursor()
                descripcion = input(f"Escribe la descripcion de la venta {contador}: ")
                cantidad = int(input("Escribe la cantidad a comprar del articulo: "))
                precio= float(input(f"Escribe el precio del articulo: "))
                valores = {"folio": contador, "descripcion":descripcion, "cantidad":cantidad,"precio":precio,"fecha_Registro": fecha_actual}
                compra = (contador,descripcion.upper(),cantidad,precio,cantidad*precio,fecha_registro)
                monto_total=monto_total+cantidad*precio
                if contador in articulos:
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :cantidad,:precio)", valores)
                    
                else:
                    articulos[contador]=[]
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO VENTAS VALUES(:folio, :fecha_Registro)", valores)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :cantidad,:precio)", valores)
                opcion=input("Escribe si deseas continuar (1-Continuar registrando/0-Dejar de registar: ")
            print(f"N° {contador}")
            for i in articulos[contador]:
                print(f"Descripcion: {i[1]}\t {i[2]}X ${i[3]}\tMonto Total: {i[4]}\n")
            print("\nMonto total a pagar: ",monto_total)
            input("<<ENTER>>")
            
            print("Registro agregado exitosamente")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            
            print("Se ha cerrado la conexión")

    return articulos,opcion


def Consultar(articulos):
    total=0
    print("\n\tConsulta tus ventas\n")
    buscar=int(input("Introduce el numero de venta a buscar: "))
    if buscar in articulos:
        for consulta in articulos[buscar]:
            print(f"Folio {consulta[0]} \t Descripcion: {consulta[1]}\t {consulta[2]}X ${consulta[3]}\tMonto Total: {consulta[4]}\t Fecha: {consulta[5]}\n")
            total=total+consulta[4]
        print(f"Precio a pagar {total}")
    else:
        print("\n\tNo se ha encontrado dicho numero de venta")
    input("<<ENTER>>")
    return articulos
    
def LeerFecha_SQL():
    separador='*'
    print("\nConsulta de reportes\n")
    while True:
        try:
            fecha_consultar = input("Dime la fecha a buscar (dd/mm/aaaa): ")
            fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
            break        
        except:
            print("Error al capturar la fecha, Vuelva capturar....")
    try:
        with sqlite3.connect("evidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fecha":fecha_consultar}
            mi_cursor.execute("SELECT v.ID_VENTAS,a.NOMBRE,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTA,v.fecha FROM ARTICULOS as a,VENTAS as v WHERE a.ID_VENTAS=v.ID_VENTAS AND DATE(v.FECHA)=:fecha;", criterios)
            registros = mi_cursor.fetchall()
            print('\n')
            for folio, nombre,cantidad,precio,total,fecha_registro in registros:
                print(f"folio = {folio}\nDescripcion = {nombre}\n{cantidad}x${precio}={total}\nFecha de registro: {fecha_registro.strftime('%d/%m/%Y')}\n{separador*30}")
    except sqlite3.Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            print("Se ha cerrado la conexión")
            input("<<ENTER>>")

def Leer_SQL(articulos):
    try:
        with sqlite3.connect("evidencia3.db",detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT v.ID_VENTAS,a.NOMBRE,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTAL,v.Fecha FROM ARTICULOS as a,VENTAS as v where a.ID_VENTAS=v.ID_VENTAS order by v.ID_ventas")
            registros = mi_cursor.fetchall()
            for registro in registros:
                if registro[0] in articulos:
                    articulos[registro[0]].append(registro)
                else:
                    articulos[registro[0]]=[registro]
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    return articulos

articulos={}
Leer_SQL(articulos)
while True:
    print("\n\tMain menu")
    print("1-Registrar una venta")
    print("2-Consultar una venta")
    print("3-Reporte de compras Fechas")
    print("X-Salir ")
    opcion = input("Elige una opcion: ")
    if opcion =='1':
        registrar1(articulos,opcion)
    elif opcion=='2':
        Consultar(articulos)
    elif opcion =='3':
        LeerFecha_SQL()
    elif opcion =='X':
        print("\nSaliendo...\n")
        break
    else:
        print("\n\nError vuelve a intentarlo\n\n")
        input("<<ENTER>>")
