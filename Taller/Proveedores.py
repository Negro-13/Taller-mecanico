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

def proveedores(page: ft.Page):
    page.title = "Interfaz Proveedores"
    db = TallerDB()

    area_derecha = ft.Column()
    area_izquierda = ft.Column()
    bottom_sheet = ft.BottomSheet(
        open=False,
        content=ft.Container(
            content=ft.Column([]),
            padding=20
        )
    )
    page.overlay.append(bottom_sheet)

    def mostrar_todos(e):
        query = "SELECT * FROM Proveedores"
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()

        def editar_proveedor(e):
            cod_prov = e.control.data
            print(f"Editar proveedor con Código: {cod_prov}")

        def eliminar_proveedor(e):
            cod_prov = e.control.data

            def seguro_borrar(ev):
                delete_query = "DELETE FROM Proveedores WHERE Cod_prov = %s"
                db.cursor.execute(delete_query, (cod_prov,))
                db.connection.commit()
                bottom_sheet.open = False
                page.update()
                mostrar_todos(None)

            def cerrar_bs(ev):
                bottom_sheet.open = False
                page.update()

            bottom_sheet.content.content.controls.clear()
            bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar el proveedor?"))
            bottom_sheet.content.content.controls.append(
                ft.Row([
                    ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                    ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                ])
            )
            bottom_sheet.open = True
            page.update()

        filas = []
        for proveedor in resultados:
            cod_prov = proveedor[0]
            btn_editar = ft.ElevatedButton("Editar", on_click=editar_proveedor, data=cod_prov)
            btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_proveedor, data=cod_prov)

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(proveedor[0]))),
                    ft.DataCell(ft.Text(proveedor[1])),
                    ft.DataCell(ft.Text(proveedor[2])),
                    ft.DataCell(ft.Text(proveedor[3])),
                    ft.DataCell(ft.Text(proveedor[4])),
                    ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                ]
            )
            filas.append(fila)

        area_derecha.controls.clear()
        area_derecha.controls.append(ft.Text("Lista de Proveedores:"))
        area_derecha.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Teléfono")),
                    ft.DataColumn(ft.Text("Email")),
                    ft.DataColumn(ft.Text("Dirección")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=filas
            )
        )
        page.update()

    def crear_proveedor(e):
        cod_prov = ft.TextField(label="Código")
        nombre = ft.TextField(label="Nombre")
        telefono = ft.TextField(label="Teléfono")
        email = ft.TextField(label="Email")
        direccion = ft.TextField(label="Dirección")

        def guardar_proveedor(e):
            insert_query = "INSERT INTO Proveedores (Cod_prov, Nombre, Telefono, Email, Direccion) VALUES (%s, %s, %s, %s, %s)"
            data = (
                cod_prov.value,
                nombre.value,
                telefono.value,
                email.value,
                direccion.value
            )
            db.cursor.execute(insert_query, data)
            db.connection.commit()
            mostrar_todos(None)

        boton_crear = ft.ElevatedButton("Crear", on_click=guardar_proveedor)
        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar_proveedor)

        area_izquierda.controls.clear()
        area_izquierda.controls.append(ft.Text("Crear nuevo proveedor:"))
        area_izquierda.controls.append(cod_prov)
        area_izquierda.controls.append(nombre)
        area_izquierda.controls.append(telefono)
        area_izquierda.controls.append(email)
        area_izquierda.controls.append(direccion)
        area_izquierda.controls.append(ft.Row(controls=[boton_buscar, boton_crear]))
        page.update()

    def buscar_proveedor(e):
        area_izquierda.controls.clear()
        campo_busqueda = ft.TextField(label="Ingrese el valor a buscar")

        criterio_dropdown = ft.Dropdown(
            label="Buscar por",
            options=[
                ft.dropdown.Option("Código"),
                ft.dropdown.Option("Nombre"),
                ft.dropdown.Option("Teléfono"),
                ft.dropdown.Option("Email"),
                ft.dropdown.Option("Dirección")
            ],
            value="Código"
        )

        def ejecutar_busqueda(e):
            valor = campo_busqueda.value
            criterio = criterio_dropdown.value

            columnas_sql = {
                "Código": "Cod_prov",
                "Nombre": "Nombre",
                "Teléfono": "Telefono",
                "Email": "Email",
                "Dirección": "Direccion"
            }

            if criterio not in columnas_sql:
                return

            query = f"SELECT * FROM Proveedores WHERE {columnas_sql[criterio]} = %s"
            db.cursor.execute(query, (valor,))
            resultados = db.cursor.fetchall()

            def editar_proveedor(e):
                cod_prov = e.control.data
                print(f"Editar proveedor con Código: {cod_prov}")

            def eliminar_proveedor(e):
                cod_prov = e.control.data

                def seguro_borrar(ev):
                    delete_query = "DELETE FROM Proveedores WHERE Cod_prov = %s"
                    db.cursor.execute(delete_query, (cod_prov,))
                    db.connection.commit()
                    bottom_sheet.open = False
                    page.update()
                    mostrar_todos(None)

                def cerrar_bs(ev):
                    bottom_sheet.open = False
                    page.update()

                bottom_sheet.content.content.controls.clear()
                bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar el proveedor?"))
                bottom_sheet.content.content.controls.append(
                    ft.Row([
                        ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                        ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                    ])
                )
                bottom_sheet.open = True
                page.update()

            filas = []
            for proveedor in resultados:
                cod_prov = proveedor[0]
                btn_editar = ft.ElevatedButton("Editar", on_click=editar_proveedor, data=cod_prov)
                btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_proveedor, data=cod_prov)

                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(proveedor[0])),
                        ft.DataCell(ft.Text(proveedor[1])),
                        ft.DataCell(ft.Text(proveedor[2])),
                        ft.DataCell(ft.Text(proveedor[3])),
                        ft.DataCell(ft.Text(proveedor[4])),
                        ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                    ]
                )
                filas.append(fila)

            area_derecha.controls.clear()
            area_derecha.controls.append(ft.Text("Resultado de la búsqueda:"))
            area_derecha.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Código")),
                        ft.DataColumn(ft.Text("Nombre")),
                        ft.DataColumn(ft.Text("Teléfono")),
                        ft.DataColumn(ft.Text("Email")),
                        ft.DataColumn(ft.Text("Dirección")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=filas
                )
            )
            page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=ejecutar_busqueda)
        boton_crear = ft.ElevatedButton("Crear", on_click=crear_proveedor)
        boton_atras = ft.ElevatedButton("Atras", on_click=mostrar_todos)

        area_izquierda.controls.append(ft.Text("Buscar proveedor"))
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
    buscar_proveedor(None)

#ft.app(target=proveedores)