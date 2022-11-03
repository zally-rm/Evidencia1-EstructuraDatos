import csv
import datetime
import os
import pandas as pd
import random
import sys
import sqlite3

fecha_actual = datetime.date.today()

posibles_claves_sala = list(range(2,10))

posibles_nums_cliente = list(range(11,100))

posibles_folios_evento = list(range(101, 200))

dict_por_fecha = dict()

conjunto_salas = set()

conjunto_eventos = set()

dict_salas_disp = dict()

set_salas_por_fecha = set()

dict_salas_turnos = dict()


if os.path.exists("Renta_espacios.db"):
    print("Se ha encontrado la base de datos en el directorio.\n")
    try:
      with sqlite3.connect("Renta_espacios.db") as conexion:
          mi_cursor = conexion.cursor()
          mi_cursor.execute("SELECT * FROM sala;")
          para_conjunto_salas1 = mi_cursor.fetchall()
          mi_cursor.execute("SELECT * FROM turnos;")
          para_conjunto_salas2 = mi_cursor.fetchall()
          for para_salas in para_conjunto_salas1:
            for para_turnos in para_conjunto_salas2:
              conjunto_salas.add((para_salas[0], para_turnos[0]))
          
          mi_cursor.execute("SELECT sala, turno FROM evento;")
          para_conjunto_evento = mi_cursor.fetchall()
          for para_eventos_sala, para_eventos_turno in para_conjunto_evento:
            conjunto_eventos.add((para_eventos_sala, para_eventos_turno))
    except sqlite3.Error as e:
      print(e)
    except:
      print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
else:
    print("No se ha encontrado una base de datos previa, se procede a crearla.\n")
    try:
        with sqlite3.connect("Renta_espacios.db") as conexion:
            mi_cursor = conexion.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS cliente (numero INTEGER PRIMARY KEY, nombre TEXT NOT NULL);")
            print('Tabla "clientes" creada')
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS sala (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL, cupo INTEGER NOT NULL);")
            print('Tabla "sala" creada')
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS turnos (clave TEXT PRIMARY KEY, nombre TEXT NOT NULL);")
            print('Tabla "turnos" creada')

            mi_cursor.execute("INSERT INTO turnos VALUES ('M', 'Matutino');")
            mi_cursor.execute("INSERT INTO turnos VALUES ('V', 'Vespertino');")
            mi_cursor.execute("INSERT INTO turnos VALUES ('N', 'Nocturno');")
            print("Registros de turnos ingresados.")

            mi_cursor.execute("CREATE TABLE IF NOT EXISTS evento (folio INTEGER PRIMARY KEY, nombre TEXT NOT NULL, fecha timestamp NOT NULL, turno TEXT NOT NULL, sala INTEGER NOT NULL, idCliente INTEGER NOT NULL, FOREIGN KEY(turno) REFERENCES turnos(clave), FOREIGN KEY(sala) REFERENCES sala(clave), FOREIGN KEY(idCliente) REFERENCES cliente(numero));")
            print('Tabla "evento" creada')
    except sqlite3.Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

