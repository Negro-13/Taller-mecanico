import os, mysql.connector, time

os.system("cls" if os.name == "nt" else "clear")


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


    def clean(self):
        os.system("cls" if os.name == "nt" else "clear")

# Menus

    def menu(self):
        print("1. Clientes")
        print("2. Vehiculos")
        print("3. Mecanicos")
        print("4. Reparaciones")
        print("5. Fichas Tecnicas")
        print("6. Salir")

    def menu_clientes(self):
        print("1. Ver clientes")
        print("2. Ver cliente especifico")
        print("3. Ver vehiculo/s del cliente")
        print("4. Alta cliente")
        print("5. Baja cliente")
        print("6. Volver ")

    def menu_vehiculos(self):
        print("1. Ver vehiculos")
        print("2. Ver vehiculo especifico")
        print("3. Ingresar vehiculo")
        print("4. Eliminar vehiculo")
        print("5. Volver")

    def menu_mecanicos(self):
        print("1. Ver mecanicos")
        print("2. Ingresar mecanico")
        print("3. Ver mecanico especifico")
        print("4. Eliminar mecanico")
        print("5. Volver")

    def menu_reparaciones(self):
        print("1. Ver reparaciones")
        print("2. Ver reparacion especifica")
        print("3. Ingresar reparacion")
        print("4. Eliminar reparacion")
        print("5. Respuestos")
        print("6. Volver")

    def menu_respuestos(self):
        print("1. Agregar repuestos usados en reparacion")
        print("X. Eliminar repuestos usados en reparacion(No usar ya que se eliminarian todos los respuestos q compartan codigo)")
        print("3. Ver repuestos usados en reparacion especifica")
        print("4. Volver")
# Funciones

#Cliente
    def All_Clientes(self):
        query = "SELECT * FROM Clientes"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")

    def Crear_Cliente(self):
        insert_query = "INSERT INTO Clientes (DNI, Nombre, Apellido, Direccion, Telefono) VALUES (%s, %s, %s, %s, %s)"
        dni = input("Ingrese DNI: ")
        nombre = input("Ingrese Nombre: ")
        apellido = input("Ingrese Apellido: ")
        direccion = input("Ingrese Direccion: ")
        telefono = input("Ingrese Telefono: ")

        data = (dni, nombre, apellido, direccion, telefono)
        self.cursor.execute(insert_query, data)
        self.connection.commit()
        print("> Cliente creado exitosamente.")
        print("> Volviendo al menu principal...")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")

    def Cliente_especifico(self):
        query = "SELECT DNI, Nombre, Apellido, Telefono FROM Clientes WHERE DNI=%s"
        dni = int(input("Ingrese DNI: "))
        data = (dni,)
        self.cursor.execute(query, data)
        fila = self.cursor.fetchone()
        if fila is not None:
            dni, nombre, apellido, telefono = fila
            print(
                "> DNI:",
                dni,
                "|",
                "Nombre:",
                nombre,
                "|",
                "Apellido:",
                apellido,
                "|",
                "Telefono:",
                telefono,
            )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()
        else:
            print("> No se encontraron resultados")

    def Vehiculos_cliente(self):
        query = "SELECT Patente, Marca, Modelo FROM Vehiculos WHERE DNI=%s"
        dni = int(input("Ingrese DNI del cliente: "))
        data = (dni,)
        self.cursor.execute(query, data)
        filas = self.cursor.fetchall()
        if filas is not None:
            for fila in filas:
                patente, marca, modelo = fila
                print(
                    "> Patente:",
                    patente,
                    "|",
                    "Marca:",
                    marca,
                    "|",
                    "Modelo:",
                    modelo,
                )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

        else:
            print("> No se encontraron resultados")

    def Eliminar_cliente(self):
        query = "DELETE FROM Clientes WHERE DNI = %s"
        data = int(input("Ingresar DNI: "))
        dni = (data)
        self.cursor.execute(query, data)
        print("> Eliminando...")
        time.sleep(1)
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()
        self.connection.commit()

