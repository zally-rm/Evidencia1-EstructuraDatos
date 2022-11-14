import csv
import datetime
import os
import pandas as pd
import sqlite3
import sys

fecha_actual = datetime.datetime.now()
rounded_actual = fecha_actual.replace(hour=0, minute=0, second=0, microsecond=0)

dict_por_fecha = dict() #para el csv que se usará para exportar el reporte a excel

set_combs_posibles = set()
set_combs_ocupadas = set()

claves_salas_disp = list()
claves_turnos_disp = list()
salas_disponibles = list()

set_nums_clientes = set()
set_claves_salas = set()
set_descrip_evento = set()

if os.path.exists("Renta_espacios.db"):
    print("\nSe ha encontrado la base de datos en el directorio.\n")
else:
    print("No se ha encontrado una base de datos previa, se procede a crearla.\n")
    try:
        with sqlite3.connect("Renta_espacios.db") as conexion:
            mi_cursor = conexion.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS cliente (numero INTEGER PRIMARY KEY autoincrement, nombre TEXT NOT NULL);")
            print('Tabla "clientes" creada')
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS sala (clave INTEGER PRIMARY KEY autoincrement, nombre TEXT NOT NULL, cupo INTEGER NOT NULL);")
            print('Tabla "sala" creada')
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS turnos (clave TEXT PRIMARY KEY, nombre TEXT NOT NULL);")
            print('Tabla "turnos" creada')
            mi_cursor.execute("INSERT INTO turnos VALUES ('M', 'Matutino');")
            mi_cursor.execute("INSERT INTO turnos VALUES ('V', 'Vespertino');")
            mi_cursor.execute("INSERT INTO turnos VALUES ('N', 'Nocturno');")
            print("Registros de turnos ingresados.")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS evento (folio INTEGER PRIMARY KEY autoincrement, nombre TEXT NOT NULL, fecha timestamp NOT NULL, turno TEXT NOT NULL, sala INTEGER NOT NULL, idCliente INTEGER NOT NULL, FOREIGN KEY(turno) REFERENCES turnos(clave), FOREIGN KEY(sala) REFERENCES sala(clave), FOREIGN KEY(idCliente) REFERENCES cliente(numero));")
            print('Tabla "evento" creada')
    except sqlite3.Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

