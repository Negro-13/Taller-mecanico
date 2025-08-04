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
        # Logica sql y el form
        dni_cliente = ft.TextField(label="DNI")
        def eliminar_cliente(e):
            query = "DELETE FROM Clientes WHERE DNI = %s"
            data = (dni_cliente.value,)
            db.cursor.execute(query, data)
            db.connection.commit()

        # Visual
        area_contenido.controls.clear()
        area_contenido.controls.append(dni_cliente)
        area_contenido.controls.append(ft.ElevatedButton("Borrar", on_click=eliminar_cliente))
        page.update()

    def mostrar_todos(e):
        query = "SELECT * FROM Clientes"
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()

        filas = []
        for cliente in resultados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente[0]))),
                    ft.DataCell(ft.Text(cliente[1])),
                    ft.DataCell(ft.Text(cliente[2])),
                    ft.DataCell(ft.Text(cliente[4])),
                    ft.DataCell(ft.Text(cliente[3])),
                ]
            )
            filas.append(fila)

        # Parte visual
        area_contenido.controls.clear()
        area_contenido.controls.append(ft.Text("Lista de Clientes:"))
        area_contenido.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("DNI")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Apellido")),
                    ft.DataColumn(ft.Text("Teléfono")),
                    ft.DataColumn(ft.Text("Dirección")),
                ],
                rows=filas
            )
        )
        page.update()


    def cliente_especifico(e):
        # Logica sql y el form
        dni_cliente = ft.TextField(label="DNI")
        def buscar_cliente(e):
            query = "SELECT * FROM Clientes WHERE DNI=%s"
            data = (dni_cliente.value,)
            db.cursor.execute(query, data)
            db.cursor.fetchone()
            db.connection.commit()

        # Visual
        area_contenido.controls.clear()
        area_contenido.controls.append(dni_cliente)
        area_contenido.controls.append(ft.ElevatedButton("Buscar", on_click=buscar_cliente))
        page.update()


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
