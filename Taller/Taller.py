import flet as ft
import mysql.connector

class TallerDB:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost', 
                user='root', 
                password='root', 
                port='3308', 
                database='taller_mecanico', 
                ssl_disabled=True 
            )

            if self.connection.is_connected():
                print("> Conexion exitosa")
                self.cursor = self.connection.cursor()
        except Exception as ex:
            print("> Error de conexion:", ex)
            exit()


def main(page: ft.Page):
    page.title = "Gestión de Clientes"
    db = TallerDB()

    area_contenido = ft.Column()
    def crear_cliente(e):
        #Creacion de los cosos del formulario

        dni_cliente = ft.TextField(label="DNI")
        nombre_cliente = ft.TextField(label="Nombre")
        apellido_cliente = ft.TextField(label="Apellido")
        telefono_cliente = ft.TextField(label="Teléfono")
        direccion_cliente = ft.TextField(label="Dirección")

        #Logica con sql

        def guardar_cliente(e):
            insert_query = "INSERT INTO Clientes (DNI, Nombre, Apellido, Direccion, Telefono) VALUES (%s, %s, %s, %s, %s)"
            data = (
                dni_cliente.value,
                nombre_cliente.value,
                apellido_cliente.value,
                direccion_cliente.value,
                telefono_cliente.value
            )
            db.cursor.execute(insert_query, data)
            db.connection.commit()

        #Anadir las cosas visualmente
        area_contenido.controls.clear()
        area_contenido.controls.append(ft.Text("Crear nuevo cliente:"))
        area_contenido.controls.append(dni_cliente)
        area_contenido.controls.append(nombre_cliente)
        area_contenido.controls.append(apellido_cliente)
        area_contenido.controls.append(telefono_cliente)
        area_contenido.controls.append(direccion_cliente)
        area_contenido.controls.append(ft.ElevatedButton("Crear", on_click=guardar_cliente))
        page.update()


    def borrar_cliente(e):
        pass

    def mostrar_todos(e):
        





        query = "SELECT * FROM Clientes"
        db.cursor.execute(query)
        for row in db.cursor.fetchall():
            print(row)

    def cliente_especifico(e):
        pass
    barra_herramientas = ft.Row(
        controls=[
            ft.ElevatedButton("Crear Cliente", on_click=crear_cliente),
            ft.ElevatedButton("Borrar Cliente", on_click=borrar_cliente),
            ft.ElevatedButton("Mostrar Todos", on_click=mostrar_todos),
            ft.ElevatedButton("Cliente Específico", on_click=cliente_especifico)
        ],
        spacing=10
    )

    page.add(barra_herramientas, ft.Divider(), area_contenido)

ft.app(target=main)
