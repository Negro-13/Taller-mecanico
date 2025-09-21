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

def mecanicos(page: ft.Page):
    page.title = "Interfaz Mecanicos"
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
        query = "SELECT * FROM Mecanicos"
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()

        def editar_mecanico(e):
            legajo = e.control.data
            print(f"Editar mecanico con Legajo: {legajo}")

        def eliminar_mecanico(e):
            legajo = e.control.data

            def seguro_borrar(ev):
                delete_query = "DELETE FROM Mecanicos WHERE Legajo = %s"
                db.cursor.execute(delete_query, (legajo,))
                db.connection.commit()
                bottom_sheet.open = False
                page.update()
                mostrar_todos(None)

            def cerrar_bs(ev):
                bottom_sheet.open = False
                page.update()

            bottom_sheet.content.content.controls.clear()
            bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar al mecanico?"))
            bottom_sheet.content.content.controls.append(
                ft.Row([
                    ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                    ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                ])
            )
            bottom_sheet.open = True
            page.update()

        filas = []
        for mecanico in resultados:
            legajo = mecanico[0]
            btn_editar = ft.ElevatedButton("Editar", on_click=editar_mecanico, data=legajo)
            btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_mecanico, data=legajo)

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(mecanico[0]))),
                    ft.DataCell(ft.Text(mecanico[1])),
                    ft.DataCell(ft.Text(mecanico[2])),
                    ft.DataCell(ft.Text(mecanico[3])),
                    ft.DataCell(ft.Text(mecanico[4])),
                    ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                ]
            )
            filas.append(fila)

        area_derecha.controls.clear()
        area_derecha.controls.append(ft.Text("Lista de Mecanicos:"))
        area_derecha.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Legajo")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Apellido")),
                    ft.DataColumn(ft.Text("Rol")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=filas
            )
        )
        page.update()

    def crear_mecanico(e):
        legajo_mecanico = ft.TextField(label="Lejajo")
        nombre_mecanico = ft.TextField(label="Nombre")
        apellido_mecanico = ft.TextField(label="Apellido")
        rol_mecanico = ft.TextField(label="Rol")
        estado_mecanico = ft.TextField(label="Estado")

        def guardar_mecanico(e):
            insert_query = "INSERT INTO Mecanicos (Legajo, Nombre, Apellido, Rol, Estado) VALUES (%s, %s, %s, %s, %s)"
            data = (
                legajo_mecanico.value,
                nombre_mecanico.value,
                apellido_mecanico.value,
                rol_mecanico.value,
                estado_mecanico.value
            )
            db.cursor.execute(insert_query, data)
            db.connection.commit()
            mostrar_todos(None)
        
        boton_crear = ft.ElevatedButton("Crear", on_click=guardar_mecanico)
        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar_mecanico)

        area_izquierda.controls.clear()
        area_izquierda.controls.append(ft.Text("Crear nuevo mecanico:"))
        area_izquierda.controls.append(legajo_mecanico)
        area_izquierda.controls.append(nombre_mecanico)
        area_izquierda.controls.append(apellido_mecanico)
        area_izquierda.controls.append(rol_mecanico)
        area_izquierda.controls.append(estado_mecanico)
        area_izquierda.controls.append(ft.Row(controls=[boton_buscar, boton_crear]))
        page.update()

    def buscar_mecanico(e):
        area_izquierda.controls.clear()

        campo_busqueda = ft.TextField(label="Ingrese el valor a buscar")

        criterio_dropdown = ft.Dropdown(
            label="Buscar por",
            options=[
                ft.dropdown.Option("Legajo"),
                ft.dropdown.Option("Nombre"),
                ft.dropdown.Option("Apellido"),
                ft.dropdown.Option("Rol")
            ],
            value="Legajo"
        )

        def ejecutar_busqueda(e):
            valor = campo_busqueda.value
            criterio = criterio_dropdown.value

            columnas_sql = {
                "Legajo": "Legajo",
                "Nombre": "Nombre",
                "Apellido": "Apellido",
                "Rol": "Rol"
            }

            if criterio not in columnas_sql:
                return

            query = f"SELECT * FROM Mecanicos WHERE {columnas_sql[criterio]} = %s"
            db.cursor.execute(query, (valor,))
            resultados = db.cursor.fetchall()

            def editar_mecanico(e):
                legajo = e.control.data
                print(f"Editar Mecanico con legajo: {legajo}")

            def eliminar_mecanico(e):
                legajo = e.control.data

                def seguro_borrar(ev):
                    delete_query = "DELETE FROM Mecanicos WHERE Legajo = %s"
                    db.cursor.execute(delete_query, (legajo,))
                    db.connection.commit()
                    bottom_sheet.open = False
                    page.update()
                    mostrar_todos(None)

                def cerrar_bs(ev):
                    bottom_sheet.open = False
                    page.update()

                bottom_sheet.content.content.controls.clear()
                bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar al mecanico?"))
                bottom_sheet.content.content.controls.append(
                    ft.Row([
                        ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                        ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                    ])
                )
                bottom_sheet.open = True
                page.update()

            filas = []
            for mecanico in resultados:
                legajo = mecanico[0]
                btn_editar = ft.ElevatedButton("Editar", on_click=editar_mecanico, data=legajo)
                btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_mecanico, data=legajo)

                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(mecanico[0]))),
                        ft.DataCell(ft.Text(mecanico[1])),
                        ft.DataCell(ft.Text(mecanico[2])),
                        ft.DataCell(ft.Text(mecanico[3])),
                        ft.DataCell(ft.Text(mecanico[4])),
                        ft.DataCell(ft.Row(controls=[btn_editar, btn_eliminar]))
                    ]
                )
                filas.append(fila)

            area_derecha.controls.clear()
            area_derecha.controls.append(ft.Text("Resultado de la búsqueda:"))
            area_derecha.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Legajo")),
                        ft.DataColumn(ft.Text("Nombre")),
                        ft.DataColumn(ft.Text("Apellido")),
                        ft.DataColumn(ft.Text("Rol")),
                        ft.DataColumn(ft.Text("Estado")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=filas
                )
            )
            page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=ejecutar_busqueda)
        boton_crear = ft.ElevatedButton("Crear", on_click=crear_mecanico)
        boton_atras = ft.ElevatedButton("Atras", on_click=mostrar_todos)

        area_izquierda.controls.append(ft.Text("Buscar mecanico"))
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
    buscar_mecanico(None)

# ft.app(target=mecanicos)
