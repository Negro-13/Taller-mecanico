import flet as ft
import mysql.connector
from Clientes import clientes
from Vehiculo import vehiculos   
from Mecanicos import mecanicos
from Proveedores import proveedores
from Stock import stock

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3308',
            user='root',
            password='root',
            database='Taller_Mecanico',
            ssl_disabled=True
        )
        if connection.is_connected():
            print('Conexión exitosa')
            return connection
    except Exception as ex:
        print('Conexión errónea')
        print(ex)
        return None

connection = connect_to_db()

def menu_principal(page: ft.Page):
    page.window.maximized = True
    page.title = "Administración de Taller Mecánico"
    
    # ----Assets Personales----
    cliente_icono = ft.Image(src="usuario.png", width=28, height=28)
    cliente_item = ft.Row(
        controls=[cliente_icono, ft.Text("Cliente")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )

    vehiculo_icono = ft.Image(src ="vehiculo.png", width=28, height=28)
    vehiculo_item = ft.Row(
        controls=[vehiculo_icono, ft.Text("Vehiculos")],
        alignment=ft.MainAxisAlignment.START,
        spacing= 8
    )
    
    proveedor_icono = ft.Image(src="proveedor.png", width=28, height=28)
    proveedor_item = ft.Row(
        controls=[proveedor_icono, ft.Text("Proveedor")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    repuesto_icono = ft.Image(src="caja-de-cambios.png", width=28, height=28)
    repuesto_item = ft.Row(
        controls=[repuesto_icono, ft.Text("Repuesto")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    empleado_icono = ft.Image(src="empleado.png", width=28, height=28)
    empleado_item = ft.Row(
        controls=[empleado_icono, ft.Text("Empleado")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    ) 
    
    usuario_icono = ft.Image(src="usuarios.png", width=28, height=28)
    usuario_item = ft.Row(
        controls=[usuario_icono, ft.Text("Usuario")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    ficha_tecnica_icono = ft.Image(src="auto.png", width=28, height=28)
    ficha_tecnica_item = ft.Row(
        controls=[ficha_tecnica_icono, ft.Text("Ficha Técnica")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    presupuesto_icono = ft.Image(src="presupuesto.png", width=28, height=28)
    presupuesto_icono_item = ft.Row(
        controls=[presupuesto_icono, ft.Text("Presupuesto")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8
    )
    
    # ---Menús---
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY),
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP),
        ],
        content=ft.Text("Archivo"), tooltip="Archivo"
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(content=vehiculo_item, on_click=lambda e: vehiculo(e, page)),
            ft.PopupMenuItem(content=proveedor_item, on_click=lambda e: proveedor(e, page)),
            ft.PopupMenuItem(content=repuesto_item, on_click=lambda e: producto(e, page)),
            ft.PopupMenuItem(content=empleado_item, on_click=lambda e: empleado(e, page)),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page)),
        ],
        content=ft.Text("Herramientas"), tooltip="Administrador de archivos maestros"
    )
    
    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ficha_tecnica_item),
            ft.PopupMenuItem(content=presupuesto_icono_item),
        ],
        content=ft.Text("Administración"), tooltip="Administración de presupuesto y ficha técnica"
    )
    
    # ---Botones de herramientas---
    boton_cliente = ft.IconButton(
        content=ft.Row(controls=[cliente_icono]),
        tooltip="Cliente",
        on_click=lambda e: cliente(e, page)
    )
    boton_vehiculo = ft.IconButton(
        content=ft.Row(controls=[vehiculo_icono]),
        tooltip="Vehiculo",
        on_click=lambda e: vehiculo(e, page)
    )
    boton_producto = ft.IconButton(
        content=ft.Row(controls=[repuesto_icono]),
        tooltip="Repuesto",
        on_click=lambda e: producto(e, page)
    )
    boton_ficha_tecnica = ft.IconButton(content=ft.Row(controls=[ficha_tecnica_icono]), tooltip="Ficha Técnica")
    boton_presupuesto = ft.IconButton(content=ft.Row(controls=[presupuesto_icono]), tooltip="Presupuesto")
    
    # ---Agregar al layout---
    page.add(
        ft.Row(controls=[archivo_menu, administracion, herramientas_menu], spacing=10),
        ft.Row(controls=[boton_cliente,boton_vehiculo, boton_producto, boton_ficha_tecnica, boton_presupuesto])
    )

def cliente(e, page: ft.Page):
    page.clean()
    menu_principal(page)
    clientes(page)

def vehiculo(e, page:ft.Page):
    page.clean()
    menu_principal(page)
    vehiculos(page)

def proveedor(e, page: ft.Page):
    page.clean()
    menu_principal(page)
    proveedores(page)

def producto(e, page: ft.Page):
    page.clean()
    menu_principal(page)
    stock(page)

def empleado(e, page: ft.Page):
    page.clean()
    menu_principal(page)
    mecanicos(page)

def usuario(e, page: ft.Page):
    pass

def login(page: ft.Page):
    usuario = ft.TextField(label="Usuario")
    clave = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    mensaje = ft.Text("")
    modo_registro = ft.Checkbox(label="Registrar nuevo usuario")

    def validar(e):
        db = connection.cursor()
        if modo_registro.value:
            # Registro de usuario
            db.execute("SELECT * FROM Usuarios WHERE Usuario=%s", (usuario.value,))
            if db.fetchone():
                mensaje.value = "El usuario ya existe"
            else:
                db.execute(
                    "INSERT INTO Usuarios (Usuario, Clave, Nombre, Apellido) VALUES (%s, %s, %s, %s)",
                    (usuario.value, clave.value, nombre.value, apellido.value)
                )
                connection.commit()
                mensaje.value = "Usuario registrado correctamente"
        else:
            # Login
            db.execute("SELECT Nombre, Apellido FROM Usuarios WHERE Usuario=%s AND Clave=%s", (usuario.value, clave.value))
            datos = db.fetchone()
            if datos:
                page.clean()
                page.session.set("usuario", usuario.value)
                page.session.set("nombre", datos[0])
                page.session.set("apellido", datos[1])
                menu_principal(page)
            else:
                mensaje.value = "Usuario o contraseña incorrectos"
        page.update()

    btn_login = ft.ElevatedButton("Ingresar / Registrar", on_click=validar)
    login_form = ft.Column(
        controls=[
            ft.Text("Login", size=24, weight="bold"),
            usuario,
            clave,
            nombre,
            apellido,
            modo_registro,
            btn_login,
            mensaje
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(
        ft.Container(
            content=login_form,
            alignment=ft.alignment.center,
            expand=True
        )
    )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window.maximized = True
    login(page)

ft.app(target=main, assets_dir="assets")
