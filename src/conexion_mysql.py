import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='tragaperras',  # ← ¡CAMBIA ESTO!
            user='root',
            password=''  # ← Si tienes contraseña, ponla aquí
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a MySQL")
            return conexion
    except Error as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        return None

def guardar_puntaje(nombre, puntaje):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO puntajes (nombre, puntaje) VALUES (%s, %s)"
            cursor.execute(query, (nombre, puntaje))
            conexion.commit()
            print(f"✅ Guardado: {nombre} - {puntaje} puntos")
        except Error as e:
            print(f"❌ Error al guardar puntaje: {e}")
        finally:
            cursor.close()
            conexion.close()

def obtener_top_puntajes(limite=10):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT %s"
            cursor.execute(query, (limite,))
            resultado = cursor.fetchall()
            print(f"📊 Resultados obtenidos: {resultado}")
            return resultado
        except Error as e:
            print(f"❌ Error al obtener puntajes: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()
    return []

def vaciar_puntajes():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM puntajes"
            cursor.execute(query)
            conexion.commit()
            print("✅ Tabla 'puntajes' vaciada.")
        except Error as e:
            print(f"❌ Error al vaciar puntajes: {e}")
        finally:
            cursor.close()
            conexion.close()