# Veiculos

    def Vehiculos(self):
        query = "SELECT * FROM Vehiculos"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

    def Crear_Vehiculo(self):
        insert_query = "INSERT INTO Vehiculos (Patente,DNI, Marca, Modelo, Color) VALUES (%s,%s,%s,%s,%s)"

        patente = input("Ingrese patente: ")
        dni = input("Ingrese DNI del dueño: ")
        marca = input("Ingrese marca: ")
        modelo = input("Ingrese modelo: ")
        color = input("Ingrese color: ")

        data = (patente, dni, marca, modelo, color)
        self.cursor.execute(insert_query, data)
        self.connection.commit()
        print("> El vehiculo ha sido creado exitosamente.")
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()

    def Vehiculo_especifico(self):
        query = "SELECT Patente, Marca, Modelo FROM Vehiculos WHERE Patente=%s"
        patente = input("Ingrese Patente del vehiculo: ")
        data = (patente,)
        self.cursor.execute(query, data)
        fila = self.cursor.fetchone()
        if fila is not None:
            patente, marca, modelo = fila
            print(
                "> Patente: ",
                patente,
                "|",
                "Marca: ",
                marca,
                "|",
                "Modelo: ",
                modelo,
            )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

        else:
            print("> No se encontraron resultados")

    def Eliminar_vehiculo(self):
        query = "DELETE FROM Vehiculos WHERE Patente = %s"
        patente = input("Ingresar Patente: ")
        data = (patente,)
        self.cursor.execute(query, data)
        print("> Eliminando...")
        time.sleep(1)
        print(">Volviendo al menu principal...")
        time.sleep(1)
        self.clean()

        self.connection.commit()