while True:
    print("***********************************************************")
    print("**               RENTA DE SALAS DE REUNIONES             **")
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
                print("**         RESERVACIÓN DE UNA SALA               **")
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
                if clientes_registrados == False:
                    print("\nNo se encontraron clientes registrados, registrate como cliente para hacer una reservación.")
                else:
                    print("\nNumero\tNombre")
                    print("*" * 30)
                    for numero, nombre in clientes_registrados:
                        print(f"{numero}\t{nombre}")
                    numero_capturado = int(input("\nIntroduce tu número de cliente para hacer una reservación: "))
                    if ((tupla[0] == numero_capturado) for tupla in clientes_registrados):
                        print("\nSalas disponibles para renta: ")
                        set_salas_disp = conjunto_salas - conjunto_eventos
                        for sala, turno in set_salas_disp:
                            dict_salas_disp["clave_sala"] = sala
                        try:
                            with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
                                mi_cursor = conexion.cursor()
                                mi_cursor.execute("SELECT * FROM sala WHERE clave=:clave_sala;", dict_salas_disp)
                                salas_registradas = mi_cursor.fetchall()
                                if salas_registradas:
                                    print("\nClave\tNombre de sala\tCupo")
                                    print("*" * 50)
                                    for clave, nombre, cupo in salas_registradas:
                                        print(f"{clave}\t{nombre}\t{cupo}")
                                    sala_deseada=int(input('\nIngrese la clave de la sala que desea reservar: '))
                                    if ((sala_deseada == sala[0]) for sala in salas_registradas):
                                        nombre_evento = input("Introduce el nombre del evento: ")
                                        fecha_capturada = input("Introduce la fecha del evento (DD/MM/AAAA): ")
                                        fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                                        delta = fecha_procesada - fecha_actual
                                        if (delta.days <= 2):
                                            print("\nLa reservación tiene que ser, por lo menos, dos días antes de la fecha actual.\n")
                                        else:
                                            turno_evento = input("Ingresa el turno en el que quieres reservar la sala (M (matutino)/ V (vespertino) / N (nocturno): ").upper()
                                            with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                                                    condiciones_sala = (sala_deseada, fecha_procesada, turno_evento)
                                                    mi_cursor = conn.cursor()
                                                    mi_cursor.execute("SELECT * FROM evento WHERE sala=? And fecha=? And turno=?", condiciones_sala)
                                                    salas_ocupadas = mi_cursor.fetchall()
                                                    if salas_ocupadas:
                                                        print("\nYa existe una reservación para esa sala, a esa fecha y en ese turno.")
                                                    else:
                                                        folio_evento = random.choice(posibles_folios_evento)
                                                        posibles_folios_evento.remove(folio_evento)
                                                        try:
                                                            with sqlite3.connect("Renta_espacios.db") as conn:
                                                                mi_cursor = conn.cursor()
                                                                dict_evento = {"folio":folio_evento, "nombre":nombre_evento, "fecha":fecha_procesada, "turno":turno_evento, "sala":sala_deseada, "idCliente":numero_capturado}
                                                                mi_cursor.execute("INSERT INTO evento VALUES(:folio, :nombre, :fecha, :turno, :sala, :idCliente)", dict_evento) 
                                                                print("\nRegistro de evento agregado.")
                                                                print(f"\nEl folio del evento es {folio_evento}, el nombre es {nombre_evento}, la fecha es {fecha_procesada.strftime('%d/%m/%Y')}, el turno es {turno_evento}\n")
                                                                conjunto_eventos.add((sala_deseada, turno_evento))
                                                        except sqlite3.Error as e:
                                                            print (e)
                                                        except:
                                                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                                    else:
                                        print("\nNo se encontró una sala registrada con esa clave.")
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
                        mi_cursor.execute("SELECT folio, nombre, sala FROM evento;")
                        eventos_registrados = mi_cursor.fetchall()
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                if eventos_registrados == False:
                  print("\nNo se encontraron eventos registrados.")
                else:
                  print("\nFolio\tNombre\tSala")
                  print("*" * 40)
                  for folio, nombre, sala in eventos_registrados:
                    print(f"{folio}\t{nombre}\t{sala}")
                  folio_capturado = int(input("Introduce el folio del evento que deseas editar: "))
                  for evento in eventos_registrados:
                    if (folio_capturado == evento[0]):
                      nuevo_nombre_evento = input(f"Escribe el nuevo nombre del evento (previamente {evento[1]}): ")
                      try:
                            with sqlite3.connect("Renta_espacios.db") as conexion:
                                mi_cursor = conexion.cursor()
                                tupla_nombre_evento = (nuevo_nombre_evento, folio_capturado)
                                mi_cursor.execute("UPDATE evento SET nombre=? WHERE folio=?;", tupla_nombre_evento)
                                print(f"Cambiaste el nombre de tu evento a: {nuevo_nombre_evento}")
                      except sqlite3.Error as e:
                        print(e)
                      except:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    else:
                      print("No se ha encontrado un evento con ese folio.")
            elif opcion2 == 3:
                print("\n**********************************************************")
                print("**              DISPONIBILIDAD DE SALAS                  **")
                print("**********************************************************")
                fecha_busqueda = input("\nIngresa la fecha para la que quieres ver las salas disponibles (DD/MM/AAAA): ")
                fecha_busq_proc = datetime.datetime.strptime(fecha_busqueda, "%d/%m/%Y").date()
                print(f"\n ** Salas disponibles el {fecha_busq_proc} **\n")
                tupla_fecha_disp = (fecha_busq_proc, )
                try:
                    with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT sala, turno FROM evento WHERE fecha=?;", tupla_fecha_disp)
                        salaTurno_evento = mi_cursor.fetchall()
                        for sala1, turno1 in salaTurno_evento:
                            set_salas_por_fecha.add((sala1, turno1))
                        sala_turno_disp = (conjunto_salas - set_salas_por_fecha)
                        lista_sala = list()
                        lista_turno = list()
                        for item in sala_turno_disp:
                            lista_sala.append(item[0])
                            lista_turno.append(item[1])
                        tupla_de_tuplas = (tuple(lista_sala), tuple(lista_turno))
                        mi_cursor.execute("SELECT sala.clave, sala.nombre, turnos.clave FROM sala INNER JOIN evento ON sala.clave=evento.sala INNER JOIN turnos ON turnos.clave=evento.turno WHERE sala.clave = ? AND turnos.clave = ?", tupla_de_tuplas)
                        salas_disponibles = mi_cursor.fetchall()
                        if salas_disponibles:
                            print("\nClave\tNombre de sala\tTurno")
                            print("*" * 50)
                            for clave, nombre, turno in salas_disponibles:
                                print(f"{clave}\t{nombre}\t\t{turno}")
                        else:
                            print("\nNo se encontraron salas disponibles en esa fecha.")
                except sqlite3.Error as e:
                    print(e)
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
                            print("\nFolio\tNombre\tFecha\tTurno\tSala\t idCliente")
                            print("*" * 60)
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
                            dict_folio_eliminar = {"folio":folio_eliminar}
                            mi_cursor.execute("SELECT * FROM evento WHERE folio = :folio", dict_folio_eliminar)
                            evento_con_folio = mi_cursor.fetchall()
                            if evento_con_folio:                    
                                print("\n** Reservación a eliminar **")
                                print("\nFolio\tNombre\tFecha\tTurno\tSala\t idCliente")
                                print("*" * 50)
                                for folio, nombre, fecha, turno, sala, cliente in evento_con_folio:
                                    print(f"{folio}\t{nombre}\t{fecha}\t{turno}\t{sala}\t{cliente}")
                                opcion_eliminar = int(input("\n¿Deseas eliminar este evento? Esta acción no puede deshacerse.\n1.Si\t2.No\n"))
                                if opcion_eliminar == 1:
                                    for folio, nombre, fecha, turno, sala, cliente in evento_con_folio:
                                        fecha_proc_eliminar = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                                        delta_eliminar = fecha_proc_eliminar - fecha_actual
                                    if (delta_eliminar.days <= 3):
                                        print("\nSolo se pueden eliminar reservaciones con, por lo menos, tres días de anticipación.")
                                    else:
                                        try:
                                            mi_cursor.execute("DELETE FROM evento WHERE folio = :folio", dict_folio_eliminar)
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
                fecha_proc_consulta = datetime.datetime.strptime(fecha_consulta, "%d/%m/%Y").date()
                tupla_fecha_consulta = (fecha_proc_consulta,)
                try:
                    with sqlite3.connect("Renta_espacios.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conexion:
                        mi_cursor = conexion.cursor()
                        mi_cursor.execute("SELECT evento.sala, cliente.nombre, evento.nombre, evento.turno FROM evento INNER JOIN cliente ON cliente.numero=evento.idCliente WHERE evento.fecha=?;", tupla_fecha_consulta)
                        eventos_en_fecha = mi_cursor.fetchall()
                        if eventos_en_fecha:
                            print("\n---------------------------------------------------------------------")
                            print(f"--    REPORTE DE RESERVACIONES PARA EL DÍA {fecha_proc_consulta}  --")
                            print("---------------------------------------------------------------------")
                            print("SALA\t\tCLIENTE\t\tEVENTO\t\tTURNO\t")
                            print("---------------------------------------------------------------------")
                            for sala, cliente, evento, turno in eventos_en_fecha:
                                print(f"{sala}\t\t{cliente}\t\t{evento}\t\t{turno}\t")
                            print("----------                 FIN DEL REPORTE                -----------\n")
                        else:
                            print("\nNo se encontraron reservaciones registradas para esa fecha.")
                except sqlite3.Error as e:
                    print(e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            elif opcion3 == 2:
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
        while nombre_sala == "":
            print("-- Debe escribirse un nombre para la sala --")
            nombre_sala = input("Ingresa el nombre de la nueva sala: ")
        cupo_sala = int(input("Ingresa el cupo de la sala: "))
        while cupo_sala == 0:
            print("-- El cupo de la sala debe ser mayor a  0 --")
            cupo_sala = int(input("Ingresa el cupo de la sala: "))
        clave_sala = random.choice(posibles_claves_sala)
        posibles_claves_sala.remove(clave_sala)
        try:
            with sqlite3.connect("Renta_espacios.db") as conexion:
                mi_cursor = conexion.cursor()
                dict_sala = {"clave":clave_sala, "nombre":nombre_sala, "cupo":cupo_sala}
                mi_cursor.execute("INSERT INTO sala VALUES(:clave, :nombre, :cupo);", dict_sala) 
                print("\nRegistro de sala agregado.")
                print(f"\nLa nueva sala ha quedado registrada como: Clave: {clave_sala} | Nombre: {nombre_sala} | Cupo: {cupo_sala}\n")
                mi_cursor.execute("SELECT clave FROM turnos;")
                tupla_turnos = mi_cursor.fetchall()
                for turno in tupla_turnos:
                  conjunto_salas.add((clave_sala, turno))
        except sqlite3.Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    elif opcion == 4:
        print("\n**********************************************************")
        print("**           REGISTRO DE CLIENTE                 **")
        print("**********************************************************")
        nombre_cliente = input("Introduce tu nombre como cliente: ")
        while nombre_cliente == "":
            print("-- Debe escribirse un nombre de cliente para el registro --")
            nombre_cliente = input("Introduce tu nombre como cliente: ")
        numero_cliente = random.choice(posibles_nums_cliente)
        posibles_nums_cliente.remove(numero_cliente)
        try:
            with sqlite3.connect("Renta_espacios.db") as conexion:
                mi_cursor = conexion.cursor()
                dict_cliente = {"numero":numero_cliente, "nombre":nombre_cliente}
                mi_cursor.execute("INSERT INTO cliente VALUES(:numero, :nombre);", dict_cliente) 
                print("\nRegistro de cliente agregado.")
                print(f"\nEl número de cliente para {nombre_cliente} es {numero_cliente}\n")
        except sqlite3.Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    elif opcion == 5:
        break
if (conexion):
    conexion.close()