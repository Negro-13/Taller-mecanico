import flet as ft
import mysql.connector

class TallerDB:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                port='3306',
                database='taller_mecanico',
                ssl_disabled=True
            )
            if self.connection.is_connected():
                print("> Conexion exitosa")
                self.cursor = self.connection.cursor()
        except Exception as ex:
            print("> Error de conexion:", ex)
            exit()

def vehiculos(page: ft.Page):
    page.title = "Interfaz Vehiculo"
    db = TallerDB()

    area_derecha = ft.Column()
    area_izquierda = ft.Column()

    def mostrar_todos(e):
        query = "SELECT * FROM Vehiculos"
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()

        def editar_vehiculo(e):
            dni = e.control.data
            print(f"Editar cliente con DNI: {dni}")

        def eliminar_vehiculo(e):
            patente = e.control.data
            delete_query = "DELETE FROM Vehiculos WHERE Patente = %s"
            db.cursor.execute(delete_query, (patente,))
            db.connection.commit()
            mostrar_todos(None)

        filas = []
        for vehiculo in resultados:
            patente = vehiculo[0]
            btn_editar = ft.ElevatedButton("Editar", on_click=editar_vehiculo, data=patente)
            btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_vehiculo, data=patente)

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(patente[0]))),
                    ft.DataCell(ft.Text(patente[1])),
                    ft.DataCell(ft.Text(patente[2])),
                    ft.DataCell(ft.Text(patente[4])),
                    ft.DataCell(ft.Text(patente[3])),
                    ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                ]
            )
            filas.append(fila)

        area_derecha.controls.clear()
        area_derecha.controls.append(ft.Text("Lista de Vehiculos:"))
        area_derecha.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Patente")),
                    ft.DataColumn(ft.Text("DNI")),
                    ft.DataColumn(ft.Text("Marca")),
                    ft.DataColumn(ft.Text("Modelo")),
                    ft.DataColumn(ft.Text("Color")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=filas
            )
        )
        page.update()
#terminar de hacer
    def crear_cliente(e):
        patente_vehiculo = ft.TextField(label="Patente")
        nombre_cliente = ft.TextField(label="DNI")
        apellido_cliente = ft.TextField(label="Marca")
        telefono_cliente = ft.TextField(label="Modelo")
        direccion_cliente = ft.TextField(label="Color")

        def guardar_cliente(e):
            insert_query = "INSERT INTO Vehiculos (Patente, DNI, Marca, Modelo, Color) VALUES (%s, %s, %s, %s, %s)"
            data = (
                patente_vehiculo.value,
                nombre_cliente.value,
                apellido_cliente.value,
                direccion_cliente.value,
                telefono_cliente.value
            )
            db.cursor.execute(insert_query, data)
            db.connection.commit()
            mostrar_todos(None)
        
        boton_crear = ft.ElevatedButton("Crear", on_click=guardar_cliente)
        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar_cliente)

        area_izquierda.controls.clear()
        area_izquierda.controls.append(ft.Text("Crear nuevo cliente:"))
        area_izquierda.controls.append(dni_cliente)
        area_izquierda.controls.append(nombre_cliente)
        area_izquierda.controls.append(apellido_cliente)
        area_izquierda.controls.append(telefono_cliente)
        area_izquierda.controls.append(direccion_cliente)
        area_izquierda.controls.append(ft.Row(controls=[boton_buscar, boton_crear]))
        page.update()

    def buscar_cliente(e):
        area_izquierda.controls.clear()

        campo_busqueda = ft.TextField(label="Ingrese el valor a buscar")

        criterio_dropdown = ft.Dropdown(
            label="Buscar por",
            options=[
                ft.dropdown.Option("DNI"),
                ft.dropdown.Option("Nombre"),
                ft.dropdown.Option("Apellido"),
                ft.dropdown.Option("Teléfono")
            ],
            value="DNI"
        )

        def ejecutar_busqueda(e):
            valor = campo_busqueda.value
            criterio = criterio_dropdown.value

            columnas_sql = {
                "DNI": "DNI",
                "Nombre": "Nombre",
                "Apellido": "Apellido",
                "Teléfono": "Telefono"
            }

            if criterio not in columnas_sql:
                return

            query = f"SELECT * FROM Clientes WHERE {columnas_sql[criterio]} = %s"
            db.cursor.execute(query, (valor,))
            resultados = db.cursor.fetchall()

            def editar_cliente(e):
                dni = e.control.data
                print(f"Editar cliente con DNI: {dni}")

            def eliminar_cliente(e):
                dni = e.control.data
                delete_query = "DELETE FROM Clientes WHERE DNI = %s"
                db.cursor.execute(delete_query, (dni,))
                db.connection.commit()
                mostrar_todos(None)

            filas = []
            for cliente in resultados:
                dni = cliente[0]
                btn_editar = ft.ElevatedButton("Editar", on_click=editar_cliente, data=dni)
                btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_cliente, data=dni)

                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente[0])),
                        ft.DataCell(ft.Text(cliente[1])),
                        ft.DataCell(ft.Text(cliente[2])),
                        ft.DataCell(ft.Text(cliente[4])),
                        ft.DataCell(ft.Text(cliente[3])),
                        ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                    ]
                )
                filas.append(fila)

            area_derecha.controls.clear()
            area_derecha.controls.append(ft.Text("Resultado de la búsqueda:"))
            area_derecha.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("DNI")),
                        ft.DataColumn(ft.Text("Nombre")),
                        ft.DataColumn(ft.Text("Apellido")),
                        ft.DataColumn(ft.Text("Teléfono")),
                        ft.DataColumn(ft.Text("Dirección")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=filas
                )
            )
            page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=ejecutar_busqueda)
        boton_crear = ft.ElevatedButton("Crear", on_click=crear_cliente)
        boton_atras = ft.ElevatedButton("Atras", on_click=mostrar_todos)

        area_izquierda.controls.append(ft.Text("Buscar cliente"))
        area_izquierda.controls.append(criterio_dropdown)
        area_izquierda.controls.append(campo_busqueda)
        area_izquierda.controls.append(ft.Row(controls=[boton_buscar, boton_crear, boton_atras]))
        page.update()

    layout = ft.Row(
        expand=True,
        controls=[
            ft.Container(content=area_izquierda, expand=3, padding=10),
            ft.Container(content=area_derecha, expand=7, padding=10)
        ]
    )

    page.add(layout)
    mostrar_todos(None)
    buscar_cliente(None)

ft.app(target=vehiculos)