#Mecanicos
    def Mecanicos(self):
        query = "SELECT * FROM Mecanicos"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)
        option = input("> Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

    def Crear_Mecanico(self):
        insert_query = "INSERT INTO Mecanicos (Legajo, Nombre, Apellido, Rol, Estado) VALUES (%s, %s, %s, %s, %s)"
        legajo = input("Ingrese Legajo: ")
        nombre = input("Ingrese Nombre: ")
        apellido = input("Ingrese Apellido: ")
        rol = input("Ingrese Rol: ").capitalize()
        estado = input("Ingrese Estado (Libre / Ocupado): ")
        while estado not in ["Libre", "Ocupado", "libre", "ocupado"]:
            print("Estado invalido, debe ser 'Libre' o 'Ocupado'")
            estado = input("Ingrese Estado (Libre / Ocupado): ")
        data = (legajo, nombre, apellido, rol, estado)
        self.cursor.execute(insert_query, data)
        self.connection.commit()
        print("> Mecanico creado exitosamente.")
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()

    def Mecanico_especifico(self):
        query = "SELECT Legajo, Nombre, Apellido, Rol, Estado FROM Mecanicos WHERE Legajo=%s"
        legajo = input("Ingrese Legajo del mecanico: ")
        data = (legajo,)
        self.cursor.execute(query, data)
        fila = self.cursor.fetchone()
        if fila is not None:
            legajo, nombre, apellido, rol, estado = fila
            print(
                "> Legajo:",
                legajo,
                "|",
                "Nombre:",
                nombre,
                "|",
                "Apellido:",
                apellido,
                "|",
                "Rol:",
                rol,
                "|",
                "Estado:",
                estado,
            )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

        else:
            print("No se encontraron resultados")

    def Eliminar_mecanico(self):
        query = "DELETE FROM Mecanicos WHERE Legajo = %s"
        legajo = input("Ingresar Legajo: ")
        data = (legajo,)   
        self.cursor.execute(query, data)
        print("> Eliminando...")
        time.sleep(1)
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()
        self.connection.commit()

#Reparacioes

    def All_Reparaciones(self):
        query = "SELECT * FROM Reparaciones"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()
    
    def Crear_Reparacion(self):
        insert_query = "INSERT INTO Reparaciones (ID, Patente, DNI, Legajo, Fecha) VALUES (%s, %s, %s, %s, %s)"
        id_reparacion = input("Ingrese ID de la reparacion: ")
        patente = input("Ingrese Patente del vehiculo: ")
        dni = input("Ingrese DNI del cliente: ")
        legajo = input("Ingrese Legajo del mecanico: ")
        fecha = input("Ingrese Fecha (YYYY-MM-DD): ")
        data = (id_reparacion, patente, dni, legajo, fecha)
        self.cursor.execute(insert_query, data)
        self.connection.commit()
        print("> Reparacion creada exitosamente.")
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()

    def Reparacion_especifica(self):
        query = "SELECT * FROM Reparaciones WHERE ID=%s"
        id_reparacion = input("Ingrese ID de la reparacion: ")
        data = (id_reparacion,)
        self.cursor.execute(query, data)
        fila = self.cursor.fetchone()
        if fila is not None:
            id_reparacion, patente, dni, legajo, fecha = fila
            print(
                "> ID de reparacion:",
                id_reparacion,
                "|",    
                "Patente:",
                patente,
                "|",
                "DNI del cliente:",
                dni,
                "|",
                "Legajo del mecanico:",
                legajo,
                "|",
                "Fecha:",
                fecha,
            )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()
    
    def Eliminar_reparacion(self):
        query = "DELETE FROM Reparaciones WHERE ID = %s"
        id_reparacion = input("Ingresar ID de la reparacion: ")
        data = (id_reparacion,)
        self.cursor.execute(query, data)
        print("> Eliminando...")
        time.sleep(1)
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()
        self.connection.commit()

# Repuestos

    def Agregar_repuestos(self):
        insert_query = "INSERT INTO Repuestos (ID, Codigo_repuesto, Precio, Cant_rep, Descripcion) VALUES (%s, %s, %s, %s, %s)"
        id_repuesto = input("Ingrese ID de la reparacion: ")
        codigo_repuesto = input("Ingrese Codigo del repuesto: ")
        precio = float(input("Ingrese Precio del repuesto: "))
        cant_rep = int(input("Ingrese Cantidad de repuestos: "))
        descripcion = input("Ingrese Descripcion del repuesto: ")
        data = (id_repuesto, codigo_repuesto, precio, cant_rep, descripcion)
        self.cursor.execute(insert_query, data)
        self.connection.commit()
        print("> Repuesto agregado exitosamente.")
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()

    def Eliminar_repuestos(self):
        query = "DELETE FROM Repuestos WHERE ID = %s"
        id_repuesto = input("Ingresar ID del repuesto: ")
        data = (id_repuesto,)
        self.cursor.execute(query, data)
        print("> Eliminando...")
        time.sleep(1)
        print("> Volviendo al menu principal...")
        time.sleep(1)
        self.clean()
        self.connection.commit()

    def Repuestos_especificos(self):
        query = "SELECT * FROM Repuestos WHERE ID=%s"
        id_reparacion = input("Ingrese ID de la reparacion la cual desee ver sus repuestos: ")
        data = (id_reparacion,)
        self.cursor.execute(query, data)
        filas = self.cursor.fetchall()
        if filas is not None:
            for fila in filas:
                id_repuesto, codigo_repuesto, precio, cant_rep, importe, descripcion = fila
                print(
                    "> ID de reparacion:",
                    id_repuesto,
                    "|",
                    "Codigo de repuesto:",
                    codigo_repuesto,
                    "|",
                    "Precio:",
                    precio,
                    "|",
                    "Cantidad de repuestos:",
                    cant_rep,
                    "|",
                    "Importe:",
                    importe,
                    "|",
                    "Descripcion:",
                    descripcion,
                )
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

# Ficha Tecnicas

    def Fichas_Tecnicas(self):
        query = "SELECT * FROM Reparaciones WHERE ID=%s"
        id_reparacion = input("Ingrese ID de la reparacion La cual desee ver su ficha tecnica: ")
        data = (id_reparacion,)
        self.cursor.execute(query, data)
        fila = self.cursor.fetchone()
        if fila is not None:
            id_reparacion, patente, dni, legajo, fecha = fila
            print(
                "> ID de reparacion:",
                id_reparacion,
                "|",    
                "Patente:",
                patente,
                "|",
                "DNI del cliente:",
                dni,
                "|",
                "Legajo del mecanico:",
                legajo,
                "|",
                "Fecha:",
                fecha,
            )
            print('Detalle')
            query2 = "SELECT * FROM Repuestos WHERE ID=%s"
            self.cursor.execute(query2, data)
            filas = self.cursor.fetchall()
            if filas is not None:
                total_importe = 0
                for fila in filas:
                    id_repuesto, codigo_repuesto, precio, cant_rep, importe, descripcion = fila
                    print(
                        ">"
                        "Codigo de repuesto:",
                        codigo_repuesto,
                        "|",
                        "Precio:",
                        precio,
                        "|",
                        "Cantidad de repuestos:",
                        cant_rep,
                        "|",
                        "Importe:",
                        importe,
                        "|",
                        "Descripcion:",
                        descripcion,
                    )
                    total_importe += importe
                print("> Importe total de la reparacion:", total_importe)
        option = input("Volver al menu principal? (s): ")
        if option.lower() == "s":
            print("> Volviendo al menu principal...")
            time.sleep(1)
            self.clean()

# Salir

    def salir(self):
        print("> Saliendo del programa...")
        time.sleep(1)
        self.cursor.close()
        self.connection.close()
        exit()


while True:
    conexion = TallerDB()
    conexion.menu()
    try:
        option = int(input("Seleccione una opcion: \n"))
    except ValueError:
        print("> Por favor, ingrese un número válido.\n")
        continue

#Clientes

    if option == 1:
        conexion.clean()
        conexion.menu_clientes()
        option2 = int(input("Seleccione una opcion: "))
        if option2 == 1:
            conexion.All_Clientes()
        elif option2 == 2:
            conexion.Cliente_especifico()
        elif option2 == 3:
            conexion.Vehiculos_cliente()
        elif option2 == 4:
            conexion.Crear_Cliente()
        elif option2 == 5:
            conexion.Eliminar_cliente()
        elif option2 == 6:
            print("> Volviendo al menu principal...")
            time.sleep(1)
            conexion.clean()
        else:
            print("> Opcion no valida, intente nuevamente.")

#vehiculos

    elif option == 2:
        conexion.clean()
        conexion.menu_vehiculos()
        option2 = int(input("Seleccione una opcion: "))
        if option2 == 1:
            conexion.Vehiculos()
        elif option2 == 2:
            conexion.Vehiculo_especifico()
        elif option2 == 3:
            conexion.Crear_Vehiculo()
        elif option2 == 4:
            conexion.Eliminar_vehiculo()
        elif option2 == 5:
            print("> Volviendo al menu principal...")
            time.sleep(1)
            conexion.clean()
        else:
            print("> pcion no valida, intente nuevamente.")

#Mecanicos

    elif option == 3:
        conexion.clean()
        conexion.menu_mecanicos()
        option2 = int(input("Seleccione una opcion: "))
        if option2 == 1:
            conexion.Mecanicos()
        elif option2 == 2:
            conexion.Crear_Mecanico()
        elif option2 == 3:
            conexion.Mecanico_especifico()
        elif option2 == 4:
            conexion.Eliminar_mecanico()
        elif option2 == 5:
            print("> Volviendo al menu principal...")
            time.sleep(1)
            conexion.clean()
        else:
            print("> Opcion no valida, intente nuevamente.")

#Reparaciones

    elif option == 4:
        conexion.clean()
        conexion.menu_reparaciones()
        option2 = int(input("Seleccione una opcion: "))
        if option2 == 1:
            conexion.All_Reparaciones()
        elif option2 == 2:
            conexion.Reparacion_especifica()
        elif option2 == 3:
            conexion.Crear_Reparacion()
        elif option2 == 4:
            conexion.Eliminar_reparacion()
        elif option2 == 5:
            conexion.clean()
            print("> Menu de repuestos:")
            conexion.menu_respuestos()
            option3 = int(input("Seleccione una opcion: "))
            if option3 == 1:
                conexion.Agregar_repuestos()
            elif option3 == 2:
                conexion.Eliminar_repuestos()
            elif option3 == 3:
                conexion.Repuestos_especificos()
        elif option2 == 6:
            print("> Volviendo al menu principal...")
            time.sleep(1)
            conexion.clean()
        else:
            print("> Opcion no valida, intente nuevamente.")

# Fichas Tecnicas

    elif option == 5:
        conexion.clean()
        print("> Fichas Tecnicas:")
        print("1. Ver fichas tecnicas")
        print("2. Volver al menu principal")
        option2 = int(input("Seleccione una opcion: "))
        if option2 == 1:
            conexion.Fichas_Tecnicas()
        elif option2 == 2:
            print("> Volviendo al menu principal...")
            time.sleep(1)
            conexion.clean()

#Salir
    elif option == 6:
        conexion.salir()
    else:
        print("> Opcion no valida, intente nuevamente.")