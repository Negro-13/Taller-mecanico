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

def stock(page: ft.Page):
    page.title = "Interfaz Stock"
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
        query = "SELECT * FROM Stock"
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()

        def eliminar_repuesto(e):
            codigo = e.control.data

            def seguro_borrar(ev):
                delete_query = "DELETE FROM Stock WHERE Codigo_repuesto = %s"
                db.cursor.execute(delete_query, (codigo,))
                db.connection.commit()
                bottom_sheet.open = False
                page.update()
                mostrar_todos(None)

            def cerrar_bs(ev):
                bottom_sheet.open = False
                page.update()

            bottom_sheet.content.content.controls.clear()
            bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar el repuesto?"))
            bottom_sheet.content.content.controls.append(
                ft.Row([
                    ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                    ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                ])
            )
            bottom_sheet.open = True
            page.update()

        def modificar_cantidad(codigo, campo, operacion):
            db.cursor.execute("SELECT Cant_rep_libre, Cant_rep_total FROM Stock WHERE Codigo_repuesto = %s", (codigo,))
            cant_libre, cant_total = db.cursor.fetchone()

            if campo == 'Cant_rep_libre':
                nueva_libre = cant_libre + operacion
                if 0 <= nueva_libre <= cant_total:
                    update_query = "UPDATE Stock SET Cant_rep_libre = %s WHERE Codigo_repuesto = %s"
                    db.cursor.execute(update_query, (nueva_libre, codigo))
                    db.connection.commit()
            elif campo == 'Cant_rep_total':
                nueva_total = cant_total + operacion
                # Validar que no sea negativo ni menor que libre
                if nueva_total >= 0 and nueva_total >= cant_libre:
                    update_query = "UPDATE Stock SET Cant_rep_total = %s WHERE Codigo_repuesto = %s"
                    db.cursor.execute(update_query, (nueva_total, codigo))
                    db.connection.commit()
            mostrar_todos(None)

        filas = []
        for repuesto in resultados:
            codigo = repuesto[0]
            btn_mas_libre = ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_libre', 1))
            btn_menos_libre = ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_libre', -1))
            btn_mas_total = ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_total', 1))
            btn_menos_total = ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_total', -1))
            btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_repuesto, data=codigo)

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(repuesto[0]))),
                    ft.DataCell(ft.Text(repuesto[1])),
                    ft.DataCell(ft.Row([btn_menos_libre, ft.Text(str(repuesto[2])), btn_mas_libre])),
                    ft.DataCell(ft.Row([btn_menos_total, ft.Text(str(repuesto[3])), btn_mas_total])),
                    ft.DataCell(ft.Text(str(repuesto[4]))),
                    ft.DataCell(ft.Text(str(repuesto[5]))),
                    ft.DataCell(ft.Row([btn_eliminar]))
                ]
            )
            filas.append(fila)

        area_derecha.controls.clear()
        area_derecha.controls.append(ft.Text("Lista de Repuestos en Stock:"))
        area_derecha.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Descripción")),
                    ft.DataColumn(ft.Text("Cant. Libre")),
                    ft.DataColumn(ft.Text("Cant. Total")),
                    ft.DataColumn(ft.Text("Proveedor")),
                    ft.DataColumn(ft.Text("Precio")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=filas
            )
        )
        page.update()

    def crear_repuesto(e):
        codigo = ft.TextField(label="Código")
        descripcion = ft.TextField(label="Descripción")
        cant_total = ft.TextField(label="Cant. Total", value="0")
        proveedor = ft.TextField(label="Proveedor")
        precio = ft.TextField(label="Precio")

        def guardar_repuesto(e):
            insert_query = "INSERT INTO Stock (Codigo_repuesto, Descripcion, Cant_rep_libre, Cant_rep_total, Proveedor, Precio) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (
                codigo.value,
                descripcion.value,
                cant_total.value,  
                cant_total.value,
                proveedor.value,
                precio.value
            )
            db.cursor.execute(insert_query, data)
            db.connection.commit()
            mostrar_todos(None)

        boton_crear = ft.ElevatedButton("Crear", on_click=guardar_repuesto)
        boton_buscar = ft.ElevatedButton("Buscar", on_click=buscar_repuesto)

        area_izquierda.controls.clear()
        area_izquierda.controls.append(ft.Text("Crear nuevo repuesto:"))
        area_izquierda.controls.append(codigo)
        area_izquierda.controls.append(descripcion)
        area_izquierda.controls.append(cant_total)
        area_izquierda.controls.append(proveedor)
        area_izquierda.controls.append(precio)
        area_izquierda.controls.append(ft.Row(controls=[boton_buscar, boton_crear]))
        page.update()

    def buscar_repuesto(e):
        area_izquierda.controls.clear()
        campo_busqueda = ft.TextField(label="Ingrese el valor a buscar")

        criterio_dropdown = ft.Dropdown(
            label="Buscar por",
            options=[
                ft.dropdown.Option("Código"),
                ft.dropdown.Option("Descripción"),
                ft.dropdown.Option("Proveedor")
            ],
            value="Código"
        )

        def ejecutar_busqueda(e):
            valor = campo_busqueda.value
            criterio = criterio_dropdown.value

            columnas_sql = {
                "Código": "Codigo_repuesto",
                "Descripción": "Descripcion",
                "Proveedor": "Proveedor"
            }

            if criterio not in columnas_sql:
                return

            query = f"SELECT * FROM Stock WHERE {columnas_sql[criterio]} = %s"
            db.cursor.execute(query, (valor,))
            resultados = db.cursor.fetchall()

            def eliminar_repuesto(e):
                codigo = e.control.data

                def seguro_borrar(ev):
                    delete_query = "DELETE FROM Stock WHERE Codigo_repuesto = %s"
                    db.cursor.execute(delete_query, (codigo,))
                    db.connection.commit()
                    bottom_sheet.open = False
                    page.update()
                    mostrar_todos(None)

                def cerrar_bs(ev):
                    bottom_sheet.open = False
                    page.update()

                bottom_sheet.content.content.controls.clear()
                bottom_sheet.content.content.controls.append(ft.Text("¿Seguro que quieres borrar el repuesto?"))
                bottom_sheet.content.content.controls.append(
                    ft.Row([
                        ft.ElevatedButton("Seguro", on_click=seguro_borrar),
                        ft.ElevatedButton("Atrás", on_click=cerrar_bs)
                    ])
                )
                bottom_sheet.open = True
                page.update()

            def modificar_cantidad(codigo, campo, operacion):
                # Obtener los valores actuales
                db.cursor.execute("SELECT Cant_rep_libre, Cant_rep_total FROM Stock WHERE Codigo_repuesto = %s", (codigo,))
                cant_libre, cant_total = db.cursor.fetchone()

                if campo == 'Cant_rep_libre':
                    nueva_libre = cant_libre + operacion
                    # Validar que no sea negativo ni mayor que total
                    if 0 <= nueva_libre <= cant_total:
                        update_query = "UPDATE Stock SET Cant_rep_libre = %s WHERE Codigo_repuesto = %s"
                        db.cursor.execute(update_query, (nueva_libre, codigo))
                        db.connection.commit()
                elif campo == 'Cant_rep_total':
                    nueva_total = cant_total + operacion
                    # Validar que no sea negativo ni menor que libre
                    if nueva_total >= 0 and nueva_total >= cant_libre:
                        update_query = "UPDATE Stock SET Cant_rep_total = %s WHERE Codigo_repuesto = %s"
                        db.cursor.execute(update_query, (nueva_total, codigo))
                        db.connection.commit()
                mostrar_todos(None)

            filas = []
            for repuesto in resultados:
                codigo = repuesto[0]
                btn_mas_libre = ft.IconButton(icon=ft.icons.ADD, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_libre', 1))
                btn_menos_libre = ft.IconButton(icon=ft.icons.REMOVE, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_libre', -1))
                btn_mas_total = ft.IconButton(icon=ft.icons.ADD, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_total', 1))
                btn_menos_total = ft.IconButton(icon=ft.icons.REMOVE, on_click=lambda e, c=codigo: modificar_cantidad(c, 'Cant_rep_total', -1))
                btn_eliminar = ft.ElevatedButton("Eliminar", on_click=eliminar_repuesto, data=codigo)

                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(repuesto[0]))),
                        ft.DataCell(ft.Text(repuesto[1])),
                        ft.DataCell(ft.Row([btn_menos_libre, ft.Text(str(repuesto[2])), btn_mas_libre])),
                        ft.DataCell(ft.Row([btn_menos_total, ft.Text(str(repuesto[3])), btn_mas_total])),
                        ft.DataCell(ft.Text(str(repuesto[4]))),
                        ft.DataCell(ft.Text(str(repuesto[5]))),
                        ft.DataCell(ft.Row([btn_eliminar]))
                    ]
                )
                filas.append(fila)

            area_derecha.controls.clear()
            area_derecha.controls.append(ft.Text("Resultado de la búsqueda:"))
            area_derecha.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Código")),
                        ft.DataColumn(ft.Text("Descripción")),
                        ft.DataColumn(ft.Text("Cant. Libre")),
                        ft.DataColumn(ft.Text("Cant. Total")),
                        ft.DataColumn(ft.Text("Proveedor")),
                        ft.DataColumn(ft.Text("Precio")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=filas
                )
            )
            page.update()

        boton_buscar = ft.ElevatedButton("Buscar", on_click=ejecutar_busqueda)
        boton_crear = ft.ElevatedButton("Crear", on_click=crear_repuesto)
        boton_atras = ft.ElevatedButton("Atras", on_click=mostrar_todos)

        area_izquierda.controls.append(ft.Text("Buscar repuesto"))
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
    buscar_repuesto(None)

#ft.app(target=stock)