while True:
    print("***********************************************************")
    print("**                    MENÚ PRINCIPAL                     **")
    print("***********************************************************")
    print("1. Reservaciones")
    print("2. Reportes")
    print("3. Registrar una nueva sala.")
    print("4. Registrar a un nuevo cliente.")
    print("5. Salir.")
    opcion= int(input("Selecionar una opción: "))

    if opcion == 1:
        while True:
            print("\n***********************************************************")
            print("**               RESERVACIONES DE SALAS                  **")
            print("***********************************************************")
            print("1. Registrar nueva reservación.")
            print("2. Modificar descripción de una reservación.")
            print("3. Consultar disponibilidad de salas para un fecha.")
            print("4. Eliminar una reservación.")
            print("5. Volver al menú principal.")
            opcion2= int(input("Selecionar una opción: "))
            if opcion2 == 1:
                print("\n**********************************************************")
                print("**              RESERVACIÓN DE UNA SALA                 **")
                print("**********************************************************")
                try:
                    with sqlite3.connect("Renta_espacios.db") as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT * FROM cliente;")
                        clientes_registrados = mi_cursor.fetchall()
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                if (len(clientes_registrados) == 0):
                    print("\nNo se encontraron clientes registrados, registrate como cliente para hacer una reservación.")
                else:
                    print("\nNumero\tNombre")
                    print("*" * 30)
                    for numero, nombre in clientes_registrados:
                        print(f"{numero}\t{nombre}")
                    numero_capturado = int(input("\nIntroduce tu número de cliente para hacer una reservación: "))
                    try: 
                        with sqlite3.connect("Renta_espacios.db") as conexion:
                            mi_cursor = conexion.cursor()
                            mi_cursor.execute("SELECT numero FROM cliente;")
                            numeros_clientes = mi_cursor.fetchall()
                    except sqlite3.Error as e:
                        print(e)
                    except:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    for elemento in numeros_clientes:
                        set_nums_clientes.add(elemento[0])
                    if numero_capturado in set_nums_clientes:
                        print("\nSalas disponibles para renta: ")
                        try:
                            with sqlite3.connect("Renta_espacios.db") as conexion:
                                mi_cursor = conexion.cursor()
                                mi_cursor.execute("SELECT * FROM sala;")
                                salas_registradas = mi_cursor.fetchall()
                                if salas_registradas:
                                    print("\nClave\tNombre de sala\tCupo")
                                    print("*" * 50)
                                    for clave, nombre, cupo in salas_registradas:
                                        print(f"{clave}\t{nombre}\t\t{cupo}")
                                    sala_deseada=int(input('\nIngrese la clave de la sala que desea reservar: '))
                                    for elemento in salas_registradas:
                                        set_claves_salas.add(elemento[0])
                                    while sala_deseada not in set_claves_salas:
                                        print("\n-- La clave de sala no existe. Ingresa una clave existente. --")
                                        sala_deseada=int(input('\nIngrese la clave de la sala que desea reservar: '))
                                    else:
                                        nombre_evento = input("Introduce el nombre del evento: ")
                                        while nombre_evento == "" or nombre_evento.isspace() == True:
                                            print("\n-- Debe escribirse un nombre para el evento --")
                                            nombre_evento = input("Introduce el nombre del evento: ")
                                        fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
                                        while (fecha_capturada == "" or str.isspace(fecha_capturada)):
                                            print("\n-- Se debe escribir una fecha para el evento --")
                                            fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
                                        fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                                        fecha_evento = datetime.datetime.combine(fecha_procesada, datetime.time(00, 00, 00))
                                        delta = fecha_evento - rounded_actual
                                        while (delta.days < 2):
                                            print("\nLa reservación tiene que ser, por lo menos, dos días antes de la fecha actual.\n")
                                            fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
                                            fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                                            fecha_evento = datetime.datetime.combine(fecha_procesada, datetime.time(00, 00, 00))
                                            delta = fecha_evento - rounded_actual
                                        turno_evento = input("Ingresa el turno en el que quieres reservar la sala (M (matutino)/ V (vespertino) / N (nocturno): ").upper()
                                        while (turno_evento == "") or (turno_evento.isspace() == True) or turno_evento not in ("M", "V", "N"):
                                            print("\n-- Se debe ingresar un turno válido para la reservación --")
                                            turno_evento = input("Ingresa el turno en el que quieres reservar la sala (M (matutino)/ V (vespertino) / N (nocturno): ").upper()
                                        with sqlite3.connect("Renta_espacios.db") as conn:
                                                condiciones_sala = (sala_deseada, str(fecha_procesada), turno_evento)
                                                mi_cursor = conn.cursor()
                                                mi_cursor.execute("SELECT * FROM evento WHERE sala=? And fecha=? And turno=?", condiciones_sala)
                                                salas_ocupadas = mi_cursor.fetchall()
                                                if salas_ocupadas:
                                                    print("\nYa existe una reservación para esa sala, a esa fecha y en ese turno.")
                                                else:
                                                    try:
                                                        with sqlite3.connect("Renta_espacios.db") as conn:
                                                            mi_cursor = conn.cursor()
                                                            dict_evento = {"nombre":nombre_evento, "fecha":fecha_procesada, "turno":turno_evento, "sala":sala_deseada, "idCliente":numero_capturado}
                                                            mi_cursor.execute("INSERT INTO evento (nombre, fecha, turno, sala, idCliente) VALUES(:nombre, :fecha, :turno, :sala, :idCliente)", dict_evento) 
                                                            print("\nRegistro de evento agregado.")
                                                            print(f"\nEl folio del evento es {mi_cursor.lastrowid}, el nombre es {nombre_evento}, la fecha es {fecha_procesada.strftime('%d/%m/%Y')}, el turno es {turno_evento}\n")
                                                    except sqlite3.Error as e:
                                                        print (e)
                                                    except:
                                                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                                else:
                                    print("\nNo se encontraron salas registradas, registra una sala para reservarla.")
                        except sqlite3.Error as e:
                            print(e)
                        except:
                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    else:
                        print("\nEl número de cliente no existe, tienes que registrarte para hacer una reservación.\n")
            elif opcion2 == 2:
                print("\n**********************************************************")
                print("**         DESCRIPCIÓN DE UNA RESERVACIÓN               **")
                print("**********************************************************")
                try:
                    with sqlite3.connect("Renta_espacios.db") as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT * FROM evento;")
                        eventos_registrados = mi_cursor.fetchall()
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                if (len(eventos_registrados) == 0):
                    print("\nNo se encontraron eventos registrados.")
                else:
                    print("\nFolio\tNombre\t Fecha\tTurno\tSala\tCliente")
                    print("*" * 55)
                    for folio, nombre, fecha, turno, sala, cliente in eventos_registrados:
                        print(f"{folio}\t{nombre}\t {fecha}\t{turno}\t{sala}\t{cliente}")
                    folio_capturado = int(input("\nIntroduce el folio del evento que deseas editar: "))
                    for evento in eventos_registrados:    
                        if (folio_capturado == evento[0]):
                            set_descrip_evento = (evento[0], evento[1])
                    while (len(set_descrip_evento) == 0):
                        print("\n-- El folio de evento no existe. Ingresa uno existente --")
                        folio_capturado = int(input("\nIntroduce el folio del evento que deseas editar: "))
                        for evento in eventos_registrados:    
                            if (folio_capturado == evento[0]):
                                set_descrip_evento = (evento[0], evento[1])
                    else:
                        nuevo_nombre_evento = input(f"\nEscribe el nuevo nombre del evento (previamente {set_descrip_evento[1]}): ")
                        while (nuevo_nombre_evento == "" or str.isspace(nuevo_nombre_evento)):
                            print("\n-- Debe escribirse un nombre nuevo para el evento --")
                            nuevo_nombre_evento = input(f"\nEscribe el nuevo nombre del evento (previamente {set_descrip_evento[1]}): ")
                        try:
                            with sqlite3.connect("Renta_espacios.db") as conexion:
                                mi_cursor = conexion.cursor()
                                tupla_nombre_evento = (nuevo_nombre_evento, folio_capturado)
                                mi_cursor.execute("UPDATE evento SET nombre=? WHERE folio=?;", tupla_nombre_evento)
                                print(f'\nSe ha cambiado el nombre del evento con folio {set_descrip_evento[0]} a: "{nuevo_nombre_evento}" ')
                        except sqlite3.Error as e:
                            print(e)
                        except:
                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion2 == 3:
                print("\n**********************************************************")
                print("**              DISPONIBILIDAD DE SALAS                  **")
                print("**********************************************************")
                fecha_busqueda = input("\nIngresa la fecha para la que quieres ver las salas disponibles (DD/MM/AAAA): ")
                while (fecha_busqueda == "" or str.isspace(fecha_busqueda)):
                    print("\n-- No se ha escrito una fecha. Escribe una fecha para continuar --")
                    fecha_busqueda = input("\nIngresa la fecha para la que quieres ver las salas disponibles (DD/MM/AAAA): ")
                fecha_busq_proc = datetime.datetime.strptime(fecha_busqueda, "%d/%m/%Y").date()
                print(f"\n ** Salas disponibles el {fecha_busq_proc} **\n")
                tupla_fecha_disp = (str(fecha_busq_proc), )
                try:
                    with sqlite3.connect("Renta_espacios.db") as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT clave FROM SALA;")
                        respuesta_salas = mi_cursor.fetchall()
                        mi_cursor.execute("SELECT clave FROM turnos;")
                        respuesta_turnos = mi_cursor.fetchall()
                        for sala in respuesta_salas:
                            for turno in respuesta_turnos:
                                set_combs_posibles.add((sala[0], turno[0]))
                        mi_cursor.execute("SELECT sala, turno FROM evento WHERE fecha=?;", tupla_fecha_disp)
                        lista_combs_ocupadas = mi_cursor.fetchall()
                        for sala, turno in lista_combs_ocupadas:
                            set_combs_ocupadas.add((sala, turno))
                        set_combs_disponibles = set_combs_posibles - set_combs_ocupadas
                        if set_combs_disponibles:
                            for set in set_combs_disponibles:
                                tupla_temporal = (set[0], set[1])
                                mi_cursor.execute("SELECT s.clave, s.nombre, t.clave FROM sala s, turnos t WHERE s.clave = ? AND t.clave = ?;", tupla_temporal)
                                sala_disponible = mi_cursor.fetchall()
                                salas_disponibles.append(sala_disponible)
                            if salas_disponibles:
                                print("\nClave\tNombre de sala\tTurno")
                                print("*" * 40)
                                for cada_sala in salas_disponibles:
                                    for clave, nombre, turno in cada_sala:
                                        print(f"{clave}\t{nombre}\t\t {turno}")
                        else:
                            print("\nNo se encontraron salas disponibles en esa fecha.")
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion2 == 4:
                print("\n**********************************************************")
                print("**               ELIMINAR UNA RESERVA                   **")
                print("**********************************************************")
                try:
                    with sqlite3.connect("Renta_espacios.db") as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT * FROM evento")
                        eventos_registrados = mi_cursor.fetchall()
                        if eventos_registrados:
                            print("\n** Reservaciones registradas **")
                            print("\nFolio\tNombre\t\tFecha\t\tTurno \tSala\tidCliente")
                            print("*" * 70)
                            for folio, nombre, fecha, turno, sala, cliente in eventos_registrados:
                                print(f"{folio}\t{nombre}\t{fecha}\t{turno}\t{sala}\t{cliente}")
                        else:
                            print("\nNo se encontraron reservaciones registradas.")
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                if eventos_registrados:
                    folio_eliminar = int(input("\nIngresa el folio del evento que deseas eliminar: "))
                    try:
                        with sqlite3.connect("Renta_espacios.db") as conexion:
                            mi_cursor = conexion.cursor()
                            tupla_folio_eliminar = (folio_eliminar, )
                            mi_cursor.execute("SELECT * FROM evento WHERE folio = ?", tupla_folio_eliminar)
                            evento_con_folio = mi_cursor.fetchall()
                            if evento_con_folio:                    
                                print("\n** Reservación a eliminar **")
                                print("\nFolio\tNombre\t\tFecha\t\tTurno \tSala\tidCliente")
                                print("*" * 70)
                                for folio, nombre, fecha, turno, sala, cliente in evento_con_folio:
                                    print(f"{folio}\t{nombre}\t{fecha}\t{turno}\t{sala}\t{cliente}")
                                opcion_eliminar = int(input("\n¿Deseas eliminar este evento? Esta acción no puede deshacerse.\n1.Si\n2.No\n>"))
                                if opcion_eliminar == 1:
                                    for folio, nombre, fecha, turno, sala, cliente in evento_con_folio:
                                        fecha_evento_eliminar = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                                        fecha_proc_eliminar = datetime.datetime.combine(fecha_evento_eliminar, datetime.time(00, 00, 00))
                                        delta_eliminar = fecha_proc_eliminar - rounded_actual
                                    if (delta_eliminar.days < 3):
                                        print("\nSolo se pueden eliminar reservaciones con, por lo menos, tres días de anticipación.")
                                    else:
                                        try:
                                            mi_cursor.execute("DELETE FROM evento WHERE folio = ?", tupla_folio_eliminar)
                                            print(f"\nSe ha eliminado la reservación con el folio {folio_eliminar}.")
                                        except sqlite3.Error as e:
                                            print(e)
                                        except:
                                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                                else:
                                    print("\nSe ha suspendido la operación.")
                            else:
                                print("\nNo se encontró una reservación con ese folio.")
                    except sqlite3.Error as e:
                        print(e)
                    except:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion2 == 5:
                break
    elif opcion == 2:
        while True:
            print("\n***********************************************************")
            print("**              REPORTES DE RESERVACIONES                **")
            print("***********************************************************")
            print("1. Reporte en pantalla de reservaciones para una fecha.")
            print("2. Exportar reporte tabular en Excel.")
            print("3. Volver al menú principal.")
            opcion3= int(input("Selecionar una opción: "))
            if opcion3 == 1:
                fecha_consulta = input("\nIntroduce la fecha a consultar (DD/MM/AAAA): ")
                while (fecha_consulta == "" or str.isspace(fecha_consulta)):
                    print("\n-- No se ha escrito una fecha. Escribe una fecha para continuar --")
                    fecha_consulta = input("\nIntroduce la fecha a consultar (DD/MM/AAAA): ")
                fecha_proc_consulta = datetime.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
                tupla_fecha_consulta = (fecha_proc_consulta,)
                try:
                    with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT evento.sala, cliente.nombre, evento.folio, evento.nombre, evento.turno FROM evento INNER JOIN cliente ON cliente.numero=evento.idCliente WHERE evento.fecha=?;", tupla_fecha_consulta)
                        eventos_en_fecha = mi_cursor.fetchall()
                        if eventos_en_fecha:
                            print("\n---------------------------------------------------------------------")
                            print(f"--    REPORTE DE RESERVACIONES PARA EL DÍA {fecha_proc_consulta}  --")
                            print("---------------------------------------------------------------------")
                            print("SALA\tCLIENTE\t\tFOLIO\t\tEVENTO\t\tTURNO")
                            print("---------------------------------------------------------------------")
                            for sala, cliente, folio, evento, turno in eventos_en_fecha:
                                print(f"{sala}\t{cliente}\t\t{folio}\t\t{evento}\t\t{turno}")
                            print("----------                 FIN DEL REPORTE                -----------\n")
                        else:
                            print("\nNo se encontraron reservaciones registradas para esa fecha.")
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion3 == 2:
                fecha_consulta = input("\nIntroduce la fecha a consultar (DD/MM/AAAA): ")
                while (fecha_consulta == "" or str.isspace(fecha_consulta)):
                    print("\n-- No se ha escrito una fecha. Escribe una fecha para continuar --")
                    fecha_consulta = input("\nIntroduce la fecha a consultar (DD/MM/AAAA): ")
                fecha_proc_consulta = datetime.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
                tupla_fecha_exportar = (fecha_proc_consulta,)
                try:
                    with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT evento.folio, evento.sala, cliente.nombre, evento.nombre, evento.turno FROM evento INNER JOIN cliente ON cliente.numero=evento.idCliente WHERE evento.fecha=?;", tupla_fecha_exportar)
                        eventos_a_export = mi_cursor.fetchall()
                        if eventos_a_export:
                            for folio, sala, cliente, evento, turno in eventos_a_export:
                                dict_por_fecha[folio] = [sala, cliente, evento, turno]
                            with open("reservaciones.csv","w", newline="") as archivo_reserv:
                                grabador = csv.writer(archivo_reserv)
                                grabador.writerow(("Folio del evento", "Sala", "Cliente", "Nombre", "Turno"))
                                grabador.writerows([(clave, datos[0], datos[1], datos[2], datos[3]) for clave, datos in dict_por_fecha.items()])
                            df_reserv_fecha = pd.read_csv('reservaciones.csv')
                            excel_reserv = pd.ExcelWriter('reservaciones.xlsx')
                            df_reserv_fecha.to_excel(excel_reserv, index=False)
                            excel_reserv.save()
                            print("\nSe ha creado el archivo excel.\n")
                        else:
                            print("\nNo se encontraron reservaciones registradas para esa fecha.")
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion3 == 3:
                break
    elif opcion == 3:
        print("\n**********************************************************")
        print("**           REGISTRAR UNA NUEVA SALA                **")
        print("**********************************************************")
        nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        while nombre_sala == "" or nombre_sala.isspace() == True:
            print("\n-- Debe escribirse un nombre para la sala --")
            nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        cupo_sala = int(input("Ingresa el cupo de la sala: "))
        while (cupo_sala <= 0):
            print("\n-- Ingresa un cupo de sala válido --")
            cupo_sala = int(input("Ingresa el cupo de la sala: "))
        try:
            with sqlite3.connect("Renta_espacios.db") as conexion:
                mi_cursor = conexion.cursor()
                tupla_sala = (nombre_sala, cupo_sala)
                mi_cursor.execute("INSERT INTO sala (nombre, cupo) VALUES(?, ?);", tupla_sala) 
                print("\nRegistro de sala agregado.")
                print(f"\nLa nueva sala ha quedado registrada como: Clave: {mi_cursor.lastrowid} | Nombre: {nombre_sala} | Cupo: {cupo_sala}\n")
        except sqlite3.Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    elif opcion == 4:
        print("\n**********************************************************")
        print("**           REGISTRO DE CLIENTE                 **")
        print("**********************************************************")
        nombre_cliente = input("Introduce tu nombre como cliente: ")
        while nombre_cliente == "" or nombre_cliente.isspace() == True:
            print("\n-- Debe escribirse un nombre de cliente para el registro --")
            nombre_cliente = input("Introduce tu nombre como cliente: ")
        try:
            with sqlite3.connect("Renta_espacios.db") as conexion:
                mi_cursor = conexion.cursor()
                tupla_nombre_cliente = (nombre_cliente, )
                mi_cursor.execute("INSERT INTO cliente (nombre) VALUES(?);", tupla_nombre_cliente) 
                print("\nRegistro de cliente agregado.")
                print(f"\nEl número de cliente para {nombre_cliente} es {mi_cursor.lastrowid}\n")
        except sqlite3.Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    elif opcion == 5:
        break
if (conexion):
    conexion.close()